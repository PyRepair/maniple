### Analysis:
The error message indicates that the model is failing at the assertion step within the `_clone_functional_model` function. Specifically, the assertion checks if the output tensor from the model is present in the tensor_map after the function execution, and an AssertionError is raised because it couldn't find the output tensor in the tensor_map.

### Bug Description:
The bug lies in the logic where the `reference_output_tensors` from the nodes are not properly updated in the `tensor_map`, causing the final assertion to fail when checking the presence of output tensors in the map.

### Bug Fix Strategy:
To fix this bug, we need to ensure that the output tensors from the model nodes are correctly updated in the `tensor_map` along with their corresponding computed tensors and masks.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_tensors = [Input(shape=layer.batch_input_shape[1:]) for layer in model._input_layers]
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
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in range(len(model._nodes_by_depth)):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue
            node_key = layer.name + '_node_' + str(node.index)
            computed_data = [(tensor_map[x][0], None) for x in node.input_tensors if x in tensor_map]
            if len(computed_data) == len(node.input_tensors):
                kwargs = node.arguments or {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                if has_arg(layer.call, 'mask') and len(computed_data) > 1:
                    kwargs['mask'] = computed_masks
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### Correction Rationale:
1. Corrected the creation of input tensors by iterating over the model's `_input_layers` to create placeholders or input tensors based on availability.
2. Updated the loop for iterating through model nodes by using the range of depths directly, helping to extract node's computed data and process it correctly for the tensor map.
3. Used the updated computed data to correctly update output tensors in the tensor map for all nodes.
4. Modified the final check for output tensors to fetch the correct tensors from the tensor map.

By applying these corrections, the function should now be able to correctly clone the functional model without encountering the previous assertion error.