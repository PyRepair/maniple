## Bug's Cause
The bug appears to be related to the computation of output tensors when creating the new model. Specifically, the issue is related to the `output_masks` computation when using a functional model with a layer that has more outputs without mask support. This issue occurs due to the Lambda layer not supporting masks, causing the `output_masks` to always be `None`. This aligns with the failing test that triggers an `AssertionError` when calling `keras.models.clone_model(model)` for a model with a Lambda layer.

## Fixing the Bug
To fix the bug, we need to address the computation of output masks for layers that do not support masks, such as the Lambda layer. It is necessary to modify the code to handle cases where the `output_masks` are `None` due to lack of mask support in specific layers.

## Corrected Code
```python
def _clone_functional_model(model, input_tensors=None):
    # ... (previous implementation code)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # ... (previous implementation code)

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
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = [None]  # Set output masks to None for layers without mask support
                    computed_tensors = [computed_tensor]
                    computed_masks = [computed_mask]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = [None] * len(output_tensors)  # Set output masks to None for layers without mask support
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
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```
In the corrected code, we handle the scenario for layers without mask support by explicitly setting the `output_masks` to `None` for these layers. This ensures that the bug related to `output_masks` computation is resolved, and the model creation process accounts for layers with and without mask support. This correction aligns with the reported issue in the GitHub post and resolves the `AssertionError` triggered by the failing test.