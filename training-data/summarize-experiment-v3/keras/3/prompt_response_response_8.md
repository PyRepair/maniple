## Bug's Cause

The bug is caused by the `_clone_functional_model` function not computing the output tensor correctly when creating a new model. This is specifically related to the issue with the script provided in the GitHub issue, where a Lambda layer with multiple outputs without mask support triggered the error.

## Fix for the Bug

To fix the bug, the function needs to be modified to handle layers with multiple outputs without mask support, such as the Lambda layer in the GitHub issue. One approach to fix this is to add a conditional check to handle the case when the `layer.compute_mask` returns `None` for layers that do not support masks. This will ensure that the output masks are correctly handled for layers with multiple outputs without mask support.

The correction also needs to ensure that the `output_tensors` and `output_masks` lists are correctly populated during the iteration over the reference model nodes.

## Corrected Code for the Buggy Function

```python
def _clone_functional_model(model, input_tensors=None):
    # ... (previous code)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer.
            layer = node.outbound_layer

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

            # Gather inputs to call the new layer.
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

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
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(layer.call, 'mask'):
                        if 'mask' not in kwargs:
                            kwargs['mask'] = computed_mask
                    output_tensors = to_list(
                        layer(computed_tensor, **kwargs))
                    if has_arg(layer.call, 'mask'):
                        output_masks = to_list(
                            layer.compute_mask(computed_tensor,
                                               computed_mask))
                    else:
                        output_masks = [None] * len(output_tensors)
                    computed_tensors = [computed_tensor]
                    computed_masks = [computed_mask]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    if has_arg(layer.call, 'mask'):
                        if 'mask' not in kwargs:
                            kwargs['mask'] = computed_masks
                    output_tensors = to_list(
                        layer(computed_tensors, **kwargs))
                    if has_arg(layer.call, 'mask'):
                        output_masks = to_list(
                            layer.compute_mask(computed_tensors,
                                               computed_masks))
                    else:
                        output_masks = [None] * len(output_tensors)
                # Update tensor_map.
                for x, y, mask in zip(reference_output_tensors,
                                      output_tensors,
                                      output_masks):
                    tensor_map[x] = (y, mask)

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected code now includes the conditional check for handling layers with multiple outputs without mask support, ensuring that the output masks are correctly handled during the iteration over the reference model nodes. This modification should resolve the issue reported in the GitHub bug.