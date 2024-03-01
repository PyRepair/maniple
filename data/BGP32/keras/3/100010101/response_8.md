### Bug Analysis:
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones. The function iterates through the nodes in the model based on depth, clones layers, and builds a new model using new input and output tensors. The error occurs when the function fails to compute the output tensors properly.

The error message indicates that the function failed to compute output `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)` during the execution of the test case `test_clone_functional_model_with_multi_outputs`.

### Bug Location:
The issue arises primarily in the part of the function where it builds the new model by iterating through nodes and cloning layers. It fails to correctly compute the output tensors and does not handle the case when the computed data for a particular layer is not complete.

### Bug Cause:
1. The function fails to properly handle cases where the computed data for a layer is incomplete, leading to the assertion error when checking if all output tensors have been computed.
2. Incorrect handling of multiple inputs and outputs in layers may result in missing output tensors in the tensor map, causing the function to fail when computing the model outputs.

### Bug Fix Strategy:
To fix the bug in the `_clone_functional_model` function:
1. Ensure that all computed data is complete before attempting to call a layer, especially when dealing with multiple inputs and outputs.
2. Check the correctness of the logic for gathering inputs and calling new layers in the function.
3. Properly update the `tensor_map` with output tensors for each node in the model.

### Corrected Code:
```python
def _clone_functional_model(model, input_tensors=None):
    # Existing code...
    # Remaining code from the function...

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        if x not in tensor_map:
            raise RuntimeError('Could not compute output ', x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model([tensor_map.get(x, x) for x in model.inputs], output_tensors, name=model.name)
```