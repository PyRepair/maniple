### Analysis:
1. The `assert x in tensor_map` error indicates that the function `_clone_functional_model` is unable to compute the output tensor during the cloning process.
2. The error message from the test points to an issue with a specific tensor, `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`, which is not found in the `tensor_map`.
3. The GitHub issue describes a similar problem where the `clone_model` function fails to compute the output tensor due to unavailability of masks from certain layers, particularly when using the `cpu_relocation=True` option.

### Bug Cause:
The bug arises when cloning a model with layers that don't support masks. The `compute_mask` method returns `None`, causing the `output_masks` to be empty, leading to missing entries in the `tensor_map`.

### Fix Strategy:
To fix the bug, we need to handle the case where layers don't support masks correctly. We can bypass the mask handling for layers without mask support.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}

    # Input handling
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    # Cloning model layers
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if has_arg(layer.call, 'mask') and any(mask is not None for _, mask in computed_data):
                    kwargs['mask'] = [mask for _, mask in computed_data if mask is not None]
                computed_tensors = [x[0] for x in computed_data]
                try:
                    output_tensors = layer(computed_tensors, **kwargs)
                except TypeError:  # Handle layers without mask support
                    output_tensors = layer(computed_tensors)
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    # Validate computed output tensors
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the `_clone_functional_model` function handles layers without mask support by attempting to call the layer with masks and falling back to calling without masks if an error occurs. This modification should resolve the issue and ensure that the output tensors are correctly computed during model cloning.