### Analysis:
1. The function `_clone_functional_model` is intended to clone a functional `Model` instance, creating new layers and weights instead of sharing existing ones.
2. The issue reported on GitHub indicates a failure when using `clone_model` on a model with multiple outputs.
3. The cause of the bug seems to be related to handling multiple outputs and the absence of mask support for certain layers like `Lambda`.
4. To fix the bug, we need to address how masks are handled during the cloning process, especially for layers without mask support.
5. Additionally, ensuring the correctness of output tensors and masks is crucial for successful model cloning.

### Fixing the Bug:
To fix the bug, we need to update the `_clone_functional_model` function to correctly handle the scenario where layers with multiple outputs without mask support are encountered. We should modify how masks are processed in such cases to prevent the reported error.

Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
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
        
    else:
        input_tensors = to_list(input_tensors)
        for orig_layer, new_input in zip(model._input_layers, input_tensors):
            layer_map[orig_layer] = new_input

    for orig, cloned in zip(model.inputs, input_tensors):
        tensor_map[orig] = (cloned, None)  # tensor, mask

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
            reference_output_tensors = node.output_tensors

            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks)) if has_arg(layer.call, 'mask') else [None] * len(output_tensors)

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    model_name = model.name if hasattr(model, 'name') else None
    return Model(input_tensors, output_tensors, name=model_name)
```

### Conclusion:
By updating the `_clone_functional_model` function as described above, we address the reported bug related to cloning functional models with multiple outputs. The correction should now allow the provided test case to pass without errors.