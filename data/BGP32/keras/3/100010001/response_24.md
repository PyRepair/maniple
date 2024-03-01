### Analysis:
The error occurs in the `_clone_functional_model` function when attempting to access an output tensor that was not computed during the cloning process. This results in the assertion error indicating that the function was unable to compute the output tensor.

### Bug:
The bug in the `_clone_functional_model` function lies in the logic inside the loop that iterates over nodes in the reference model. The function fails to properly handle cases where the output tensors of a node are not available in the `tensor_map`.

### Fix:
To fix the bug, we need to ensure that when processing each node, we only attempt to call the layer if all the input tensors are available in the `tensor_map`. If any input tensor is missing, we should skip calling the layer and move on to the next node.

### Corrected Version:
Below is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    
    input_layers = [x._keras_history[0] for x in input_tensors]
    for original, cloned in zip(model._input_layers, input_layers):
        layer_map[original] = cloned

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if all(x in tensor_map for x in node.input_tensors):
                if layer not in layer_map:
                    new_layer = layer.__class__.from_config(layer.get_config())
                    layer_map[layer] = new_layer
                else:
                    new_layer = layer_map[layer]
                    if isinstance(new_layer, InputLayer):
                        continue

                computed_data = [tensor_map[x] for x in node.input_tensors]

                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(new_layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                    if has_arg(new_layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks

                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                if has_arg(new_layer, 'compute_mask'):
                    output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))
                else:
                    output_masks = [None] * len(output_tensors)

                for output, output_tensor, output_mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[output] = (output_tensor, output_mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    for output in model.outputs:
        assert output in tensor_map, 'Could not compute output ' + str(output)

    return Model(input_tensors, output_tensors, name=model.name)
```

After applying the fix, the corrected `_clone_functional_model` function should now properly clone the functional model and compute the output tensors.