The bug in the `_clone_functional_model` function lies in the initialization of `input_layers` and `input_tensors` when `input_tensors` is not provided. This causes a mismatch between the expected and actual behavior of building the model upon new inputs.

### Error explanation:
When `input_tensors` is not provided, the function should create placeholders to build the model on top of it. However, the initialization of `input_layers` is missing in this case, leading to an empty list and incorrect mapping between the original input layers and the newly created ones. This results in a failure to compute the model outputs correctly.

### Bug fix strategy:
To address this issue, we need to correctly initialize `input_layers` when `input_tensors` is not provided and ensure that the mapping between the original input layers and the placeholders is accurate. Moreover, we should update the `layer_map` and `tensor_map` logic to match the correct input layer creation process.

### Corrected function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    
    if input_tensors is None:
        input_layers = []  # Initialize input_layers
        input_tensors = []
        for layer in model._input_layers:
            # Create placeholders and update input_layers
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_layers.append(input_tensor)
            layer_map[layer] = input_tensor

    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                input_layers.append(input_tensor)
                layer_map[x._keras_history[0]] = input_tensor
            else:
                input_layers.append(x)

    for x, y in zip(model.inputs, input_layers):
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
                
                if has_arg(layer.call, 'mask'):
                    if 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_layers, output_tensors, name=model.name)
```

By updating the initialization of `input_layers` properly and ensuring the mapping logic is correct, the corrected function should now accurately clone the functional model as expected.