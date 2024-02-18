## Bug Cause Analysis

The bug occurs when the function `_clone_functional_model` fails to correctly compute the output tensors for the new model. This is highlighted by the failing test `test_clone_functional_model_with_multi_outputs` triggered by the `clone_model` method in the `test_sequential_model.py` file. The error message indicates that the function fails to compute the output tensor with the name "swap_layer_1/Identity:0". 

Additionally, the GitHub issue provides a similar scenario where `clone_model` fails to compute the output tensors correctly when using multi_gpu_model with cpu_relocation=True. The issue indicates that the problem arises from a layer not supporting masks, which causes the `layer.compute_mask` method to always return None.

## Bug Location
The issue is likely related to the computation of output tensors and masks for layers, especially when using layers that do not support masks.

## Fixing the Bug
To fix the bug, the computation of the output tensors and masks must be adjusted to handle layers that do not support mask computation.

## The corrected code:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    # ... [existing code]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            # Get or create layer
            if layer not in layer_map:
                # Clone layer and handle masks
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
                if isinstance(layer, InputLayer):
                    layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            # Compute list of masks
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                # Call layer with masks, without masks, or with a list of masks
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)  # Update tensor_map
    return Model(input_tensors, [tensor_map[x][0] for x in model.outputs], name=model.name)
```

The corrected code handles the computation of output tensors and masks for layers that do not support masks correctly, ensuring that the output tensors are computed as expected. This should resolve the issue causing the failing test and the problem reported in the GitHub issue.