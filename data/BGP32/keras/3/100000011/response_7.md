### Analysis:
The buggy function `_clone_functional_model` is responsible for cloning a functional `Model` instance in Keras. The GitHub issue related to this bug indicates that when using `clone_model` with `multi_gpu_model` and `cpu_relocation=True`, an error occurs due to the `output_masks` being `[None]` instead of `[None, None]` as expected. This is because the `layer.compute_mask` method returns `None` when the layer does not support masks, leading to the assertion error when computing the output tensors in the function.

### Potential Error Locations:
1. In the creation of the input layers when `input_tensors` is not provided.
2. Handling the input tensors to ensure they come from Keras layers.
3. Computation of output tensors and masks in the loop.
4. Checking for computed output tensors at the end.

### Cause of the Bug:
The bug occurs because the function assumes that the `compute_mask` method will return valid masks for each output tensor. However, when certain layers (like Lambda) do not support masks, the `output_masks` list ends up containing `[None]`, causing issues when computing the final output tensors in `tensor_map`.

### Strategy for Fixing the Bug:
To fix this bug, we can modify the function to handle cases where `compute_mask` returns `None` properly by checking for the existence of masks before assigning them to the `output_masks` list. Additionally, we need to ensure that the function can handle situations where certain layers do not support masks by modifying the logic for computing the output tensors appropriately.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        input_layers = []
        input_tensors = []
 
        for i, layer in enumerate(model._input_layers):
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[model.inputs[i]] = newly_created_input_layer

    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                # Cache newly created input layer.
                original_input_layer = model._input_layers[i]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
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

            computed_data = []  # List of tuples (input, mask).
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(layer.call, 'mask') and computed_mask is not None:
                        if 'mask' not in kwargs:
                            kwargs['mask'] = computed_mask
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensor, computed_mask))
                    computed_tensors = [computed_tensor]
                    computed_masks = [computed_mask] if computed_mask is not None else [None]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    if has_arg(layer.call, 'mask') and any(mask is not None for mask in computed_masks):
                        if 'mask' not in kwargs:
                            kwargs['mask'] = computed_masks
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                    output_masks = [mask if mask is not None else None for mask in output_masks]

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

After applying the corrections to handle cases where `compute_mask` returns `None`, the function should now be able to clone functional models correctly without running into the `Could not compute output Tensor` issue as reported in the GitHub thread.