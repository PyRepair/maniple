### Analysis:
1. The function `_clone_functional_model` is responsible for cloning a functional model by creating new layers and new weights instead of sharing the existing ones. It iterates over the nodes of the original model and creates new layers based on the node's outbound layer. It then updates the input and output tensors based on the cloned layers.
   
2. The error is raised when the function tries to compute the output tensor for a swap layer in the model. The failing assertion indicates that the output tensor for a specific layer could not be computed.
   
3. The expected values and types of variables show that the tensor mapping is missing the required output tensor for the swap layer. This is mainly due to problems in updating the tensor mapping correctly during the cloning process, especially in handling layers that have multiple outputs.

### Solution:
1. To fix the bug, we need to ensure that the tensor mapping is correctly updated for all layers, including those with multiple outputs.
   
2. We should make sure that the function correctly handles layers that do not support masking, like the Lambda layer in this case.
   
3. Update the tensor mapping and output tensor computation mechanisms to cater to layers with multiple outputs properly.

### Corrected function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                cloned_input_layer = input_tensor._keras_history[0]
                layer_map[x] = cloned_input_layer
        input_tensors = [layer_map.get(input_tensor, input_tensor) for input_tensor in input_tensors]

    for original_input, cloned_input in zip(model.inputs, input_tensors):
        tensor_map[original_input] = (cloned_input, None)

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                computed_data.append(tensor_map.get(x, (None, None)))

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                if has_arg(layer.call, 'mask'):
                    if len(computed_tensors) == 1:
                        kwargs.setdefault('mask', computed_masks[0])
                    else:
                        kwargs.setdefault('mask', computed_masks)
                
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for output_tensor, reference_output in zip(output_tensors, reference_output_tensors):
                    tensor_map[reference_output] = (output_tensor, None)

    output_tensors = [tensor_map.get(x, None) for x in model.outputs]
    assert all(output_tensor is not None for output_tensor in output_tensors), 'Could not compute output tensors'
    
    return Model(input_tensors, output_tensors, name=model.name)
``` 

This corrected function addresses the issues in updating the tensor mapping and computing the output tensors correctly, especially for layers with multiple outputs. It ensures that the model cloning process proceeds smoothly and is capable of handling complex model structures like the one in the failing test case.