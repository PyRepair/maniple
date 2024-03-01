### Analysis:
The provided GitHub issue indicates that there is an issue with the `clone_model` function in Keras when using it with `multi_gpu_model` and `cpu_relocation=True`. The error message mentioned in the issue indicates that there is an assertion error related to computing the output tensor.

### Potential Error Locations:
1. Line 157: The assertion error occurs during the loop over `reference_output_tensors`.
2. Line 153: The issue points out that `output_masks` will always be `[None]`, which can cause problems in computing the output tensors.

### Cause of the Bug:
The bug seems to stem from the computation of `output_masks` where Lambda layers do not support masks, causing them to return `None`. This behavior leads to an incorrect number of output masks being generated, resulting in the assertion error when computing the final output tensors.

### Strategy for Fixing the Bug:
To fix the bug, we need to handle the case where a layer does not support masks, ensuring that the output masks are generated correctly even if they are not supported by the layer type encountered during cloning.

### Corrected Version:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        input_tensors = []
        for _original in model.inputs:
            input_tensor = Input(batch_shape=_original._keras_shape,
                                 dtype=_original.dtype,
                                 sparse=_original._sparse,
                                 name=_original.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            newly_created_input_layer = input_tensor
            layer_map[_original] = newly_created_input_layer
    else:
        input_tensors = [Input(tensor=x) if not K.is_keras_tensor(x) else x for x in input_tensors]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in range(len(model._nodes_by_depth) - 1, -1, -1):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                tensor_map.update({x: (y, None) for x, y in zip(node.output_tensors, output_tensors})

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version addresses the issue by ensuring that the output masks are handled correctly, even when they are not supported by certain layers like Lambda layers.