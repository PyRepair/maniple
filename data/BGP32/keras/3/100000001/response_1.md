### Analysis:
The problematic areas in the `_clone_functional_model` function are:
1. Incorrect usage of `'= '` instead of `','` inside the `raise ValueError` statements.
2. The `input_layers` list is not being appended correctly in the first loop.
3. The index for accessing the original input layer in the second loop is not correct.
4. Incorrect caching of input data inside the `else` block.
5. Invalid check for the layer type in the `else` block.
6. Incorrect unpacking of `computed_data` inside the `if` condition.
7. Inconsistent usage of masks during layer computation.
8. Missing InputLayer handling in the layer cloning section.

### Bug Explanation:
The main bug in the provided function arises from improper indexing when working with `input_layers` list in the first loop. It causes an index out of range error and results in incorrect layer mapping. Additionally, inconsistent usage of masks during layer computations can lead to undesired behavior, and missing handling for InputLayer clones can result in unexpected errors.

### Bug Fix Strategy:
1. Replace `'= '` with `','` inside the `raise ValueError` statements.
2. Correctly append the `input_layers` list when creating the input tensors in the first loop.
3. Fix the index issue for accessing the original input layer in the second loop.
4. Properly cache the input data in the `else` block.
5. Adjust the type check logic to account for InputLayer instances.
6. Ensure consistent usage of masks during layer computations.
7. Add handling for InputLayer cloning in the layer cloning section.

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
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            layer_map[layer] = input_tensor
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        # Make sure that all input tensors come from a Keras layer.
        # If tensor comes from an input layer: cache the input layer.
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                # Cache newly created input layer.
                original_input_layer = model._input_layers[i]
                layer_map[original_input_layer] = input_tensor
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
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
                computed_tensors, computed_masks = zip(*computed_data)
                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = computed_masks
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```