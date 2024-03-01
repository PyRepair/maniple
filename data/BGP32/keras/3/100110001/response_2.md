### Analysis:
The `_clone_functional_model` function is intended to clone a functional `Model` instance by creating new layers and new weights. The error message indicates that the failing test is attempting to clone a model using this function, but it is encountering an `AssertionError` stating that the output tensor could not be computed.

### Bug:
The bug lies in the handling of input layers and their associated tensors. When dealing with input tensors that are not provided explicitly, the function fails to properly map the input layers to newly created input tensors.

### Fix:
To address the bug, we need to ensure that the input layer and its associated tensor mapping are correctly handled. Specifically, when creating the input layers and their corresponding tensors, the mapping between the original input layer and the newly created input layer is crucial for further computations.

### Corrected Version:
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
            layer_map[layer] = input_tensor._keras_history[0]  # Update mapping correctly
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = model._input_layers[i]
                layer_map[original_input_layer] = input_tensor._keras_history[0]  # Update mapping correctly
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    # Rest of the function remains unchanged

    # Check that we did compute the model outputs, then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

By correctly updating the mapping between original input layers and newly created input tensors, the corrected function should now properly handle input layers when cloning a functional `Model` instance. This fix should resolve the `AssertionError` encountered in the failing test.