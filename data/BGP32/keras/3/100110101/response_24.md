### Bug Analysis
The buggy function `_clone_functional_model` is expected to clone a functional `Model` instance, creating new layers and weights instead of sharing them. The bug seems to be related to handling the creation of new input layers and mapping the tensors correctly.

The failing test `test_clone_functional_model_with_multi_outputs` intends to create a model with multiple outputs, clone it using `keras.models.clone_model`, and compare the predictions of the original and cloned models. The failure occurs because the input to the model is a lambda layer with multiple outputs, which the current implementation of `_clone_functional_model` does not handle correctly.

### Bug Explanation
1. The function starts by creating new input layers if `input_tensors` is not provided, but it fails to correctly handle storing these newly created input layers in the `layer_map`.
2. When the function encounters a lambda layer with multiple outputs, such as the `layer1` in the failing test, the mechanism to handle multiple outputs and correctly compute the tensor map is not implemented correctly. This leads to the failing assertion where the output tensor from the SwapLayer is not found in the `tensor_map`.
3. The failure is due to the incomplete handling of lambda layers with multiple outputs in the model cloning function.

### Bug Fix Strategy
To fix the bug, we need to:
1. Ensure that newly created input layers are correctly added to the `layer_map`.
2. Add support for lambda layers with multiple outputs in the function logic for creating the tensor map.
3. Update the model cloning function to handle lambda layers with multiple outputs properly.

### Corrected Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[input_tensors[i]._keras_history[0]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in reversed(sorted(model._nodes_by_depth.keys())):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]
                if isinstance(new_layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data) if len(computed_data) > 1 else ([computed_data[0][0]], [computed_data[0][1]])
                if has_arg(new_layer.call, 'mask'):
                    kwargs['mask'] = computed_masks
                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks)) if has_arg(layer.call, 'mask') else [None] * len(output_tensors)

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
    cloned_outputs = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, cloned_outputs, name=model.name)
```

After applying this correction to the `_clone_functional_model` function, the test `test_clone_functional_model_with_multi_outputs` should pass without any assertion errors.