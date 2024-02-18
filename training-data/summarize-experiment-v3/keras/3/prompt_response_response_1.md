## Bug Cause

The bug is caused by the inability of the `_clone_functional_model` function to properly compute the output tensors, especially when dealing with layers that have multiple outputs without mask support. This issue is apparent from the failing test case `test_clone_functional_model_with_multi_outputs`, which triggers an `AssertionError` when attempting to compute the output tensor "swap_layer_1/Identity:0". The function fails to properly handle the computation of output tensors in such cases, leading to the error.

## Fixing the Bug

To fix the bug, the function `_clone_functional_model` needs to be updated to properly handle layers with multiple outputs and without mask support. This can be achieved by modifying the logic for computing the output tensors and handling the lack of mask support in certain layers.

## The corrected code for the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    # [Previous code...]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

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

            # Get the output tensors of the layer
            computed_tensors = layer(reference_input_tensors)

            # Update tensor_map.
            for x, y in zip(node.output_tensors, computed_tensors):
                tensor_map[x] = (y, None)  # tensor, mask

    # Create a list of output tensors for the new model
    output_tensors = [tensor_map[x][0] for x in model.outputs]

    return Model(input_tensors, output_tensors, name=model.name)
```

With this corrected code, the function properly computes the output tensors for the new model, handling layers with multiple outputs and without mask support.

By implementing these changes, the issue mentioned in the GitHub report should be resolved, and the failing test case `test_clone_functional_model_with_multi_outputs` should pass successfully.