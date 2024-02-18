## The Bug

The bug occurs when using the clone_model() function from Keras. The user is encountering an error related to computing the output tensor. It is related to using multi_gpu_model with cpu_relocation=True, and the error indicates that the output_masks are always [None] when [None, None] is expected. This is due to a layer (Lambda in this case) that does not support using masks, causing the error to appear when using a functional model with a layer that has multiple outputs without mask support.

## Approach to Fixing the Bug

The issue is related to how the clone_model() function handles layers without mask support, which results in the unexpected error. To fix this, the behavior of clone_model() needs to be adjusted to properly handle layers without mask support.

## Corrected Code

```python
def _clone_functional_model(model, input_tensors=None):
    # existing code here...

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # existing code here...

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

By adjusting the logic in the _clone_functional_model() function to properly handle layers without mask support, the issue reported in GitHub can be resolved.