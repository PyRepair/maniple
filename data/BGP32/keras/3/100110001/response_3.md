### Analysis:
The error occurs during the cloning of a functional model with multiple outputs. The `AssertionError` states that the model was unable to compute one of the outputs during the cloning process.

### Bug:
The bug lies in the `_clone_functional_model` function. Specifically, the bug is related to handling the multiple outputs scenario. The issue stems from not correctly tracking the input tensors and not properly formulating the new model with its outputs.

### Fix Strategy:
1. Ensure that all input tensors are correctly mapped and accounted for.
2. Check that all outputs are successfully computed during the replication of the model.
3. Correctly initialize the Model instance with the input and output tensors.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    input_layers = model.input_layers
    output_layers = model.output_layers

    layer_map = {}  
    tensor_map = {}  

    input_tensors = to_list(input_tensors) if input_tensors is not None else input_layers

    for x, y in zip(input_layers, input_tensors):
        tensor_map[x] = (y, None)

    for output_layer in output_layers:
        # Get or create layer.
        if output_layer not in layer_map:
            # Clone layer.
            new_layer = output_layer.__class__.from_config(output_layer.get_config())
            layer_map[output_layer] = new_layer
        else:
            # Reuse previously cloned layer.
            new_layer = layer_map[output_layer]

        layer_tensors = []
        for input_layer in output_layer._inbound_nodes[0].input_tensors:
            tensor, mask = tensor_map[input_layer]
            layer_tensors.append(tensor)

        kwargs = output_layer._inbound_nodes[0].arguments if output_layer._inbound_nodes else {}

        output_tensor = new_layer(layer_tensors[0] if len(layer_tensors) == 1 else layer_tensors, **kwargs)
        tensor_map[output_layer] = (output_tensor, None)

    output_tensors = [tensor_map[output_layer][0] for output_layer in output_layers]

    return Model(input_tensors, output_tensors, name=model.name)
```

### Corrected Test:
The provided test should pass after applying the correct function.