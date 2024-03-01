### Bug Analysis:
The bug occurs when using `clone_model` in a scenario with a model containing a layer that has multiple outputs without mask support. The error arises from line 157 of the `keras/models.py` file, where the script fails to compute the output tensor properly due to the absence of masks. This situation causes an assertion error, where the output tensor cannot be computed correctly, leading to failures in the model cloning process.

### Potential Bug Location:
The issue seems to originate in the handling of masks for layers with multiple outputs in the `_clone_functional_model` function in the `keras/models.py` file.

### Bug Cause:
1. The script does not handle cases where layers with multiple outputs lack mask support.
2. Due to this, the output_masks are set to `None`, causing issues when trying to compute the output tensors.

### Strategy for Fixing the Bug:
1. Check for the presence of masks before assigning them to output_masks.
2. Update the logic to handle layers with multiple outputs that do not support masks.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.input_spec.shape[1:]) for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in range(len(model._nodes_by_depth)):
        nodes = model._nodes_by_depth.get(depth, [])
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

            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                output_tensors = to_list(layer(computed_data[0][0], **kwargs))
                tensor_map.update({x: (y, None) for x, y in zip(reference_output_tensors, output_tensors})

    output_tensors = [tensor_map.get(x, None) for x in model.outputs]
    assert all(output_tensors), 'Could not compute output ' + ', '.join(str(x) for x in model.outputs)

    return Model(input_tensors, output_tensors, name=model.name)
```

With this corrected version of the function, the bug related to the assertion error should be resolved, and the function should function correctly in scenarios with layers having multiple outputs without mask support.