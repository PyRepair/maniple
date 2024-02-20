Based on the provided information, it appears that the bug in the `_clone_functional_model` function occurs when it attempts to compute the outputs of certain layers, specifically when using a functional model with a layer that has multiple outputs without mask support. This results in an `AssertionError` because the model could not compute the output tensor with a specific shape and data type.

To fix the bug, one approach is to check for the presence of masks in the layer and handle the computation of masks and output tensors appropriately. Additionally, it may be necessary to refactor the computation logic for such layers to ensure that the output tensors and masks are properly handled.

Here is the corrected code for the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    # ... (existing code)

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

            computed_data = []  # List of tuples (input, mask).
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]

                kwargs = node.arguments if node.arguments else {}
                if has_arg(layer.call, 'mask') and computed_masks:
                    kwargs['mask'] = computed_masks

                call_result = layer.call(computed_tensors, **kwargs)
                mask_result = layer.compute_mask(computed_tensors, computed_masks)

                if isinstance(call_result, list):
                    output_tensors = call_result
                    if mask_result:
                        output_masks = mask_result
                    else:
                        output_masks = [None] * len(output_tensors)
                else:
                    output_tensors = [call_result]
                    output_masks = [mask_result] if mask_result else [None]

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
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

In the corrected code, the logic for handling masks and output tensors has been revised to address the specific issue raised in the GitHub report. This includes properly handling the computation of masks, checking for their presence, and correctly setting the output tensors and masks based on the layer's behavior. This adjustment should ensure that the function can handle models with layers that have multiple outputs and mask support.