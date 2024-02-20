## Bug Cause

The bug is caused by the incorrect handling of multi-output layers without mask support in the `_clone_functional_model` method, leading to the program not being able to compute the output tensors when using `clone_model()`. This issue is reported in the GitHub issue, confirming that the error occurs when using a model with a layer that has more outputs without mask support, causing the error to appear.

The error message line: `assert x in tensor_map, 'Could not compute output ' + str(x)` at line 166 in the `_clone_functional_model` method indicates that the output tensors cannot be computed properly, leading to the `AssertionError` being triggered.

## Fix

To fix the bug, the `_clone_functional_model` method needs to be modified to correctly handle multi-output layers without mask support. The code can be updated to make sure that `layer.compute_mask` does not always return `None` and that the multi-output layers are properly handled during the cloning process.

A possible approach to fix the bug is to modify the `_clone_functional_model` method to handle multi-output layers that do not support masks in a way that ensures the proper computation of output tensors. This may involve implementing a custom solution to handle the multi-output layers without mask support.

## Corrected Code

```python
def _clone_functional_model(model, input_tensors=None):
    # ... (existing code)

    # Check if the layer supports masks
    layer_supports_mask = hasattr(layer, 'compute_mask')

    # If the layer supports masks or is a multi-output layer
    if layer_supports_mask or len(reference_output_tensors) > 1:
        output_masks = []  # Initialize the output_masks list
        for ref_output_tensor in reference_output_tensors:
            if layer_supports_mask:
                # Use layer.compute_mask if available
                output_masks.append(layer.compute_mask(ref_output_tensor, None))
            else:
                # For multi-output layers without mask support, set mask to None
                output_masks.append(None)
    else:
        # If the layer does not support masks and outputs a single tensor
        output_masks = None

    # ... (existing code)

    # Update tensor_map.
    for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
        tensor_map[x] = (y, mask)

    # ... (existing code)
```

In the corrected code, the `_clone_functional_model` method has been modified to handle the computation of output masks for multi-output layers without mask support. This includes checking if the layer supports masks, handling multiple outputs, and ensuring proper handling of the mask computation. The code now correctly handles the scenario described in the GitHub issue and should resolve the reported bug.