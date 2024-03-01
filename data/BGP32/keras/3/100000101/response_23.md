The bug in the provided function is due to the incorrect construction of the `layer_map` and `tensor_map` dictionaries. These dictionaries are used to store mappings between original layers/tensors and newly created layers/tensors. However, there are issues with how these mappings are being correctly updated during the model-cloning process.

To fix the bug, we need to make sure that the mappings in `layer_map` and `tensor_map` are correctly established and updated for all layers and tensors in the model during the cloning process.

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
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    
    for orig_input_tensor, new_input_tensor in zip(model.inputs, input_tensors):
        tensor_map[orig_input_tensor] = (new_input_tensor, None)  

    for depth in range(max(model._nodes_by_depth.keys()), -1, -1):
        nodes = model._nodes_by_depth.get(depth, [])
        for node in nodes:
            layer = node.outbound_layer
            
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []  
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    if has_arg(new_layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = None
                    output_tensors = to_list(new_layer(computed_tensor, **kwargs))
                    output_masks = to_list(new_layer.compute_mask(computed_tensor, None))
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                    if has_arg(new_layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = None
                    output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                    output_masks = to_list(new_layer.compute_mask(computed_tensors, None))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

In the corrected version, we iterate over the nodes in the model in a descending order of depth, ensuring that dependencies are resolved correctly. We update the `tensor_map` and `layer_map` dictionaries accurately during the cloning process. This should fix the bug and ensure that the function behaves correctly for the provided input cases.