### Analysis:
- The buggy function `_clone_functional_model` is responsible for cloning a functional Keras `Model` instance.
- The error message indicates that the bug is occurring at line 166 where an `AssertionError` is raised due to the output tensor not being found in the `tensor_map`.
- The GitHub issue provides a similar scenario where `clone_model` is causing issues with multi outputs and a layer that does not support masks, resulting in output masks being `None`.
- The issue arises due to handling multiple outputs and the lack of support for masks in certain layers like `Lambda`.

### Bug Cause:
- The bug occurs because the code does not handle multiple outputs properly, leading to issues where the output tensor is not present in the `tensor_map`.
- Additionally, the code does not properly handle the case where layers do not support masks, causing issues during the computation of outputs.

### Fix Strategy:
- Modify the code to correctly handle multiple outputs and the absence of masks for certain layers.
- Ensure that the output tensors are properly computed and added to the `tensor_map`.

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
            layer_map[layer] = input_tensor
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, input_tensor in enumerate(input_tensors):
            if K.is_keras_tensor(input_tensor):
                layer_map[input_tensor._keras_history.layer] = input_tensor
            else:
                name = model._input_layers[i].name
                input_layer = Input(tensor=input_tensor, name='input_wrapper_for_' + name)
                layer_map[input_tensor] = input_layer
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    for depth in list(model._nodes_by_depth.keys())[::-1]:
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_config = layer.get_config()
                new_layer = layer.__class__.from_config(new_config)
                layer_map[layer] = new_layer
            layer = layer_map[layer]
            
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
                    
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data] if len(computed_data[0]) == 2 else None
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                tensor_map.update({x: (y, mask) for x, y, mask in zip(reference_output_tensors, output_tensors, computed_masks)})

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

Executing the corrected function with the provided failing test case should now pass without raising any assertion errors.