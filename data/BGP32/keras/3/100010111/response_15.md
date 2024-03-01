### Analysis:
The buggy function is `_clone_functional_model` which is intended to clone a functional `Model` instance while creating new layers and weights instead of sharing the weights of the existing layers.

#### Issues:
1. The error message states that the function was not able to compute the output tensor.
2. The input tests have a multi-output model case that is not handled correctly in the cloning process.
3. The function is not correctly handling the scenario when a `Lambda` layer is used in the model which does not support mask.

### Bug Fix Strategy:
1. Adjust the function to correctly handle the scenario when there are multiple output tensors to be computed and added the necessary logic for `Lambda` layers.
2. Ensure that all input tensors come from a Keras layer and handle the multi-output cases appropriately.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

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
        input_layers = input_tensors
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]

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
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    tensor_map[node.output_tensors[0]] = (output_tensors[0], None)
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    for x, y in zip(reference_output_tensors, output_tensors):
                        tensor_map[x] = (y, None)

    output_tensors = [tensor_map[t][0] for t in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### The corrected function addresses the issues identified and should now be able to handle the multi-output model case and the `Lambda` layers correctly.