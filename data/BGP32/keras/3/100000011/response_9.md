### Analysis:
The GitHub issue highlights an error encountered when using `clone_model()` in Keras, specifically related to the `output_masks` being set to None due to a layer not supporting masks. This results in the script raising an `AssertionError` stating "Could not compute output Tensor".

### Potential Error Locations:
1. The computation of `output_masks` in the function `_clone_functional_model()` may be setting it to None when it should not be.
2. The handling of layers that do not support masks, as mentioned in the GitHub issue, may lead to unexpected behavior.

### Cause of the Bug:
The bug is caused by the `output_masks` being set to None when a layer does not support masks, leading to an error when computing the output tensors for the model.

### Strategy for Fixing the Bug:
To address this bug, we need to check if the layer supports masks before setting the `output_masks`. If the layer does not support masks, we should handle this scenario appropriately to avoid setting it to None.

### Corrected Version of the Function:
Here is the corrected version of the `_clone_functional_model()` function:

```python
def _clone_functional_model(model, input_tensors=None):
    # code removed for brevity
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # code removed for brevity

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

            # code removed for brevity

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
                if len(computed_data) == 1:
                    # code removed for brevity
                else:
                    # code removed for brevity

                # Update tensor_map.
                for x, y, mask in zip(reference_output_tensors,
                                      output_tensors,
                                      output_masks):
                    mask = None if mask is None else to_list(mask)  # Check and handle None masks
                    tensor_map[x] = (y, mask)  # Update tensor_map with computed outputs and masks
    
    # code removed for brevity
```

By adding the check and handling for `None` masks, we ensure that the `output_masks` are correctly set in the `tensor_map`, preventing the `AssertionError` from occurring when computing the output tensors.