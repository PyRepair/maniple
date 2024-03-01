### Analysis:
1. The `clone_model` function in the failing test `test_clone_functional_model_with_multi_outputs` is calling the `_clone_functional_model` function in the Keras models module.
2. The error message indicates an assertion error where the output tensor of the model is not found in the `tensor_map`.
3. The `tensor_map` dictionary is supposed to map input tensors to their corresponding computed tensors.
4. The issue seems to be related to the handling of multiple output tensors in the `SwapLayer` and `Lambda` layers.

### Bug Explanation:
The bug lies in the handling of multiple output tensors. The original implementation only considered a single output tensor per layer, leading to compatibility issues when dealing with layers that have multiple output tensors.

### Bug Fix:
To fix this bug, we need to update the function `_clone_functional_model` to handle multiple output tensors correctly.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
    else:
        input_tensors = to_list(input_tensors)

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

            reference_input_tensors = node.input_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                    kwargs['mask'] = computed_masks

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
``` 

This corrected version includes the necessary adjustments to handle multiple output tensors and should pass the failing test case.