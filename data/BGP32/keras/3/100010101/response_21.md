### Bug Explanation:
1. The bug occurs because the function is checking if the input `model` is an instance of `Model` correctly, but it incorrectly raises an error if the input is an instance of `Sequential`.
2. The bug stems from the incorrect condition checking at line 32. If the input `model` is of type `Sequential`, it should not raise an error but treat it as a functional model.
3. Furthermore, at line 164, it is assumed that all reference output tensors are available in `tensor_map`, leading to the AssertionError at line 166 if this assumption is not met.

### Bug Fix Strategy:
1. Update the condition at line 32 to correctly handle the case when `model` is an instance of `Sequential`.
2. Check and update the code at line 164 to handle the scenario where some reference output tensors are not available in `tensor_map`.

### The corrected function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got {}'.format(model))

    # Handles the case where input is of type Sequential
    if isinstance(model, Sequential):
        model = Model(inputs=model.inputs, outputs=model.outputs)
    
    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
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
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
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
            reference_output_tensors = node.output_tensors
    
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
                    if has_arg(layer.call, 'mask'):
                        if 'mask' not in kwargs:
                            kwargs['mask'] = computed_mask
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensor, computed_mask))
                    computed_tensors = [computed_tensor]
                    computed_masks = [computed_mask]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    if has_arg(layer.call, 'mask'):
                        if 'mask' not in kwargs:
                            kwargs['mask'] = computed_masks
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)
    
    output_tensors = []
    for x in model.outputs:
        if x not in tensor_map:
            raise AssertionError('Could not compute output ', str(x))
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```