The bug in the `_clone_functional_model` function is causing the issue reported on GitHub. The function fails to handle the case where the output masks are always None due to a layer not supporting masks, leading to the "Could not compute output Tensor" error.

**Analysis:**
- The bug arises when iterating over the reference model nodes and calling the layers. If a layer does not support masks, the output masks are set to None, which conflicts with the expected output_masks being [None, None].
- The issue stems from handling layers that do not support masks, like Lambda layers.

**Strategy for Fixing the Bug:**
- Modify the function to handle layers that do not support masks by adjusting the logic when computing output tensors and masks.
- Update the code to correctly propagate None when masks are not supported by layers.

**Corrected Version of the Function:**
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor._keras_history[0]

    for i, x in enumerate(to_list(input_tensors)):
        if not K.is_keras_tensor(x):
            name = model._input_layers[i].name
            input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
            input_tensors[i] = input_tensor
            layer_map[x._keras_history[0]] = input_tensor._keras_history[0]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            # Get or create layer.
            if layer not in layer_map:
                new_layer = Layer.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                    kwargs['mask'] = computed_masks
                    computed_tensor = computed_tensors

                output_tensors = to_list(layer(computed_tensor, **kwargs))
                output_tensors = [tensor if tensor is not None else None for tensor in output_tensors]

                tensor_map.update(zip(reference_output_tensors, [(tensor, None) for tensor in output_tensors]))

    for x in model.outputs:
        if x not in tensor_map:
            raise AssertionError('Could not compute output ' + str(x))
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

By updating the function as above, it will handle the case where output masks are always None, preventing the error highlighted in the GitHub issue.