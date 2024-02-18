## Bug Cause

The bug occurs in the `_clone_functional_model` function when it fails to compute the output tensor for a specific tensor named "swap_layer_1/Identity:0". This issue is related to the computation of outputs for a new model created during the cloning process.

## Fixing the Bug

To resolve this bug, we need to update the computation of the output tensors in the `_clone_functional_model` function. Specifically, we need to ensure that the output tensors are correctly computed for the new model being created. Additionally, we need to consider cases where the layers do not support masks.

Here's the corrected code for the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    # existing code...

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterate over every node in the reference model, in depth order.
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
                output_tensors = []
                output_masks = []
                for x, mask in zip(reference_input_tensors, [None] * len(reference_input_tensors)):
                    if x in tensor_map:
                        computed_tensor, _ = tensor_map[x]
                        computed_outputs = to_list(layer(computed_tensor, **kwargs))
                        output_tensors.extend(computed_outputs)
                        output_masks.extend([layer.compute_mask(computed_tensor, None)] * len(computed_outputs))

                # Update tensor_map.
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

This fix ensures that the output tensors are correctly computed for the new model being created, taking into account cases where the layers do not support masks.

By implementing this fix, the failing test `test_clone_functional_model_with_multi_outputs` should pass, and the corresponding issue on GitHub related to the bug will also be resolved.