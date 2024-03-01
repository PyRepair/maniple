### Bug Analysis:
1. The error message "Could not compute output Tensor" is triggered because the function fails to properly compute the output tensors while cloning a functional model.
2. The issue arises when the function encounters a Lambda layer that has multiple outputs without mask support. This results in the output_masks list being filled with None values, leading to the error.
3. The function should handle such cases where layers do not support masks correctly to prevent the error during output computation.

### Bug Fix Strategy:
1. Modify the function to check if the output_mask is None and handle it appropriately to ensure that the list contains the correct values.
2. Update the logic for handling output tensors and masks when multiple outputs are involved without mask support to avoid the error.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    if input_tensors is None:
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[input_tensors[i]] = input_tensor
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
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
                computed_tensors = [data[0] for data in computed_data]
                computed_masks = [data[1] for data in computed_data]
                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = computed_masks if any(mask is not None for mask in computed_masks) else None
                output_tensors = to_list(layer(computed_tensors, **kwargs))

                for i, x in enumerate(node.output_tensors):
                    tensor_map[x] = (output_tensors[i], None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected function addresses the issue of handling output_masks when computing the output tensors for the cloned functional model. This should resolve the error message encountered during the test.