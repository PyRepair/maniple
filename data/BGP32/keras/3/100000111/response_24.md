### Analysis
The bug seems to occur due to the issue with the computation of output masks during the cloning of the model in the `clone_functional_model` function. The issue described in the GitHub post highlights the specific problem when using `clone_model` and `multi_gpu_model` with `cpu_relocation=True`. The issue arises from the fact that the `Lambda` layer in the model does not support using masks, leading to the computation of `output_masks` as `[None]` when it should be `[None, None]`.

### Bug Explanation
The bug originates from the incorrect computation of `output_masks` due to the non-support of masks by the `Lambda` layer. This leads to the error when trying to clone the model with multiple outputs. The incorrect calculation of `output_masks` fails to satisfy the expected values, causing the assertion error.

### Bug Fix Strategy
To fix the bug, we need to ensure that the `output_masks` are computed properly for each layer in the model, considering any potential lack of support for masks in specific layers like `Lambda`. By modifying the calculation of `output_masks` and managing the behavior for layers lacking mask support, we can address the issue.

### Corrected Function
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
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                                sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
        layer_map = {original_layer: new_layer for original_layer, new_layer in zip(model._input_layers, input_tensors)}
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                _original = input_tensors[i]._keras_history[0]
                newly_created = input_tensor._keras_history[0]
                layer_map[_original] = newly_created
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    depth_keys = sorted(model._nodes_by_depth.keys(), reverse=True)
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
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                if hasattr(layer, 'compute_mask') and has_arg(layer.compute_mask, 'tensor'):
                    computed_masks = [x[1] for x in computed_data]
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                else:
                    output_masks = [None] * len(output_tensors)
                
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    assert all(x in tensor_map for x in model.outputs), 'Could not compute output'

    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version includes adjustments to compute `output_masks` appropriately, considering the mask support for layers and handling layers like `Lambda` correctly. The function now aligns with the expected values and should no longer raise the reported error.