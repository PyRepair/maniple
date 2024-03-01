The bug in the `_clone_functional_model` function arises from the incorrect handling of input tensor mapping and the creation of new input layers. This leads to incorrect mappings and missing output tensors in the cloned model.

To fix this bug, we need to adjust the logic related to input tensor creation and mapping in the function. Specifically, we need to ensure that the input tensors are correctly created, mapped, and used in the cloning process.

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
            input_tensor = Input(batch_shape=layer.input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_layer = Input(tensor=x,
                                    name='input_wrapper_for_' + name)
                input_tensors[i] = input_layer
                layer_map[model._input_layers[i]] = input_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth, nodes in model._nodes_by_depth.items():
        for node in nodes:
            outbound_layer = node.outbound_layer
            if outbound_layer not in layer_map:
                new_layer = outbound_layer.__class__.from_config(outbound_layer.get_config())
                layer_map[outbound_layer] = new_layer
            else:
                new_layer = layer_map[outbound_layer]

            reference_input_tensors = node.input_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(new_layer(computed_tensor, **kwargs))
                    computed_tensors = [computed_tensor]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(new_layer(computed_tensors, **kwargs))

                for i, x in enumerate(node.output_tensors):
                    tensor_map[x] = (output_tensors[i], None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

With these corrections, the `_clone_functional_model` function should now properly handle the cloning of the model and pass the failing test.