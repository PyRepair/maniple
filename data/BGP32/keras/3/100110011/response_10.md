### Analysis:
1. The bug occurs in the `_clone_functional_model` function in the `keras/models.py` file.
2. The error message indicates that the assertion `assert x in tensor_map` fails, leading to the error `Could not compute output Tensor(...)`.
3. The issue reported on GitHub suggests that the error is related to the use of multi_gpu_model with `cpu_relocation=True`.
4. The error is caused by the Lambda layer not supporting masks, leading to `output_masks` being `None` instead of the expected `[None, None]`.

### Bug Cause:
The bug occurs when the Lambda layer is used with multiple outputs without mask support. This results in missing data in the `output_masks` list, causing the assertion failure.

### Fix Strategy:
To fix the bug, we need to handle cases where the output masks are not generated due to the Lambda layer not supporting masks. We can adjust the logic to account for this scenario.

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
            layer_map[layer] = input_tensor
        for original_layer, cloned_layer in zip(model._input_layers, input_tensors):
            layer_map[original_layer] = cloned_layer
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                layer_map[original_input_layer] = input_tensor
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for layer in model.layers:
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer

    for node in model._nodes_by_depth:
        layer = node.outbound_layer
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer

    for node in model._nodes:
        reference_input_tensors = node.input_tensors
        reference_output_tensors = node.output_tensors
        computed_data = []
        for x in reference_input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])

        if len(computed_data) == len(reference_input_tensors):
            kwargs = node.arguments if node.arguments else {}
            computed_tensors = [x[0] for x in computed_data]
            computed_masks = [x[1] for x in computed_data if x[1] is not None]
            output_tensors = to_list(layer(computed_tensors, **kwargs))
            output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
            
            for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(to_list(input_tensors), output_tensors, name=model.name)
```

This corrected function should address the issue and allow the failing test to pass successfully.