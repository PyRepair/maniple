Based on the provided test case, failing test, and GitHub issue, it seems that the bug occurs when handling multiple output tensors in the `_clone_functional_model` function. The error message "Could not compute output Tensor" indicates that there is an issue with computing the output tensors, specifically when there are multiple output tensors involved.

It is mentioned in the GitHub issue that the problem arises when using a functional model with a layer that has multiple outputs without mask support, leading to the error.

Approaches for fixing the bug:
1. Ensure that the function properly handles the case of multiple output tensors without mask support.
2. Modify the computation of output tensors and output masks to handle cases where there are multiple outputs without mask support.

Based on these insights, here is the corrected code for the buggy function:

```python
def _clone_functional_model(model, input_tensors=None):
    # ... (rest of the function remains the same)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterate over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # ... (rest of the code remains the same)

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
                computed_tensors = [x[0] for x in computed_data]
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                computed_output = layer.call(computed_tensors, **kwargs)
                if isinstance(computed_output, list):
                    output_tensors = to_list(computed_output)
                else:
                    output_tensors = [computed_output]
                # Update tensor_map.
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

In the corrected code, the handling of multiple output tensors without mask support has been improved to ensure proper computation of the output tensors and updating the `tensor_map` accordingly. This should address the issue reported in the failing test and the GitHub issue.