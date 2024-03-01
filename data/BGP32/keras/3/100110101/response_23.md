### Issue Analysis
The error occurs in the `_clone_functional_model` function when trying to compute the output tensors. It fails to find a corresponding tensor in the `tensor_map` for one of the model's outputs (`Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`). This failure leads to the `AssertionError` as the model cannot be correctly cloned.

### Bug Cause
1. The `input_layers` list is created but not used for anything.
2. During the creation of `new_layer` if we encounter an existing layer, the function continues but doesn't update the `layer_map` with the reused layer.
3. If a tensor in the reference model's input tensors does not have a corresponding entry in the `tensor_map`, it will not compute the output tensors, leading to the failure.

### Bug Fix
1. Update the `input_layers` list when creating input tensors.
2. Update `layer_map` with reused layers during layer creation.
3. Handle the case where input tensors are missing from the `tensor_map` more gracefully.

### Corrected Code
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    input_layers = []

    if input_tensors is None:
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            input_layers.append(input_tensor._keras_history[0])
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                input_layers.append(input_tensor._keras_history[0])
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
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
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensor, computed_mask))
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        if x not in tensor_map:
            raise ValueError(f'Could not compute output {x}')
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

After making these updates to the function, the provided test case should pass without any `AssertionError`.