### Bug Analysis:
The bug arises from the `clone_model` function failing the test case, specifically due to an `AssertionError` when checking the computation of the output tensor.

1. **Error Cause:** The error occurs because the function fails to compute the output tensor for the `SwapLayer` object in the model, resulting in the assertion failure.

2. **Buggy Code Explanation:**
   - The `for x in model.outputs` loop fails to compute the output tensors properly due to incorrect mapping or missing entries in the `tensor_map`.
   - When trying to compute the output tensor "Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)", the function is unable to find this tensor in the `tensor_map`, leading to the assertion failure.

### Bug Fix Strategy:
To fix this bug, we need to ensure that all output tensors are correctly computed and present in the `tensor_map`. We can modify the computation logic and the mapping process in the function to address this issue.

### Corrected Function:

Here is the corrected version of the `_clone_functional_model` function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.input_shape[1:]) for layer in model._input_layers]
    else:
        input_tensors = to_list(input_tensors)

    for original_input, input_tensor in zip(model._input_layers, input_tensors):
        layer_map[original_input] = input_tensor
        tensor_map[original_input.output] = input_tensor

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            inbound_tensors = [tensor_map[x] for x in node.input_tensors]
            kwargs = node.arguments or {}
            layer = node.outbound_layer

            if len(inbound_tensors) == 1:
                computed_data = [(inbound_tensors[0], None)]
            else:
                computed_data = [(x, None) for x in inbound_tensors]

            if all(x in tensor_map for x in node.input_tensors):
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(layer(inbound_tensors, **kwargs))
                tensor_map.update(zip(node.output_tensors, output_tensors))

    output_tensors = [tensor_map[x] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By addressing the logic for computing output tensors based on the input tensors and node connections, we can ensure that the function correctly clones the given functional model. This corrected version should now pass the failing test case.