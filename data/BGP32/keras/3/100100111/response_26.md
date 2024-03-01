### Analysis:
1. The purpose of the `_clone_functional_model` function is to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones.
2. The function seems to have issues with creating new input layers and maintaining references to existing layers.
3. The failing test case `test_clone_functional_model_with_multi_outputs` creates a model with multiple inputs and outputs and then attempts to clone it using the `clone_model` function. The issue arises due to incorrect handling of input and output tensors during the cloning process.
4. The GitHub issue posted is related to a similar problem where the user encountered an error when using `clone_model` with multi-GPU processing, leading to an assertion error due to improper computation of output tensors.

### Bug Fix Strategy:
1. Address the handling of input tensors, particularly when creating placeholders or using existing tensors.
2. Ensure that the mapping between original and new layers is correct.
3. Verify the computation of output tensors and masks to prevent errors during the cloning process.

### Corrected Function:
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
            layer_map[layer] = input_tensor._keras_history[0]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                layer_map[x._keras_history[0]] = input_tensor._keras_history[0]
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
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    kwargs['mask'] = computed_masks if has_arg(layer.call, 'mask') else None
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                for x, (y, mask) in zip(reference_output_tensors, zip(output_tensors, output_masks)):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected function addresses the issues related to creating new input layers, mapping layers correctly, and computing output tensors during the cloning process, as per the expected behavior described in the failing test case and the GitHub issue.