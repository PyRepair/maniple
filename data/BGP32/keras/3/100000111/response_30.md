### Analysis:
The bug in the `_clone_functional_model` function occurs because the `output_masks` variable will always be `[None]` due to the behavior of layers without mask support like `Lambda` layers. This causes an issue when trying to compute the output of the model, resulting in the error described in the GitHub issue.

### Bug Cause:
The bug arises from the incorrect handling of layers that do not support masks, leading to the `output_masks` variable always being `[None]`. This inconsistency in the expected output structure causes the function to fail when computing the output tensors.

### Proposed Fix:
To fix the bug, we need to modify the logic related to handling layers without mask support to ensure that the `output_masks` variable reflects the correct structure. We can update the code to handle the case where mask support is not available more robustly.

### Corrected Function:
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
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[x._keras_history[0]] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

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
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                arg_len = len(computed_data)
                if arg_len == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    new_output_masks = [None for _ in range(len(output_tensors))]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    new_output_masks = [None for _ in range(len(output_tensors))]

                for x, y, mask in zip(node.output_tensors, output_tensors, new_output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected function now properly handles layers without mask support and ensures that the `output_masks` are correctly initialized, addressing the issue described in the GitHub report.