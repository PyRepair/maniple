The bug in the provided function lies in the incorrect creation and handling of input tensors when `input_tensors` is not None. The function fails to correctly handle the case when input tensors are provided in the function call, causing issues with the mapping of tensors.

To fix this bug, we need to ensure that the provided input tensors are correctly processed and mapped to the corresponding layers. Specifically, we need to update the `_input_tensors` list to include the created input tensors and ensure that the mapping in `tensor_map` is correct.

Here is the corrected version of the function:

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
            # Cache newly created input layer.
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                # Cache newly created input layer.
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
                computed_masks = [x[1] for x in computed_data]
                
                if has_arg(layer.call, 'mask') and isinstance(computed_masks[0], list):
                    kwargs['mask'] = computed_masks[0]
                                        
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                if has_arg(layer.call, 'mask'):
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                    for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                        tensor_map[x] = (y, mask)
                else:
                    for x, y in zip(reference_output_tensors, output_tensors):
                        tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the function should now properly handle the provided input tensors and create new mappings in `tensor_map` based on the processed inputs.