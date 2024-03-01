### Analysis:
The GitHub issue reported an error occurring when using `clone_model` with `multi_gpu_model` and `cpu_relocation=True`. The issue seems to be related to the `clone_model` function implementing the model cloning process. The error message indicates that the output tensor of the model could not be computed, leading to an `AssertionError`.

### Potential Error Locations:
1. Computing output tensors and masks in the cloning process.
2. Handling multiple outputs from a layer without mask support.

### Cause of the Bug:
The bug seems to stem from the `compute_mask` method returning `None` for output masks when using a layer without mask support (specifically, Lambda layer). This leads to the `output_masks` list containing only `None` elements, causing the subsequent failure when computing output tensors.

### Strategy for Fixing the Bug:
To fix the bug, we need to handle the case where layers do not support masks by adjusting how the `output_masks` list is generated in the cloning process. We may need to modify the logic to account for layers that do not produce masks.

### Corrected Version:
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
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
            input_layers.append(newly_created_input_layer)

        for original, cloned in zip(model._input_layers, input_layers):
            layer_map[original] = cloned

    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

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
                computed_tensors = [x[0] for x in computed_data]
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                else:
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for reference_output_tensor, output_tensor in zip(node.output_tensors, output_tensors):
                    tensor_map[reference_output_tensor] = (output_tensor, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

By adjusting how `output_masks` are handled and focusing on handling layers without mask support, this corrected version should address the issue reported on GitHub.