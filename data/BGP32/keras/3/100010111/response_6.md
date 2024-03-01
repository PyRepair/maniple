### Analysis:
1. The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance with new layers and weights instead of sharing existing weights.
   
2. The error message states that an assertion fails because the output tensor is not present in `tensor_map`.

3. The function loops over the nodes of the model to create and call layers. The bug might be related to how tensors and layers are managed in the cloning process, especially when dealing with multiple outputs and layers that do not support masks.

4. The error in the failing test is due to the Lambda layer not supporting masks, leading to None values, causing the assertion to fail. Updating the cloning mechanism to handle cases where the layer does not support masks should resolve this issue.

### Strategy for fixing the bug:
1. When encountering a layer that does not support masks, handle the case appropriately to prevent issues with the tensor mapping.
2. Add conditions to account for multiple output tensors in the layers when building the model.
3. Make sure that the tensors and corresponding outputs are correctly mapped during the cloning process.

### Bug-fixed function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) 
                        for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                layer_map[x] = input_tensor
                input_tensors[i] = input_tensor
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            new_layer = layer.__class__.from_config(layer.get_config())

            if layer not in layer_map:
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                if node.supports_masking:
                    output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))

                output_tensors = to_list(new_layer(computed_tensors, **kwargs))

                if node.supports_masking:
                    for x, y, mask in zip(reference_input_tensors, output_tensors, output_masks):
                        tensor_map[x] = (y, mask)
                else:
                    for x, y in zip(reference_output_tensors, output_tensors):
                        tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

Now, with the introduced fixes and adjustments, the function should correctly handle the cloning of a functional model, especially in scenarios where layers do not support masking.