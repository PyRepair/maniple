### Analysis:
1. The buggy function `_clone_functional_model` is responsible for cloning a functional `Model` instance by creating new layers and weights instead of sharing the existing ones.
2. The error occurs when trying to clone a model that has multiple inputs and outputs without mask support.
3. The failing test `test_clone_functional_model_with_multi_outputs` tries to clone a model with multiple outputs, resulting in an assertion error due to the inability to compute the output tensor.
4. The GitHub issue provides a similar scenario where the `clone_model` function fails when dealing with a model with multiple outputs without mask support.
5. The root cause of the bug lies in the way the function handles masks for layers without mask support, causing the computed output masks to be set as `None`, leading to the assertion error.

### Bug Fix Strategy:
1. Modify the function to handle layers without mask support differently, ensuring proper masking is handled.
2. Update the cloning process to correctly compute and set the output masks for layers with multiple outputs.

### Bug Fix:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [K.placeholder(shape=layer.batch_input_shape, dtype=layer.dtype) for layer in model._input_layers]

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
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data] if any(x[1] is not None for x in computed_data) else None
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = [layer.compute_mask(x, mask) if mask is not None else None for x, mask in zip(computed_tensors, computed_masks)]
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
``` 

By updating the `_clone_functional_model` function to handle layers without mask support correctly, the bug can be fixed, and the failing test should pass without any assertion errors.