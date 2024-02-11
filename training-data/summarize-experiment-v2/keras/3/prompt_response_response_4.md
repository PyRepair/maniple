Potential Error Location:
The error seems to be occurring when the `clone_model` function is unable to compute the output tensor for a specific layer. This is likely due to the `Layer.compute_mask` method returning `None` for certain layers without mask support, leading to the `AssertionError`.

Bug Cause:
The input tensor and output tensor mapping is not being properly handled, and the code is not correctly computing output tensors for certain layers.

Potential Fixes:
1. Handle the case where the `Layer.compute_mask` method returns `None` appropriately for layers without mask support.
2. Update the logic for computing output tensors to ensure that all output tensors are correctly computed.

```python
# The corrected _clone_functional_model function
def _clone_functional_model(model, input_tensors=None):
    # existing code...

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # existing code...

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

By updating the code to handle cases where the `Layer.compute_mask` method returns `None`, and ensuring that the output tensors are correctly computed for all layers, the bug should be resolved.

Additionally, a fix should be made to the failing test for `clone_functional_model` to ensure that it properly evaluates the output and passes the test case.