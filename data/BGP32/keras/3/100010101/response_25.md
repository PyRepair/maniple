### Analysis
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and new weights. The error occurs when the function tries to retrieve the output tensor from the model but fails to find it in the `tensor_map`.

The expected behavior is that the function correctly clones the model by creating new layers and matching the input and output tensors accordingly.

### Bug
The bug lies in the incorrect handling of the `input_layers` variable when building the placeholders for input tensors. This leads to a mismatch between the created input tensors and the expected ones, causing the error when trying to compute the output tensors.

### Fix
To fix the bug, we need to correctly build the input tensors by adding them to the `input_tensors` list and the `input_layers` list. Additionally, we need to ensure that the `input_layers` are correctly mapped to the newly created input tensors in the `layer_map`.

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
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            input_layers.append(layer)
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    # Remaining code remains the same

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version ensures that the input tensors are correctly created and mapped to the input layers, resolving the error encountered during the test execution.