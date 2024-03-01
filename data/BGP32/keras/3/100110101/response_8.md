### Bug Explanation
The bug in the `_clone_functional_model` function arises from the way the input layers and input tensors are handled in the function. When the input tensors are provided to the function, it fails to correctly create the input layers and integrate them into the model, leading to a failure in computing the model outputs.

The error message indicates that the function failed to compute the output tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`. This failure stems from the incorrect handling of input layers and tensors in the function.

### Bug Fix Strategy
1. Ensure that the function correctly handles the input tensors provided to it to create the corresponding input layers.
2. Update the handling of input layers and input tensors to correctly map and use them during the model creation.

### The Corrected Version of the Function
Here is a corrected version of the `_clone_functional_model` function that addresses the bug:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

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
            layer_map[layer] = input_tensor
            input_layers.append(input_tensor) # Add the created input layer to input_layers for correct mapping
        
        for _original, _cloned in zip(model._input_layers, input_layers):
            layer_map[_original] = _cloned
    
    else:
        input_tensors = to_list(input_tensors)
        layer_inputs = model.inputs
        for x, layer_input in zip(input_tensors, layer_inputs):
            if not K.is_keras_tensor(x):
                shared_layer = layer_input._keras_history[0]
                input_layer = Input(tensor=x, name='input_wrapper_for_'+shared_layer.name)
                layer_map[shared_layer] = input_layer
            else:
                layer_map[layer_input] = x

    for orig_input, new_input in zip(model.inputs, input_tensors):
        tensor_map[orig_input] = (new_input, None)

    # Rest of the function remains the same...

```

By correctly handling the input layers and tensors provided to the function, the corrected version should now be able to accurately clone the functional model.