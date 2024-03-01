### Analysis:
1. **Bug in the Code**:
    - The bug occurs in the `_clone_functional_model` function within the Keras library. The issue arises when trying to clone a model with multiple outputs and a layer in the model does not support masks.
    - The failing test case provided tries to clone a model with a functional layer that does not support masks, leading to the error message "Could not compute output".
  
2. **Error Location**:
    - The error occurs when iterating over the nodes in the model and trying to compute the output tensors. The issue arises due to the inability to compute masks for layers that don't support them.

3. **Cause of the Bug**:
    - When the layers in the model have multiple outputs and one of the layers lacks support for masks, the function fails to compute the output tensors correctly, leading to the AssertionError. This issue was reported on GitHub under the title "Could not compute output Tensor" where the user provided a script that reproduces the error.

### Bug Fix Strategy:
To fix the bug and address the reported GitHub issue, you need to update the `_clone_functional_model` function to handle layers without mask support properly. This involves adjusting the logic when computing the tensor outputs for each layer. Instead of always expecting masks for the output tensors, we need to handle the case where a layer doesn't support masks.

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
            # Cache newly created input layer.
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
        for _original, _cloned in zip(model._input_layers, input_layers):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for x in input_tensors:
            if not K.is_keras_tensor(x):
                name = model._input_layers[len(_input_tensors)].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                # Cache newly created input layer.
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
            compute_flag = True
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
                else:
                    compute_flag = False
                    break

            if compute_flag:
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the `_clone_functional_model` function should now properly handle cases where layers do not support masks and compute the output tensors for each layer in the model. This fix is aligned with addressing the reported issue on GitHub.