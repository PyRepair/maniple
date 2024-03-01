### Analysis:
The error is occurring because the `assert` statement in the `_clone_functional_model` function is failing to find a computed output tensor in the `tensor_map`. This failure is causing the test to raise an `AssertionError` with the message `Could not compute output`.

The GitHub issue mentioned a scenario where multiple outputs were being used with a custom layer that doesn't support masks, causing `output_masks` to be set to `None`. This scenario is similar to the failing test case with multiple outputs, leading to the issue experienced by the user.

### Bug Cause:
1. The `assert` statement in the `_clone_functional_model` function is checking for every output tensor in the model, but due to the absence of proper handling for layers that don't support masks, the required tensor might not be present in the `tensor_map`.

### Strategy for fixing the bug:
1. Ensure that all output tensors are properly added to the `tensor_map`, even if the layer doesn't support masks.

### Corrected function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                         name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  
    
    for depth in reversed(range(len(model.layers))):
        layer = model.layers[depth]
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
        else:
            new_layer = layer_map[layer]

        input_tensors = [layer_map[node] for node in new_layer._inbound_nodes]

        output_tensors = new_layer(input_tensors)
        
        for x, y in zip(new_layer._outbound_nodes, output_tensors):
            tensor_map[x] = (y, None)

    output_tensors = model.outputs
    for x in output_tensors:
        assert x in tensor_map, 'Could not compute output ' + str(x)
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected function includes modifications to ensure that all output tensors are properly added to the `tensor_map` even when the layer doesn't support masks. This should resolve the issue with the failing test case and align with the scenario described in the GitHub issue.