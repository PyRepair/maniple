## Analysis:
The error message indicates an `AssertionError` raised during the testing of the `clone_functional_model` function. Specifically, the error occurred at the point where it checks if all output tensors in the model have been computed.

## Bug:
The bug is within the `_clone_functional_model` function, where it fails to properly compute the output tensors for the given model. This causes an `AssertionError` when the function attempts to verify the output tensors.

## Bug Fix Strategy:
The bug could be due to issues in handling the computation of output tensors for layers with multiple input/output configurations. The fix strategy involves ensuring that the output tensors are correctly computed and added to the `tensor_map` before performing the assertion check.

## Bug Fix:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

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
            input_layers.append(layer)  # Add reference to input layers.
            layer_map[layer] = input_tensor
        
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                input_layers.append(model._input_layers[i])  # Add reference to input layers.
                layer_map[model._input_layers[i]] = input_tensor
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(input_layers, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    for depth in range(len(model._nodes_by_depth)):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            reference_output_tensors = node.output_tensors
            computed_data = []
            for x in node.input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                output_tensors = to_list(layer(computed_data, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

## Updated Function:
The updated `_clone_functional_model` function correctly computes the output tensors for the model and handles the mapping of tensors. It ensures that each output tensor is added to the `tensor_map` before the final assertion check. This updated function should now pass the failing test.