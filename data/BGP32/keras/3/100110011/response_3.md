### Potential Error Locations:
1. The check for the input model type not being a `Model` instance might be causing issues.
2. The handling of input tensor creation and mapping could be incorrect.
3. The iteration over nodes in the model might be problematic.
4. The update of the `tensor_map` and validation of computed model outputs seems to be leading to the error.

### Bug Cause:
The bug occurs due to the incorrect handling of input tensors and their mapping in the `_clone_functional_model` function. The error message shows that the output tensor of the `SwapLayer` is not computed, leading to an assertion failure. The issue reported on GitHub provides a similar case using a `Lambda` layer, which might not support masks, resulting in None values.

### Strategy for Fixing the Bug:
1. Check the input model type more accurately.
2. Ensure correct creation and mapping of input tensors.
3. Verify the iteration over nodes and layers in the model.
4. Update the `tensor_map` correctly and validate the computed model outputs.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(shape=layer.input_shape) for layer in model.layers if layer.__class__.__name__ == "InputLayer"]
    else:
        input_tensors = to_list(input_tensors)

    for i, x in enumerate(input_tensors):
        if not K.is_keras_tensor(x):
            name = model.layers[i].name
            input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
            input_tensors[i] = input_tensor
            layer_map[model.layers[i]] = input_tensor
            tensor_map[x] = (input_tensor, None)

    for layer in model.layers:
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer

        for node in layer._inbound_nodes:
            inbound_layers = [input_layer.output for input_layer in node.inbound_layers]
            inbound_tensors = [tensor_map[tensor][0] for tensor in inbound_layers]
            kwargs = {'training': True} if has_arg(layer.call, 'training') else {}
            output_tensors = layer(inbound_tensors, **kwargs)

            for x, y in zip(node.input_tensors, output_tensors):
                tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version addresses the issues related to input tensor creation, mapping, and handling of model layers and nodes. It should now be able to correctly clone a functional model instance.