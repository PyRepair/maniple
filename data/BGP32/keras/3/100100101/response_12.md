The bug in the `_clone_functional_model` function is related to the incorrect handling of mapping input tensors when creating a clone of a functional model. The function fails to properly handle the input tensors and their mapping, resulting in incorrect behavior and failing the test case.

### Bug Explanation:
- The function fails to properly create input tensors when they are not provided as input. 
- When input tensors are not provided, the function creates a new input tensor based on the properties of the original model's input layers. However, it fails to add these newly created input layers to the `input_layers` list, leading to a mismatch in the subsequent steps of the function.
- This results in incorrect mapping of input tensors and missing input layers in the final model, causing the test case to fail.

### Fix Strategy:
1. Ensure that newly created input layers are added to the `input_layers` list to maintain consistency.
2. Correct the mapping of input tensors and handle the creation of placeholders if input tensors are not provided.

### Corrected Function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  

    # Create placeholders if input tensors are not provided
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for i, layer in enumerate(model._input_layers):
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            input_layers.append(input_tensor)  # Add the newly created input layer
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    # Code for node traversal and creating the model as before

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

With these changes, the function should now correctly handle the mapping of input tensors, create placeholders when needed, and build the clone of the functional model as expected. This corrected version should pass the failing test case.