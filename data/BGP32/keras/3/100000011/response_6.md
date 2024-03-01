### Analysis:
- The provided function `_clone_functional_model` is responsible for cloning a functional `Model` instance in Keras.
- The GitHub issue reported an error related to the usage of `clone_model()` when using `multi_gpu_model` with `cpu_relocation=True`.
- The error originates from the fact that `output_masks` may be `None` when a layer with more outputs without mask support is used.
- This is due to the fact that the `Lambda` layer does not support masks, leading to `output_masks` being set to `None`.

### Error Locations:
1. Line 153: `output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))` - The issue of `output_masks` potentially being `None` originates from here.
2. Line 157: `for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):` - This loop may break if `output_masks` are `None`.

### Bug Cause:
The bug is caused by the usage of a layer (`Lambda`) without mask support, leading to unexpected behavior in the computation of output masks in the cloning process.

### Strategy for Fixing the Bug:
To fix the bug, we need to handle the case where `output_masks` may be `None` due to layers without mask support. We can modify the way output masks are computed in such scenarios to ensure smooth cloning of the model.

### Corrected Version of the Function:

```python
# The corrected version of the function
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    in_layers = []
    tensor_map = {}
    if input_tensors is None:
        # Create placeholders to build the model upon.
        input_layers = []
        input_tensors = []
        for in_layer in model.inputs:
            input_layer = Input(batch_shape=in_layer.shape, dtype=in_layer.dtype)
            input_tensors.append(input_layer)
            in_layers.append(in_layer)
            layer_map[in_layer] = input_layer
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = in_layers[i].name
                input_layer = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_layer
                layer_map[in_layers[i]] = input_layer

    for in_x, in_y in zip(model.inputs, input_tensors):
        tensor_map[in_x] = (in_y, None)

    depth_keys = sorted(model._nodes_by_depth.keys(), reverse=True)
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

            reference_input_tensors = node.input_tensors
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for out_x in model.outputs:
        assert out_x in tensor_map, 'Could not compute output ' + str(out_x)
        tensor, _ = tensor_map[out_x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the function addresses the issue of `output_masks` potentially being `None` by simplifying the handling of masks and ensuring the smooth cloning of the functional model.