### Analysis:
1. **Error Message**:
   - The error message indicates an AssertionError stating that the output Tensor could not be computed.

2. **Expected Input/Output**:
   - The function `_clone_functional_model` is expected to clone a functional `Model` instance while creating new layers and weights.

3. **GitHub Issue**:
   - The issue on GitHub provides a detailed description of the problem, mentioning that the error occurs when using `clone_model()` in combination with `multi_gpu_model` and `cpu_relocation=True`.

### Bug Explanation:
- The function encounters an error when trying to compute the output tensor, likely due to issues with handling multiple outputs in a layer that does not support masks.

### Bug Location:
- The bug might be occurring in the section where output_masks are being computed.

### Bug Fix Strategy:
- Modify the code to handle scenarios where layers do not support masks and ensure that the output tensors are computed correctly.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors

            computed_data = [(tensor_map[x] if x in tensor_map else (x, None)) for x in reference_input_tensors]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]

    return Model(input_tensors, [tensor_map[x][0] for x in model.outputs], name=model.name)
```

By making these adjustments, the corrected function should handle the computation of output tensors correctly and avoid the AssertionError.