The bug in the provided function is due to the incorrect handling of input layers and the creation of placeholder input tensors. Here's an explanation of the bug and a strategy to fix it:

1. The bug occurs when the function is creating new input tensors without properly mapping them to the original input layers. This leads to an inconsistency in the creation of placeholder input tensors if `input_tensors` is not provided.

2. The bug specifically affects the creation of `input_layers` and the mapping of the newly created input tensors to the original input layers.

To fix this bug:
- Ensure that the newly created input tensors are correctly mapped to the original input layers.
- Update the assignment of `input_layers` to include the correct input layers for mapping.
- Check the consistency of input tensor creation when `input_tensors` is not provided.

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
            input_layers.append(layer)
            layer_map[layer] = input_tensor
        
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []

        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                layer_map[model._input_layers[i]] = input_tensor
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

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []

    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

Make sure to thoroughly test the corrected function with different scenarios to ensure its correctness.