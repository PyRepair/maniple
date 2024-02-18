## Bug Cause:

The bug is caused by the incorrect computation of the output tensors and masks during the creation of a new model in the `_clone_functional_model` function. Specifically, the issue arises when a layer with multiple outputs and no mask support is encountered, leading to the error "Could not compute output Tensor".


## Fixing the Bug:

To fix the bug, we need to update the logic for computing the output tensors and masks where layers with multiple outputs and no mask support are encountered. We should handle the absence of masks correctly and ensure that the output masks are computed appropriately.


## Corrected Code:

```python
def _clone_functional_model(model, input_tensors=None):
    # ... (existing code)

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer.
            layer = node.outbound_layer

            # Get or create layer.
            if layer not in layer_map:
                # Clone layer.
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                # Reuse previously cloned layer.
                layer = layer_map[layer]
                # Don't call InputLayer multiple times.
                if isinstance(layer, InputLayer):
                    continue

            # Gather inputs to call the new layer.
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            # If all previous input tensors are available in tensor_map,
            # then call node.inbound_layer on them.
            computed_data = []  # List of tuples (input, mask).
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                # Call layer.
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                computed_tensors = [x[0] for x in computed_data]

                # Handle layers with multiple outputs and no mask support
                output_tensors = []
                output_masks = []
                for computed_tensor in computed_tensors:
                    if has_arg(layer.call, 'mask'):
                        if 'mask' not in kwargs:
                            kwargs['mask'] = None  # Handle absence of masks
                    output = layer(computed_tensor, **kwargs)
                    if isinstance(output, (list, tuple)):
                        output_tensors.extend(to_list(output))
                        output_masks.extend([None] * len(to_list(output)))
                    else:
                        output_tensors.append(output)
                        output_masks.append(None)

                # Update tensor_map.
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    # ... (existing code)
```

By making the above changes, we ensure that the computation of the output tensors and masks properly handles layers with multiple outputs and no mask support, resolving the issue reported on GitHub.