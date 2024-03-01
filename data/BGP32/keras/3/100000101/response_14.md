### Analysis:
The bug in the `_clone_functional_model` function seems to be related to the creation and mapping of input tensors. The function is expected to clone a given functional model, but it fails to properly handle the input tensors, resulting in incorrect mappings and missing outputs.

The issue arises from the incorrect handling of input tensors when creating new layers and mapping them in `layer_map` and `tensor_map`. Additionally, the loop that iterates through nodes and computes outputs has issues with correctly mapping the tensors, leading to missing outputs.

### Bug Fix Strategy:
1. Ensure that the input tensors are properly created and mapped to the corresponding layers.
2. Correct the mapping of tensors during the computation of output tensors.
3. Verify the creation of new layers and update the mapping accordingly.

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
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        for orig, cloned in zip(model._input_layers, input_tensors):
            layer_map[orig] = cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                layer_map[x._keras_history[0]] = input_tensor
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
                    tensor_map[reference_output_tensors[0]] = (output_tensors[0], None)
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    for x, y in zip(reference_output_tensors, output_tensors):
                        tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        output_tensors.append(tensor_map[x][0])

    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the function addresses the issues related to input tensor creation, mapping, layer cloning, and output tensor computation. It should now properly clone the functional model with the expected input/output values.