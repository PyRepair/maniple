### Bug Analysis:
1. The function is expecting an instance of `Model` as the input argument, but it is incorrectly raising an error when checking for `Sequential` instances. This check should be removed.
2. The function is not properly populating the `input_layers` list, which leads to incorrect layer mappings.
3. There might be an issue with the creation of new layers and updating the `tensor_map` during the iteration process.

### Bug Fix:
1. Remove the `if isinstance(model, Sequential)` condition that raises an error for `Sequential` instances.
2. Populate the `input_layers` list with the newly created input tensors.
3. Update the `tensor_map` with the newly calculated tensors and masks during the layer cloning process.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    input_layers = []
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            input_layers.append(input_tensor)
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

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
                kwargs = node.arguments or {}
                input_data = [x[0] for x in computed_data]
                if 'mask' in kwargs:
                    kwargs['mask'] = [x[1] for x in computed_data if x[1] is not None]
                output_tensors = layer(input_data, **kwargs)
                output_masks = layer.compute_mask(input_data, **kwargs)
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_layers, output_tensors, name=model.name)
```  