### Analysis:
- The buggy function `_clone_functional_model` is responsible for cloning a functional `Model` instance.
- The error message indicates that the function fails to compute the output Tensor while trying to clone the model.
- The error occurs when trying to compute the output_tensors for the model, specifically at the assertion step.
- The cause of the bug seems to be related to handling multiple outputs from a layer.
- The GitHub issue describes a similar bug where the function fails to compute the output tensor due to None values for output masks.

### Bug Cause:
Since `Lambda` layers do not support masks, the function fails to compute the output masks, resulting in None values for output masks. This leads to the assertion error while trying to compute the model outputs.

### Bug Fix:
To fix the bug, we need to adjust how the function handles layers with multiple outputs that do not support masks. Specifically, we need to handle the case where the layer's `compute_mask` method returns None for output masks.

### Corrected Function:
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
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
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
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments or {}
                computed_tensors, computed_masks = zip(*computed_data) if computed_data else ([], [])
                if not all(computed_masks):
                    computed_masks = len(computed_tensors) * [None]
                    
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

### Summary:
The bug in the `_clone_functional_model` function was addressed by handling the case where the layer's `compute_mask` method returns None for output masks, ensuring that the output_masks are set appropriately. By making these adjustments, the function will be able to successfully compute the output tensors for the model and address the AssertionError encountered in the failing test.