The bug in the `_clone_functional_model` function is caused by an issue in handling the input layers when cloning a model with multiple output layers. The function fails to correctly map the input layers and their corresponding tensors, leading to incorrect behavior when creating the new cloned model.

To fix this bug, we need to ensure that the input layers are properly mapped to their corresponding tensors and that the model's outputs are correctly computed and returned in the new cloned model.

Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        # Create input tensors if not provided
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    
    for original, cloned in zip(model._input_layers, input_tensors):
        layer_map[original] = cloned
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask
        
    for layer in model.layers:
        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer

    for node in model._nodes_by_depth:
        layer = node.outbound_layer

        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
            layer = new_layer
        else:
            layer = layer_map[layer]

        reference_input_tensors = node.input_tensors
        output_tensors = to_list(layer(reference_input_tensors))
        
        for x, y in zip(node.output_tensors, output_tensors):
            tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

With this corrected version, the `_clone_functional_model` function should now be able to correctly clone a functional model with multiple output layers. This fix ensures that the input layers are properly handled and mapped to their corresponding tensors in the new cloned model.