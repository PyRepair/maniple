The bug in the `_clone_functional_model` function arises from incorrect handling of `Sequential` models, which are subclassed from the general `Model` class. The function checks for `Sequential` instances, resulting in an incorrect error message when a `Sequential` model is passed. To correct this issue, the function needs to be updated to properly handle `Sequential` models.

### Bug Explanation:
1. The function `_clone_functional_model` raises an error if the input model is an instance of `Sequential`, which is an incorrect check since `Sequential` models are subclasses of `Model` and thus should not trigger this specific error.
2. Due to this incorrect check, when the test calls `clone_model(model)`, it triggers the error message `Expected 'model' argument to be a functional 'Model' instance, got a 'Sequential' instance instead:` during the creation of the new model.
3. The expected model output tensors are not computed correctly due to the erroneous handling of Sequential models in the function.

### Fix Strategy:
1. Update the validation of the input model to consider `Sequential` models as valid instances of `Model`.
2. Ensure the correct construction of the output model by adjusting how the layers are cloned and managed within the function.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
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

    ...
    # The remaining part of the function remains the same
```

By updating the `_clone_functional_model` function as outlined above, it will correctly handle `Sequential` models and avoid the previous error scenario in the test code.