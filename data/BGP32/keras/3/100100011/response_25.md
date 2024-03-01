### Error Location:
The buggy function `_clone_functional_model` has a bug in handling models with multiple outputs. Specifically, the issue arises when the function encounters a layer that does not support masks (like the Lambda layer in the test case provided) and attempts to compute masks, resulting in None values for `output_masks`. This leads to an error when the function tries to process the output tensors.

### Bug Cause:
The buggy function fails to handle layers without mask support correctly, resulting in mismatched values for `output_masks` and subsequently failing to compute the model outputs accurately.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the handling of layers without mask support to avoid trying to compute masks. We can skip mask computation for layers that do not support masks, preventing the `None` values issue.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                x = Input(tensor=x, name='input_wrapper_for_' + name)
            layer_map[x._keras_history[0]] = x

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in reversed(sorted(model._nodes_by_depth.keys())):
        for node in model._nodes_by_depth[depth]:
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

            if all(x in tensor_map for x in reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors]

                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    kwargs.setdefault('mask', None)
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    kwargs.update({'mask': [x[1] for x in computed_data]})

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the `_clone_functional_model` function should resolve the issue mentioned in the failing test and the related GitHub issue. It adjusts the handling of layers without mask support, preventing the error when computing model outputs.