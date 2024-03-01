### Analysis:
The buggy function `_clone_functional_model` is responsible for cloning a functional Keras model. The issue described in the GitHub problem is related to an error message "Could not compute output Tensor" when using `clone_model()` to clone a model with multiple outputs. The bug occurs due to the fact that the layer `Lambda` used in the model does not support masks, leading to `layer.compute_mask(...)` always returning `None`, even though it is expected to return `[None, None]`.

### Bug Location:
The bug seems to be related to the handling of masks with layers that do not support masks, specifically in the logic for computing output masks in the `_clone_functional_model` function.

### Cause of the Bug:
1. The bug occurs due to the way output masks are handled when iterating over the reference model's nodes.
2. The function expects `output_masks` to be `[None, None]`, but due to the absence of mask support in the `Lambda` layer, it always returns `None`.
3. This mismatch in expected versus actual output masks causes the "Could not compute output Tensor" error.

### Strategy for Fixing the Bug:
To fix the bug, we need to adjust the logic for handling output masks in the `_clone_functional_model` function when cloning models with layers that do not support masks. We should handle the case where the layer's `compute_mask` function returns `None`.

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
        input_tensors = [Input(batch_shape=layer.shape) for layer in model.input_layers]

    for original_input, new_input in zip(model.input_layers, input_tensors):
        layer_map[original_input] = new_input

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
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

            computed_data = []
            for x in node.input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                
                computed_tensors = [x[0] for x in computed_data]
                
                if has_arg(layer.call, 'mask') and all(x[1] is not None for x in computed_data):
                    kwargs['mask'] = [x[1] for x in computed_data]
                    
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        if x not in tensor_map:
            raise ValueError('Could not compute output ' + str(x))
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

By updating the logic for handling masks in the cloning process, the corrected version of the `_clone_functional_model` function should now be able to clone models with multiple outputs without the "Could not compute output Tensor" error.