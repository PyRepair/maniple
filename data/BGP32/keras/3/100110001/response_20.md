### Analysis:
1. The `__clone_functional_model` function is expected to clone a functional `Model` instance and create new layers (and new weights) instead of sharing existing ones.
2. The error occurs when trying to clone a `Model` instance that is actually a `Sequential` instance, leading to a `ValueError`.
3. The failing test `test_clone_functional_model_with_multi_outputs` creates a `Model` instance with multiple inputs and outputs, and then attempts to clone this model. The error message indicates that the `Model` being cloned contains a layer named `swap_layer_1`, which could not be computed.
4. The `_clone_functional_model` function fails to handle Sequential models correctly, as the function expects a `Model` instance and not a `Sequential` instance. The incorrect type check and handling of Sequential models is the cause of the bug.

### Bug Fix Strategy:
To fix the bug, we need to update the type check logic to correctly handle the case when a `Sequential` model is passed for cloning:
1. Modify the type check to exclude `Sequential` instances and only accept `Model` instances.
2. To handle cases where a Sequential model is passed, we can raise a specific error message indicating that only functional models can be cloned.
3. Additionally, update the logic to properly clone the layers and generate the new model with the correct input and output tensors.

### Corrected Version:
```python
from keras.engine import Model, Sequential, Input, InputLayer

def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got {}'.format(model))

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
    # Add handling for Sequential models
    elif isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead: {}'.format(model))
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    # Rest of the function remains the same

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)

``` 

By implementing this corrected version of the `_clone_functional_model` function, we handle the type check for `Sequential` models appropriately and provide an error message when trying to clone them. This update should resolve the issue with cloning functional models properly.