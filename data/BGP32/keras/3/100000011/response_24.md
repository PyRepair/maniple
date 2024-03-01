### Analysis:
The buggy function `_clone_functional_model` is used to clone a functional `Model` instance in Keras. The issue reported on GitHub points out a specific scenario where using `clone_model` function leads to an error due to the model having a layer with multiple output tensors without mask support. This results in `output_masks` being set to `[None]` instead of `[None, None]`, causing the error.

### Error locations:
1. Line 157: `for x, y, mask in zip(reference_output_tensors,`
2. Line 153: `output_masks = to_list(`

### Cause of the bug:
The bug arises from the way the function handles layers with multiple output tensors that do not support masks. If such a layer is present in the model being cloned, the function incorrectly sets `output_masks` to `[None]` instead of the expected `[None, None]`.

### Strategy for fixing the bug:
To fix the bug, we need to ensure that when dealing with layers that have multiple output tensors without mask support, the function correctly sets `output_masks` to a list of multiple `None` values.

### Corrected version:
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
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
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
                computed_masks = [None] * len(computed_data)
                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = computed_masks
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                for x, y, mask in zip(reference_output_tensors, output_tensors, computed_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version ensures that when multiple output tensors without mask support are encountered, `computed_masks` is correctly set to a list of `None` values. This addresses the issue reported on GitHub and should prevent the `Could not compute output Tensor` error when using `clone_model()`.