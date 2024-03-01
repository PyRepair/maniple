The bug in the `_clone_functional_model` function lies in the incorrect creation and handling of input tensors and input layers within the function. The issue is related to the mismatch between the creation of input tensors and the caching of input layers.

To fix the bug, we need to ensure that the newly created input layers are correctly mapped to their corresponding original input layers. Also, we need to handle the creation of input layers and input tensors consistently throughout the function.

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

            input_layers.append(layer)
            input_tensors.append(input_tensor)

            layer_map[layer] = input_tensor
            tensor_map[layer.output] = (input_tensor, None)

        for idx, layer in enumerate(model._input_layers):
            if idx < len(input_layers):
                layer_map[layer] = input_layers[idx]

    else:
        input_tensors = to_list(input_tensors)
        new_input_tensors = []
        
        for i, x in enumerate(input_tensors):
            if K.is_keras_tensor(x):
                new_input_tensors.append(x)

            else:
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)

                new_input_tensors.append(input_tensor)
                layer_map[x] = input_tensor
                tensor_map[x] = (input_tensor, None)

        input_tensors = new_input_tensors

    for x in model.inputs:
        tensor_map[x] = (layer_map[x], None)

    nodes_depth = sorted(model._nodes_by_depth.keys(), reverse=True)

    for depth in nodes_depth:
        nodes = model._nodes_by_depth[depth]

        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                if 'mask' not in kwargs and has_arg(new_layer.call, 'mask'):
                    kwargs['mask'] = computed_masks

                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))

                for idx, x in enumerate(reference_output_tensors):
                    tensor_map[x] = (output_tensors[idx], output_masks[idx])

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected version of the function ensures that the input layers and input tensors are correctly mapped and handled throughout the function. This should address the bug and meet the expected input/output values for the given test cases.