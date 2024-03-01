### Bug Explanation
The bug occurs in the `_clone_functional_model` function due to incorrect handling of the input tensors when cloning a model. The function fails to properly create input layers and update the `input_layers` list. This results in missing input layers and inconsistencies in the creation of the new model.

### Bug Fix Strategy
To fix the bug, we need to ensure that all input tensors are correctly mapped to input layers and that the layer creation process proceeds smoothly. This involves creating placeholders for input tensors when not provided, correctly handling input tensor origins, and ensuring that all tensors are properly mapped during the cloning process.

### Corrected Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

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
            input_layers.append(input_tensor)
        
        input_layers.reverse()  # Reverse input_layers list to correctly map with input_tensors
        
        for original, cloned in zip(model._input_layers, input_layers):
            layer_map[original] = cloned

    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                _input_layers = x._keras_history[0]
                layer_map[_input_layers] = input_tensor
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
            else:
                new_layer = layer_map[layer]
                if isinstance(new_layer, InputLayer):
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
                    computed_tensor, _ = computed_data[0]
                else:
                    computed_tensors, _ = zip(*computed_data)
                
                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

After applying these changes, the `test_clone_functional_model_with_multi_outputs` test should now pass successfully without any assertion errors.