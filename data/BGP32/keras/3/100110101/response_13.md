### Bug Analysis:
1. The buggy function `_clone_functional_model` is designed to clone a functional `Model` instance, creating new layers and weights instead of sharing existing ones.
2. The function iterates through the nodes of the input model, creating new layers and connecting them based on the node connections.
3. The error occurs when the function tries to compute the output tensors for the new model but fails to do so, leading to an assertion error.

### Bug Explanation:
1. In the failing test case `test_clone_functional_model_with_multi_outputs`, a model is created with multiple outputs.
2. When the function `clone_model` is called in the test case, it internally calls `_clone_functional_model` to generate a clone of the model.
3. The `_clone_functional_model` function fails to correctly compute the output tensors for the new model due to problems with how layers are mapped and connected.

### Bug Fix Strategy:
1. Ensure that the input tensors map correctly to the corresponding layer nodes.
2. Make sure that the new layers are cloned properly and connected based on the node connections.
3. Update the tensor map correctly to track the connections between input and output tensors.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
                         for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

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

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = [tensor_map[x] for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                    kwargs['mask'] = computed_masks
                    
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

After integrating this corrected version of the `_clone_functional_model` function, the failing test case should pass successfully without AssertionError.