### Analysis:
1. The function `_clone_functional_model` in the `keras/models.py` file is intended to clone a functional `Model` instance.
2. The test function `test_clone_functional_model_with_multi_outputs` in `tests/keras/test_sequential_model.py` creates a model with multiple outputs and then attempts to clone it using `keras.models.clone_model`.
3. The error message indicates that an assertion fails because the output tensor cannot be computed.
4. The GitHub issue describes a similar problem where `clone_model` fails when multi-GPU functionality with `cpu_relocation=True` is used, indicating a bug during the model cloning process.

### Bug Explanation:
The bug occurs due to the incorrect handling of multiple output tensors in the `_clone_functional_model` function. When constructing the new model's output tensors, it fails to properly map the output layers leading to the assertion error. This issue specifically arises when an output tensor cannot be computed, as indicated in the failing test and the GitHub issue.

### Bug Fix Strategy:
1. Ensure that all output tensors are correctly mapped and computed during the model cloning process.
2. Handle the case where a layer does not support masks, such as in the case of the Lambda layer used in the failing test and described in the GitHub issue.

### Corrected Version
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
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        for original_layer, input_layer in zip(model._input_layers, input_tensors):
            layer_map[original_layer] = input_layer
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            name = model._input_layers[i].name
            if not K.is_keras_tensor(x):
                x = Input(tensor=x, name='input_wrapper_for_' + name)
            layer_map[model._input_layers[i]] = x

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
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
                if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                    kwargs['mask'] = computed_masks
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                tensor_map.update((k, (v, m)) for k, v, m in zip(reference_output_tensors, output_tensors, computed_masks))

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### Changes Made:
1. Corrected the mapping and handling of input tensors when building the model.
2. Updated the mapping and calculation of output tensors to ensure all outputs are correctly computed.
3. Handled the case where a layer does not support masks, providing appropriate behavior.

By implementing the corrections outlined above, the function `_clone_functional_model` should now be able to handle the cloning of functional models with multiple outputs, resolving the bug described in the failing test and the GitHub issue.