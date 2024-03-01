### Bug Explanation
The bug in the `_clone_functional_model` function lies in the incorrect handling of the `input_layers` list and the creation of placeholder input layers. The function fails to correctly populate the `input_layers` list, leading to issues when creating new input layers.

### Bug Fix Strategy
To fix the bug, we need to ensure that the `input_layers` list is properly constructed and that the creation of placeholder input layers is consistent with the actual input layers of the model.

### Updated Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_layers = model._input_layers[:]  # Clone the list
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in input_layers]

        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + model._input_layers[i].name)
                input_tensors[i] = input_tensor
                layer_map[x._keras_history[0]] = input_tensor._keras_history[0]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

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
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensor, computed_mask))
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)

```

After applying these changes, the `_clone_functional_model` function should now correctly clone the functional model as intended and pass the failing test case.