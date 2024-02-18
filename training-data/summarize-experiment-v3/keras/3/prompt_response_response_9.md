The potential error in the `_clone_functional_model` function is related to the computation of the output tensors. The failing test `test_clone_functional_model_with_multi_outputs` is triggering an `AssertionError` when calling `keras.models.clone_model(model)`, indicating an issue with computing the output tensor "swap_layer_1/Identity:0". The GitHub issue also mentions a similar error related to the `clone_model` function and the computation of output tensors, particularly when using a functional model with a layer that has multiple outputs without mask support.

To fix the bug, we need to ensure that the computation of output tensors and masks is handled correctly, especially for layers with multiple outputs and layers without mask support.

Here's the corrected code for the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    # ... (previous code remains the same) ...

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
            all_tensors_found = True
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
                else:
                    all_tensors_found = False
                    break

            if all_tensors_found:
                computed_tensors, computed_masks = K.layer_utils.get_compute_mode(
                    layer, reference_input_tensors, tensor_map, node)

                # Update tensor_map.
                for x, y, mask in zip(reference_output_tensors, computed_tensors, computed_masks):
                    tensor_map[x] = (y, mask)

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        if x in tensor_map:
            tensor, mask = tensor_map[x]
            output_tensors.append(tensor)
        else:
            raise AssertionError('Could not compute output ' + str(x))
    return Model(input_tensors, output_tensors, name=model.name)
```

In the updated code:
1. The `get_compute_mode` function from `K.layer_utils` is used to handle the computation of output tensors and masks for each layer, ensuring that all input tensors are found in the `tensor_map` before performing the computation.
2. If any output tensor is not found in the `tensor_map`, an `AssertionError` is raised to indicate that the output tensor could not be computed.

These changes address the bug and should resolve the issue reported in the GitHub thread.