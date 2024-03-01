### Analysis:
The provided buggy function `_clone_functional_model` is used for cloning a functional model instance in Keras. The issue reported on GitHub mentions an error related to the `clone_model` function when using `cpu_relocation=True` parameter and a model with a Lambda layer that does not support masks. The cause of the bug seems to be related to the behavior of the `compute_mask` method when used with layers that do not support masks, resulting in `output_masks` being assigned to `None`.

### Identified Error Location:
Based on the provided buggy function and the GitHub issue, the potential error location in the function that causes the reported bug can be identified in the following lines:
```python
output_masks = to_list(
    layer.compute_mask(computed_tensors, computed_masks))
```

### Cause of the Bug:
1. The Lambda layer used in the model in the GitHub issue does not support masks, which results in the `output_masks` being set to `None`.
2. This condition causes an inconsistency in the expected output masks.
3. During the subsequent process, when the output tensors are being computed, the error message `Could not compute output Tensor` is raised due to the mismatch in masks.

### Strategy for Fixing the Bug:
To fix the bug and address the reported issue on GitHub:
1. Check if the layer supports masks before assigning output masks in the `output_masks` variable.
2. If the layer does not support mask, do not include it in the `output_masks` to avoid setting it to `None`.
3. Ensure that the output masks list matches the number of output tensors.

### Corrected Function:
Based on the analysis and the identified issue, here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    # Other parts of the function remain the same

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            # Code to clone layers remains the same

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []  # List of tuples (input, mask)
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                if layer.supports_masking:  # Check if layer supports masks
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                else:
                    output_masks = [None] * len(reference_output_tensors)  # Set masks to None if not supported

                # Call the layer and update tensor_map
                # Code for calling the layer remains the same

    # Check the computed model outputs and create a new model
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

Applying the fix above should address the issue reported on GitHub related to the `clone_model` function error when using the Lambda layer.