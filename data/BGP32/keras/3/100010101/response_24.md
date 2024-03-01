### Bug Analysis
The bug in the `_clone_functional_model` function arises from the incorrect handling of input tensors and the construction of the new model. Specifically, the function fails to properly handle the case where there are multiple outputs from a layer, resulting in an assertion error when verifying the computed output tensors.

1. The function incorrectly constructs the `input_layers` list, which remains empty, causing an issue in the subsequent loop.
2. The new cloned model is not being properly instantiated with input and output tensors, leading to the assertion error during the validation step.

### Bug Fix Strategy
To fix the bug in the function `_clone_functional_model`, we need to make sure that the new input layer is properly created and added to the `input_layers` list. Additionally, we should correctly construct the `output_tensors` list when instantiating the new model.

### Corrected Function
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    input_layers = []
    if input_tensors is None:
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_layers.append(input_tensor)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
            
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    output_tensors = []
    for node in model.outputs:
        if node in tensor_map:
            output_tensors.append(tensor_map[node][0])
        else:
            raise ValueError('Could not compute output ' + str(node))
    
    return Model(input_layers, output_tensors, name=model.name)
```

This corrected version of the function ensures that input layers are properly created and added to the `input_layers` list. Additionally, it correctly constructs the output tensors list for the new model instantiation. This should resolve the assertion error encountered during the failing test case.