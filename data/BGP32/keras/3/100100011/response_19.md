### Analysis:
1. The `_clone_functional_model` function is responsible for cloning a functional `Model` instance. It iterates over the layers of the original model, creates new layers, and builds a new model using the new layers.
2. The test function `test_clone_functional_model_with_multi_outputs` creates a model with multiple inputs and multiple outputs. It then uses `keras.models.clone_model` to clone the model and compares the predictions from the original model and the cloned model.
3. The GitHub issue reports an error related to not being able to compute the output tensor when using `clone_model` with a model that has a layer with multiple outputs but does not support masks.
4. The bug seems to be related to handling outputs and masks when a layer does not support masks, leading to incorrect output tensors being computed during the cloning process.

### Bug Cause:
- The bug is caused by the `output_masks` being set to `None` due to a layer (like Lambda) not supporting masks.
- When the cloned layers are created from the original layers, the logic for computing masks and handling multiple outputs is flawed, leading to incorrect values or `None` being assigned to `output_masks`, which causes the failure in predicting output tensors.

### Bug Fix Strategy:
- Update the logic for handling masks and outputs when cloning layers.
- Ensure that when a layer does not support masks, the output masks are handled properly during the cloning process.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_layers = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
                        for layer in model._input_layers]
        input_tensors = input_layers

        for original, cloned in zip(model._input_layers, input_layers):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        new_input_tensors = []

        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                new_input_tensors.append(input_tensor)

                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                new_input_tensors.append(x)

        input_tensors = new_input_tensors

    for orig_input, new_input in zip(model.inputs, input_tensors):
        tensor_map[orig_input] = (new_input, None)

    for depth in reversed(range(len(model._nodes_by_depth))):
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
            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data) if computed_data else ([], [])
                
                if has_arg(new_layer.call, 'mask'):
                    kwargs['mask'] = computed_masks if computed_masks and all(mask is not None for mask in computed_masks) else None

                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                
                if has_arg(new_layer.call, 'mask'):
                    output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))
                else:
                    output_masks = [None] * len(output_tensors)

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    for x in model.outputs:
        if x not in tensor_map:
            raise ValueError('Could not compute output ' + str(x))

    return Model(input_tensors, output_tensors, name=model.name)
```

After applying the suggested corrections to the `_clone_functional_model` function, it should be able to successfully clone functional models, including models with layers that have multiple outputs and do not support masks, resolving the issue raised in the GitHub report.