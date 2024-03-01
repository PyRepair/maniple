### Analysis:
- The buggy function `_clone_functional_model` is designed to clone a functional `Model` instance.
- The failing test is `test_clone_functional_model_with_multi_outputs` from `test_sequential_model.py`.
- The error message indicates that it fails to compute the output tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`.
- The corresponding GitHub issue points out an issue with `clone_model` and `output_masks` when using multi_gpu_model with cpu_relocation=True.

### Bug Cause:
- The bug occurs due to an issue in processing output masks when cloning a functional model with multiple outputs.
- Specifically, the bug lies in the handling of `output_masks` when calling `layer.compute_mask()` in the function `_clone_functional_model`.

### Bug Fix Strategy:
- Modify the logic for handling output masks to ensure correct processing when dealing with models and layers with multiple outputs.
- Update the `compute_mask` handling in the loop for each node's input tensors to properly set the `output_masks` for the subsequent calculations.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape[1:], dtype=layer.dtype, name=layer.name) for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)

    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = computed_masks if len(computed_data) > 1 else computed_masks[0]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

After applying this corrected version, the function `_clone_functional_model` should be able to clone a functional model with multiple outputs successfully, addressing the issue reported in the failing test and the GitHub issue.