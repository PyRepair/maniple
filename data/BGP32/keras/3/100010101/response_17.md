### Analysis:
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers with new weights instead of sharing the weights of the existing layers. The error message indicates that there is an issue when trying to compute the output for a tensor.

#### Bugs in the current implementation:
1. The variable `input_layers` is defined but not used within the function.
2. The loop that assigns the input layers to `layer_map` is missing, leading to incorrect input_tensors being generated.
3. There is an issue when handling multi-output layers, causing a failure in computing the output tensors.

### Bug Fix Strategy:
1. Initialize the `input_layers` list inside the `if input_tensors is None` block and use it to assign the input layers correctly.
2. Ensure that all input tensors are correctly cached in the `layer_map` and `tensor_map`.
3. Improve the handling of multi-output layers to compute the correct output tensors.

### Bug-fixed version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    input_layers = []  # List to store input layers
    if input_tensors is None:
        # Create placeholders to build the model on top of
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                                 sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer
            new_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = new_input_layer
            input_layers.append(new_input_layer)
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                # Cache newly created input layer
                original_input_layer = x._keras_history[0]
                new_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = new_input_layer
            input_layers.append(x)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

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
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor))
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_layers, output_tensors, name=model.name)
```