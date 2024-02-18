## Bug's Cause
The bug is caused by an issue in the computation of outputs when creating a new model through the `_clone_functional_model` function. Specifically, the error is related to the failure of computing the output tensor "swap_layer_1/Identity:0". This is due to the computation of the output masks at line 153 in the function. Additionally, the issue on GitHub clarifies that if a functional model contains a layer with multiple outputs and no mask support, the error can occur.

## Fixing the Bug
To fix the bug, we need to handle the case where a layer has multiple outputs without mask support. Additionally, we need to ensure that the output masks are appropriately computed for all layers. Finally, we need to update the `layer.compute_mask` function's behavior when dealing with multi-output layers without mask support.

## Corrected Code
```python
def _clone_functional_model(model, input_tensors=None):
    # ... existing code ...

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # ... existing code ...

            # If all previous input tensors are available in tensor_map,
            # then call node.inbound_layer on them.
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
                if has_arg(layer.call, 'mask'):
                    if len(computed_data) == 1:
                        computed_tensor, computed_mask = computed_data[0]
                        if has_arg(layer.call, 'mask') and computed_mask is not None:
                            kwargs['mask'] = computed_mask
                    else:
                        computed_tensors = [x[0] for x in computed_data]
                        computed_masks = [x[1] for x in computed_data]
                        if has_arg(layer.call, 'mask') and all(mask is not None for mask in computed_masks):
                            kwargs['mask'] = computed_masks
                output_tensors = to_list(layer(*computed_tensors, **kwargs))
                if has_arg(layer.call, 'mask'):
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                    # Update tensor_map.
                    for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                        tensor_map[x] = (y, mask)
                else:
                    # Update tensor_map without masks for layers lacking mask support.
                    for x, y in zip(reference_output_tensors, output_tensors):
                        tensor_map[x] = (y, None)

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```