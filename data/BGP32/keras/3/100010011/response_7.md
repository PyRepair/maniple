### Analysis:
- The buggy function `_clone_functional_model` is supposed to clone a functional `Model` instance while creating new layers and new weights instead of sharing the weights of the existing layers.
- The failing test `test_clone_functional_model_with_multi_outputs` is trying to clone a `Model` with multiple outputs but encountering an error during the process.
- The error message indicates that the assertion for computing the model outputs fails due to a problem with the output tensor.
- The GitHub issue describes a similar scenario where the user encounters an error when using `clone_model` with a `Lambda` layer that does not support masks, leading to the error message.

### Potential Error Location:
- The issue might be related to how the function handles layers without mask support, such as the `Lambda` layer, causing the output masks to be `None`.
- The error could be due to incorrect handling of output tensors and masks in the cloning process, specifically when dealing with layers that do not support masks.

### Bug Cause:
- The bug occurs because the function does not handle layers without mask support correctly, leading to the assertion error when trying to compute the output tensor.

### Suggested Fix Strategy:
- Ensure that layers without mask support are handled properly during the cloning process, avoiding issues with output tensors and masks.
- Modify the function to handle cases where layers do not support masks appropriately to prevent the assertion error.

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
        for i, layer in enumerate(model._input_layers):
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
            input_layers.append(input_tensor)
        for _original, _cloned in zip(model._input_layers, input_layers):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                layer_map[model._input_layers[i]] = input_tensor
                input_tensors[i] = input_tensor

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

                if has_arg(layer.call, 'mask'):
                    if 'mask' not in kwargs:
                        kwargs['mask'] = [x[1] for x in computed_data if x[1] is not None]

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

### Summary:
The corrected version of the `_clone_functional_model` function now properly handles layers without mask support during the cloning process, preventing errors related to output tensors and masks. This should resolve the issue mentioned in the GitHub report and allow the function to work correctly when dealing with models with multiple outputs.