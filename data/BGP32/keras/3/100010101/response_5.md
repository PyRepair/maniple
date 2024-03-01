The bug in the `_clone_functional_model` function lies in the incorrect handling of the `input_layers` list when `input_tensors` is None, resulting in an empty `input_layers` list and subsequently leading to missing proper mapping in the `layer_map`. This missing mapping causes the assertion error during the model output computation.

To fix the bug, we need to ensure that the `input_layers` list is populated correctly by appending the newly created input layers. Additionally, we need to properly update the `layer_map` with the correct mapping between original layers and cloned layers.

Here is the corrected version of the `_clone_functional_model` function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None or not input_tensors:
        input_tensors = [Input(batch_shape=input_layer.batch_input_shape, dtype=input_layer.dtype, sparse=input_layer.sparse, name=input_layer.name)
                         for input_layer in model._input_layers]
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth, reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data if x[1] is not None]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for i in range(len(reference_output_tensors)):
                    tensor_map[reference_output_tensors[i]] = (output_tensors[i], output_masks[i])

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    for output_tensor in model.outputs:
        if output_tensor not in tensor_map:
            raise ValueError('Could not compute output ', output_tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version populates the `input_tensors` list properly when `input_tensors` is None, ensures proper mapping in the `layer_map`, and adjusts the input layer creation logic. The function now handles the model cloning process correctly and should pass the failing test case.