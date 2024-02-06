Based on the provided error message, it seems that there is an issue in the `clone_model` function, where the output tensor cannot be computed. The function `_clone_functional_model` inside the Keras library seems to be the source of this problem. This function is responsible for cloning a functional `Model` instance and appears to encounter issues when dealing with a layer that has multiple outputs without mask support.

The error suggests that the `output_masks` for the layers with multiple outputs is always `None`, whereas it's expected to be `[None, None]`. This is likely due to the fact that the function `layer.compute_mask(...)` always returns `None` since Lambda layers do not support using masks.

To fix this bug, one possible approach is to modify the function to handle the case where a layer with multiple outputs without mask support is encountered. This might involve updating the logic around computing output tensors and masks for such layers.

Here's the revised and fixed version of the `_clone_functional_model` function to address the bug:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        input_layers = [Input(batch_shape=layer.batch_input_shape,
                              dtype=layer.dtype,
                              sparse=layer.sparse,
                              name=layer.name) for layer in model._input_layers]
        input_tensors = input_layers
        for original, cloned in zip(model._input_layers, input_layers):
            layer_map[original] = cloned
    else:
        if not all(K.is_keras_tensor(x) for x in to_list(input_tensors)):
            raise ValueError('All input tensors must come from a Keras layer')

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer.
            layer = node.outbound_layer

            # Get or create layer.
            if layer not in layer_map:
                # Clone layer.
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                # Reuse previously cloned layer.
                layer = layer_map[layer]

            # Gather inputs to call the new layer.
            reference_input_tensors = node.input_tensors

            # If all previous input tensors are available in tensor_map,
            # then call node.inbound_layer on them.
            computed_data = []  # List of tuples (input, mask).
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                # Update tensor_map.
                for x, y, mask in zip(node.output_tensors, layer(computed_data)):
                    tensor_map[x] = (y, mask)

    # Check that we did compute the model outputs,
    # then instantiate a new model from inputs and outputs.
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

By modifying and updating the logic in the `_clone_functional_model` function, we aim to address the issues related to computing the output tensors and masks for layers with multiple outputs without mask support.

This revised function ensures that the input tensors are correctly mapped, handles the creation and reuse of layers, and properly computes the output tensors and masks. This should resolve the bug encountered during the cloning process.