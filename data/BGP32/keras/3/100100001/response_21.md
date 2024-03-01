### Analysis:
1. The `_clone_functional_model` function is meant to clone a functional Model instance by creating new layers with new weights instead of sharing weights from the original model.
2. Potential error locations:
   - Incorrect handling of `input_layers` and `input_tensors` when input_tensors is not provided.
   - Possible issues with mapping input layers and tensors.
   - Iterating over nodes in depth order and computing output tensors.
   - Checking the computed output tensors at the end.
3. The bug is likely to be related to how the input layers and tensors are handled, leading to incorrect mapping and potential issues with computing output tensors.
4. Strategy for fixing the bug:
   - Correctly create placeholders for input_layers when input_tensors is not provided.
   - Ensure consistent mapping of input tensors with corresponding layers.
   - Properly compute and update the tensor_map with output tensors.
   - Verify that all model outputs have been computed before creating a new model instance.

### Corrected Version:
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
        for layer in model.inputs:
            input_tensor = Input(batch_shape=layer.shape,
                                 dtype=layer.dtype,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            input_layers.append(layer)
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for layer in model.layers:
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer

    for node in model._nodes_by_depth:
        layer = node.outbound_layer
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
        else:
            new_layer = layer_map[layer]

        reference_input_tensors = node.input_tensors
        reference_output_tensors = node.output_tensors

        computed_data = []
        for x in reference_input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])

        if len(computed_data) == len(reference_input_tensors):
            kwargs = node.arguments if node.arguments else {}
            computed_tensors = [x[0] for x in computed_data]
            computed_masks = [x[1] for x in computed_data]
            output_tensors = to_list(new_layer(computed_tensors, **kwargs))
            output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))

            for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, f'Could not compute output {x}'
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)

```

By correcting the logic for handling input layers/tensors, mapping layers, computing output tensors, and ensuring all model outputs are computed, the corrected `_clone_functional_model` function should now pass the failing test provided.