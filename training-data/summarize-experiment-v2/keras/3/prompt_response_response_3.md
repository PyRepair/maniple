The buggy function `_clone_functional_model` appears to be failing when attempting to clone a functional model with multiple outputs, especially when used with layers that do not support masks. This is evidenced by the failing test case `test_clone_functional_model_with_multi_outputs` and the error message `AssertionError: Could not compute output Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`.

The bug seems to be related to the computation of output masks for layers that do not support masks, leading to the inability to compute the output tensors correctly.

The potential error location within the function could be in the handling of output masks for layers that do not support masks, which leads to the error in computing the output tensors.

To fix this bug, the handling of layers that do not support masks needs to be improved. One approach could involve checking if the layer supports masks before attempting to compute them, and if the layer does not support masks, then directly proceeding with computing the output tensors without involving the masks.

Here is the corrected code for the problematic function:

```python
def _clone_functional_model(model, input_tensors=None):
    # ... (existing code)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterate over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # ... (existing code)

            # If all previous input tensors are available in tensor_map,
            # then call node.inbound_layer on them.
            
            # New code to handle layers without mask support
            if has_arg(layer.call, 'mask'):
                computed_data = []  # List of tuples (input, mask).
                for x in reference_input_tensors:
                    if x in tensor_map:
                        computed_data.append(tensor_map[x])

                if len(computed_data) == len(reference_input_tensors):
                    # ... (existing code)
            else:
                # Call layer without involving masks
                computed_data = []  # List of tuples (input, mask).
                for x in reference_input_tensors:
                    if x in tensor_map:
                        computed_data.append(tensor_map[x])

                if len(computed_data) == len(reference_input_tensors):
                    # Call layer without masks
                    if node.arguments:
                        kwargs = node.arguments
                    else:
                        kwargs = {}
                    # ... (existing code)

    # ... (existing code)
```

With this correction, the function should now be able to handle layers without mask support appropriately, and the failing test case should pass without raising the `AssertionError`.

Additionally, the suggested GitHub issue title "Could not compute output Tensor" and its detailed description properly convey the problem and its context, allowing for an informed discussion and potential solutions.