### Identification of Potential Error Locations
1. The check for whether the input model is an instance of `Model` is correct but the subsequent check for `Sequential` instance is incorrect. 
2. The instantiation of `input_layers` list within the `if input_tensors is None:` block is not utilized later in the code.
3. The assignment of `input_tensor` within the `else` block does not populate the `input_layers` list as intended.
4. Issues with the usage of `new_layer` and `layer_map`.
5. The error message "Could not compute output Tensor" indicates an issue with computing the model outputs.

### Bug Cause
The bug is likely the result of incorrect operations within the `_clone_functional_model` function. The flow of the function is not handling the layers and inputs properly, resulting in the inability to compute the model outputs correctly. This issue corresponds to the GitHub issue where a similar problem has been observed.

### Fixing Strategy
1. Remove the incorrect check for `Sequential` instance.
2. Properly populate the `input_layers` list.
3. Correct the assignment and usage of `input_tensor` within the function.
4. Ensure correct handling of cloned layers using `new_layer` and `layer_map`.
5. Address the issue with computing model outputs.

### Corrected Version of the Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensor._keras_history = [layer, 0, 0]
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor

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
                new_layer = layer_map[layer]

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

                output_tensors = to_list(new_layer(computed_data, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        if x not in tensor_map:
            raise ValueError('Could not compute output ', x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```