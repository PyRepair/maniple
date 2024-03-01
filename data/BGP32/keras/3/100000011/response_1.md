## Analysis:
The buggy function `_clone_functional_model` is used to clone a functional `Model` instance but has an issue related to the computation of output tensors, leading to the error mentioned in the GitHub issue.

## Identified Potential Error Locations:
1. In the section where the `output_masks` are computed based on the layer's ability to support masks.
2. The handling of multiple outputs from a layer without mask support.
3. The mapping of input tensors with their corresponding new input layers.

## Cause of the Bug:
The bug arises due to the inability to compute output tensors properly when cloning a model in the presence of layers with multiple outputs without mask support, as observed in the Lambda layer in the GitHub issue. This leads to a mismatch in the expected output masks causing the `Could not compute output Tensor` error.

## Strategy for Fixing the Bug:
1. Modify the logic for handling output masks when calling the layer.
2. Handle the case of multiple outputs from a layer without mask support appropriately.
3. Ensure the proper mapping of input tensors with their newly created input layers.

## Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[model._input_layers[i]] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for node in model._nodes_by_depth:
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

        computed_data = []  # List of tuples (input, mask)
        for x in reference_input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])

        if len(computed_data) == len(reference_input_tensors):
            kwargs = node.arguments if node.arguments else {}
            
            computed_tensors = [x[0] for x in computed_data]
            computed_masks = [x[1] for x in computed_data]

            output_tensors = to_list(layer(computed_tensors, **kwargs))
            output_masks = [None] * len(output_tensors)

            for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the `_clone_functional_model` function includes fixes to properly handle output masks and multiple outputs without mask support, addressing the issue mentioned in the GitHub thread.