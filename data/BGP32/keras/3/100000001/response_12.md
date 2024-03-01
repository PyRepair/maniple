### Analysis:
The buggy function `_clone_functional_model` is intended to clone a functional Keras `Model` instance by creating new layers and new weights instead of sharing the existing ones. This function iterates over the layers of the original model, creates new instances of each layer, and builds a cloned model using newly instantiated layers.

### Bugs:
1. The function contains a logical error in the handling of input layers when `input_tensors` are provided. 
2. In the section where input tensors are processed, the function incorrectly populates `_input_tensors` instead of updating `input_tensors` with the new input tensors.

### Bug Cause:
The cause of the bug is that the function is not updating the `input_tensors` list with the newly created input tensors when `input_tensors` are provided as an argument. This results in incorrect use of input tensors while building the cloned model.

### Strategy for Fixing the Bug:
To fix the bug, the function needs to correctly update the `input_tensors` list with the new input tensors created when `input_tensors` are provided as an argument. This involves replacing `_input_tensors` with `input_tensors` in the relevant section of the function.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    # Function implementation
    ...
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_layers = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_layers.append(input_tensor)
            # Cache newly created input layer.
            layer_map[layer] = input_tensor

    else:
        # Make sure that all input tensors come from a Keras layer.
        # If tensor comes from an input layer: cache the input layer.
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                # Cache newly created input layer.
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer

    for _original, _cloned in zip(model._input_layers, input_tensors):
        layer_map[_original] = _cloned
    ...
```

In the corrected version, `input_tensors` list is properly updated with the new input tensors when `input_tensors` are provided, ensuring that the cloned model is built correctly using the new input tensors.