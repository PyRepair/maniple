### Analysis:
1. The buggy function `_clone_functional_model` is supposed to clone a functional `Model` instance. The function fails to properly handle certain scenarios, leading to the error message during the failing test.
2. The error occurs when the `clone_model` function is called in the failing test `test_clone_functional_model_with_multi_outputs`.
3. The failing test error message indicates that the specific tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)` couldn't be computed, which points to an issue in the model cloning process.
4. The GitHub issue also identifies a similar problem when using `clone_model`, mentioning the issue relating to the `clone_model` method not handling multi-output layers without mask support properly.

### Bug Cause:
The bug arises from the `_clone_functional_model` function not handling multi-output layers without mask support correctly when cloning the model. This leads to the error where the output tensor is not computed.

### Bug Fix Strategy:
To fix the bug, we need to address how the function handles multi-output layers without mask support during the model cloning process. Specifically, in scenarios where a layer doesn't support masks and has multiple outputs, the function must handle this case properly to avoid the error.

### Corrected Version:
Here is the corrected version of the `_clone_functional_model` function:
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
            layer_map[layer] = input_tensor
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            outbound_layer = node.outbound_layer
            if outbound_layer not in layer_map:
                new_layer = outbound_layer.__class__.from_config(outbound_layer.get_config())
                layer_map[outbound_layer] = new_layer
            else:
                outbound_layer = layer_map[outbound_layer]
                if isinstance(outbound_layer, InputLayer):
                    continue

            input_tensors = [tensor_map[x][0] for x in node.input_tensors if x in tensor_map]
            if len(input_tensors) == len(node.input_tensors):
                arguments = node.arguments if node.arguments else {}
                computed_tensors = [tensor_map[x][0] for x in node.input_tensors]
                kwargs = {'mask': tensor_map[x][1] for x in node.input_tensors if tensor_map[x][1] is not None}
                output_tensors = to_list(outbound_layer(computed_tensors, **kwargs))
                output_masks = to_list(outbound_layer.compute_mask(computed_tensors, computed_tensors))
                
                for i, output_tensor in enumerate(to_list(node.output_tensors)):
                    tensor_map[output_tensor] = (output_tensors[i], output_masks[i])

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

With these corrections, the function should now properly handle cloning a functional model with multi-output layers without mask support, resolving the error encountered in the failing test.