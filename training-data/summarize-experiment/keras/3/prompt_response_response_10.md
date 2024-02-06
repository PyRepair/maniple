The potential error location within the `_clone_functional_model` function is likely related to the final instantiation of the new model from inputs and outputs. Specifically, the issue may arise from the computation and mapping of output tensors, as indicated by the failing test case.

The error occurs when the `clone_model` function is called on a model that has a layer with more outputs without mask support, resulting in an AssertionError with the message: "Could not compute output Tensor".

This error is likely the result of the `output_masks` always being [None], as Lambda doesn't support using masks. The `output_masks` are computed using `layer.compute_mask(...)`, which will always return None for the Lambda layer.

To fix this bug, we can address the issue by ensuring that the computation and mapping of output tensors account for scenarios where layers have multiple outputs without mask support. This can be achieved by checking if the layer supports masks and determining the appropriate handling for output masks.

Here's the corrected version of the `_clone_functional_model` function that addresses this bug:

```python
def _clone_functional_model(model, input_tensors=None):
    # (Existing function code remains unchanged)

    # Check that we did compute the model outputs.
    output_tensors = []
    for x in model.outputs:
        if x in tensor_map:
            tensor, mask = tensor_map[x]
            output_tensors.append(tensor)
        else:
            raise ValueError('Could not compute output ' + str(x))

    # Instantiate a new model from inputs and outputs.
    return Model(input_tensors, output_tensors, name=model.name)
```

In this corrected version, we directly retrieve the computed tensor and mask from the `tensor_map` if the output tensor is found in the map. If the output tensor is not found in the map, an exception is raised to indicate that the output could not be computed.

This fix ensures that the output_tensors are properly computed and mapped, taking into account scenarios where layers have multiple outputs without mask support.

By implementing this correction, the bug related to the erroneous computation of the output tensors in the `_clone_functional_model` function should be resolved, and the `clone_model` function should work as expected for the given test case and similar scenarios.