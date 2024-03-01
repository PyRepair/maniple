### Analysis:
1. The `clone_model` function is trying to create a clone of a model by calling the `_clone_functional_model` function.
2. The error message indicates that the assertion `assert x in tensor_map` is failing because the tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)` is not found in the `tensor_map`.
3. The issue on GitHub also highlights a similar problem where the `compute_mask` function inside the `layer` is returning `None` and causing issues with multi-output layers.
4. The problem arises when dealing with layers that do not support masks, and the `clone_model` function does not handle this scenario properly.

### Bug Cause:
The bug is caused by the failure to handle layers that do not support masks correctly when cloning a functional model.

### Solution:
To fix the bug, we need to modify the `_clone_functional_model` function to address the issue of missing masks for layers that do not support them.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    ...
    
    output_tensors = []
    output_masks = [] # New list to store masks
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x] # Retrieve the corresponding mask as well
        output_tensors.append(tensor)
        output_masks.append(mask) # Append the mask to the list

    return Model(input_tensors, output_tensors, name=model.name, output_masks=output_masks)
```

By updating the `_clone_functional_model` function to handle output masks as well, we ensure that the cloned model can correctly handle layers that do not support masks.

This correction should resolve the issue and allow the test case `test_clone_functional_model_with_multi_outputs` to run successfully.