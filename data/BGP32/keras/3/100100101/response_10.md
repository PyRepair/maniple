### Bug Explanation:

The bug in the `_clone_functional_model` function lies in the section where the input layers are processed. Specifically, there are two issues:
1. When creating input placeholders for building the model, the loop intended to cache the newly created input layers assigns the list `input_layers` to an empty list instead of the placeholders that were created, resulting in an incomplete creation of the `layer_map`.
2. When dealing with input tensors that are not instances of Keras layers, the code creates new input layers correctly but assigns them to the variable `_input_tensors` instead of updating `input_tensors`, leading to an inconsistency in the input tensors used for the rest of the function.

### Fix Strategy:

To address the bug, the following steps can be taken:
1. Ensure that the newly created input layers are properly added to the `input_layers` list.
2. Update the `input_tensors` list with the new input layers when non-Keras tensors are encountered.

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
            input_layers.append(input_tensor)
            layer_map[layer] = input_tensor._keras_history[0]

    else:
        input_tensors = to_list(input_tensors)

        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[x._keras_history[0]] = input_tensor._keras_history[0]

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
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    computed_tensors = [computed_tensor]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected function addresses the issues mentioned above and should now properly clone the functional model as expected in the failing test case.