### Analysis:
1. The `clone_model` function is calling the `_clone_functional_model` internally, passing the model to be cloned as an argument.
2. The error occurs because the code is failing to compute the output tensor for a particular case with multiple outputs and Lambda layers.
3. The error message indicates that the function was not able to compute the output tensor for `"swap_layer_1/Identity:0"`.
4. The issue reported on GitHub describes a similar scenario, stating that the error occurs due to a mismatch in the expected output masks.
5. The function needs to be modified to handle cases where the output masks are `None`.

### Bug Cause:
The bug is caused by a mismatch in the expected output masks when dealing with multiple output layers and Lambda layers that do not support masks. The function is currently assuming that masks are always present, leading to an assertion error.

### Fix Strategy:
To fix the bug, we need to modify the code to handle cases where the output masks are `None`. This involves updating the logic related to checking and handling masks during the computation of output tensors.

### Corrected Function:
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
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_layer = Input(batch_shape=layer.batch_input_shape,
                                dtype=layer.dtype,
                                sparse=layer.sparse,
                                name=layer.name)
            input_tensors.append(input_layer)
            layer_map[layer] = input_layer
    else:
        input_tensors = to_list(input_tensors)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
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
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the function should now handle cases where output masks are `None` and successfully clone functional models with multiple outputs.