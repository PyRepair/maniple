### Analysis:
1. The `clone_model` function is encountering an issue when dealing with a functional model containing layers without mask support, specifically in the case of multiple outputs from a layer without mask support.
2. The test function provided demonstrates the failure scenario where `clone_model` fails to handle a model with multiple output tensors.
3. The issue reported on GitHub points out the error scenario and provides a script to reproduce the error, highlighting the need for handling cases where layers do not support masks correctly.
4. The primary cause of the bug is the improper handling of layers without mask support, leading to the `Could not compute output Tensor` error during the cloning process.
  
### Bug Fix Strategy:
1. Update the code to properly handle layers without mask support when cloning the functional model.
2. Modify the logic to ensure that the model can handle multiple outputs and correctly initialize the output masks.

### Bug Fix:
```python
def _clone_functional_model(model, input_tensors=None):
    ...
    # Snippet of the corrected code
    output_tensors = to_list(layer((computed_tensor, *computed_tensors[1:]), **kwargs))
    if not isinstance(output_tensors, list):
        output_tensors = [output_tensors]
    output_masks = [None] * len(output_tensors)

    tensor_map[x] = (y, output_masks[0])  # Update tensor_map

# Check that we did compute the model outputs,
# then instantiate a new model from inputs and outputs.
output_tensors = []
for x in model.outputs:
    assert x in tensor_map, 'Could not compute output ' + str(x)
    tensor, mask = tensor_map[x]
    output_tensors.append(tensor)
...
```

This fix ensures that the model correctly handles multiple outputs and their associated masks when cloning a functional model, addressing the issue raised in the failing test and the GitHub report.