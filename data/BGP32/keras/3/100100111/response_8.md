### Analysis:
1. The buggy function `_clone_functional_model` is intended to clone a functional model instance in Keras, creating new layers and weights instead of sharing existing ones.
2. The function expects a `Model` instance as input and checks for certain conditions before proceeding with cloning.
3. The bug seems to occur when dealing with models containing multiple inputs and outputs, where layers may not support masks causing the error "Could not compute output Tensor."
4. The failing test case `test_clone_functional_model_with_multi_outputs` demonstrates this issue when cloning a model with Lambda and SwapLayer layers, leading to an assertion error.

### Bug Explanation:
The bug occurs due to the incorrect handling of layer masks in functional models containing multiple inputs and outputs. In the failing test case, the Lambda layer does not support masks, causing the model cloning process to encounter issues with mask handling.

### Bug Fix Strategy:
1. Check for layers that do not support masks and bypass mask-related operations if necessary.
2. Update the logic for handling layers that do not support masks during the cloning process.
3. Ensure that the tensor mapping and output computations consider cases where masks are not supported by specific layers.

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
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
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
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

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

By updating the mask handling logic and ensuring proper handling of layers that do not support masks, the corrected function should now be able to clone functional models with multiple inputs and outputs correctly. This corrected version should resolve the issue mentioned in the GitHub bug report and pass the failing test case provided.