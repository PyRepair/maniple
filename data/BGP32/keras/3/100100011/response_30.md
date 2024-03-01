After analyzing the provided buggy function `_clone_functional_model` and the failing test `test_clone_functional_model_with_multi_outputs`, we can see that the bug lies in the method's handling of multiple output tensors. This issue is related to a GitHub issue where the user encountered an error when using `clone_model()` with a model that has multiple outputs from a layer that does not support masks. The bug causes the `clone_model()` function to fail to compute the output tensors correctly, leading to an assertion error.

To fix this bug, we need to adjust the logic in the `_clone_functional_model` function to correctly handle multiple outputs from a layer that does not support masks. Specifically, we need to ensure that the `output_masks` are handled properly when processing multiple output tensors.

Here's the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
                         for layer in model._input_layers]
    
    for original, cloned in zip(model._input_layers, input_tensors):
        layer_map[original] = cloned
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # Initialize mask as None
    
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
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
    
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
    
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(layer(computed_tensors, **kwargs))
    
                computed_tensors = list(computed_tensors)
                computed_masks = [None] * len(computed_tensors)  # Masks are None for multiple outputs
    
                tensor_map.update({x:y for x, y in zip(node.output_tensors, output_tensors)})
    
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the function should address the bug reported in the GitHub issue and ensure that the `clone_model` function works correctly with multiple outputs from layers that do not support masks.