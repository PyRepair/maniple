The bug in the `_clone_functional_model` function seems to be related to the incorrect handling of input and output tensors and the mapping of layers and tensors. This results in the assertion error during the test, indicating that the output tensor is not present in the `tensor_map`.

The potential error location within the problematic function is likely in the section where the function iterates over the nodes of the model and computes the output tensors.

The bug's cause is the mishandling of layer mapping and tensor mapping, leading to incorrect computation of output tensors, which fails the assertion during the test.

Possible approaches for fixing the bug include:
1. Ensuring that the mapping of layers and tensors is correctly managed to avoid duplication and retain the intended behavior of the cloned model.
2. Properly computing the output tensors and handling them in the `tensor_map` to ensure their availability.

Here's the corrected code for the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    input_layers = model._input_layers

    if input_tensors is None:
        for layer in input_layers:
            input_tensor = Input(shape=layer.input_shape[1:])
            layer_map[layer] = input_tensor
            input_tensors = input_tensor
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[input_layers[i]] = input_tensor
            else:
                layer_map[input_layers[i]] = x

    for layer in model.layers:
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
        else:
            layer_map[layer] = layer_map[layer]

    for node in model._nodes_by_depth:
        layer = node.outbound_layer
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
        else:
            new_layer = layer_map[layer]
            if isinstance(new_layer, InputLayer):
                continue

        reference_input_tensors = node.input_tensors
        computed_data = []

        for x in reference_input_tensors:
            computed_data.append(tensor_map[x])

        if len(computed_data) == len(reference_input_tensors):
            if node.arguments:
                kwargs = node.arguments
            else:
                kwargs = {}

            computed_tensors = [x[0] for x in computed_data]
            output_tensors = to_list(new_layer(computed_tensors, **kwargs))

            for x, y in zip(node.output_tensors, output_tensors):
                tensor_map[x] = y

    output_tensors = [tensor_map[x] for x in model.outputs]

    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected function ensures proper mapping of input and output tensors, handles layer duplication correctly, and computes the output tensors accurately. It should pass the failing test and resolve the Github issue regarding the cloned functional model.