Based on the error message and the provided context, the issue seems to be occurring during the cloning of a functional model with multiple outputs. The specific assertion error indicates that the output tensor 'Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)' could not be found in the `tensor_map`.

The potential error location within the problematic function seems to be in the block of code where the function iterates over the nodes of the model, gets or creates new layers, gathers input and output tensors, calls the new layers, and updates the `tensor_map` accordingly. 

The reason behind the occurrence of the bug could be related to discrepancies in the input and output tensors, as well as the creation of new layers, causing the function to return incorrect results. Additionally, mismatches in shapes and types of input/output tensors and layers might also be contributing to the error.

To fix the bug, it is necessary to ensure that the input tensors and layers are properly created and mapped, and that the input and output tensors, as well as the new layers, are handled correctly during the cloning process. Careful attention to these aspects is crucial for identifying and resolving the bugs.

Please find the revised version of the `_clone_functional_model` function below:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)
    
    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
                         for layer in model._input_layers]
    else:
        # Make sure that all input tensors come from a Keras layer.
        input_tensors = to_list(input_tensors)
        input_layers = [x._keras_history[0] if K.is_keras_tensor(x) else Input(tensor=x, name='input_wrapper_for_' + model._input_layers[i].name)
                        for i, x in enumerate(input_tensors)]
        for orig, cloned in zip(model._input_layers, input_layers):
            layer_map[orig] = cloned
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask
    
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]
                if isinstance(new_layer, InputLayer):
                    continue
            
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
            
            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                
                computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This revised version of the function addresses the issues related to input tensor creation, layer mapping, and tensor mapping, ensuring proper handling of input and output tensors, as well as the creation of new layers during the cloning process. It should resolve the bug and produce the expected output.