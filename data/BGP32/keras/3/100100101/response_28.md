### Bug Explanation
The bug in the `_clone_functional_model` function arises from the incorrect handling of input tensors when cloning a model with multiple outputs. Specifically, the function fails to correctly map the reference output tensors to the newly computed output tensors, leading to incorrect model cloning.

### Bug Location
The main issue lies in how the function handles the mapping of reference output tensors to the computed output tensors within the loop iterating over nodes in the model.

### Bug Fix Strategy
To fix the bug, we need to ensure that the mapping between reference output tensors and computed output tensors is correctly maintained throughout the function. This involves updating the `tensor_map` dictionary with the correct tensor mappings based on the computed output tensors.

### Corrected Version of the Function

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            input_layers.append(layer)
            layer_map[layer] = input_tensor
            
    else:
        input_tensors = to_list(input_tensors)
        input_layers = [x._keras_history[0] if K.is_keras_tensor(x) else None for x in input_tensors]
        for original_layer, tensor in zip(model._input_layers, input_tensors):
            layer_map[original_layer] = tensor
    
    for original_tensor, tensor in zip(model.inputs, input_tensors):
        tensor_map[original_tensor] = (tensor, None)
    
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            
            layer = layer_map[layer]
            
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
            
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                
                computed_tensors = [x for x, _ in computed_data]
                computed_masks = [mask for _, mask in computed_data]
                
                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = computed_masks
                
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                
                for ref_out_tensor, new_out_tensor, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[ref_out_tensor] = (new_out_tensor, mask)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected function ensures that the mapping between input tensors and output tensors is accurately maintained during the model cloning process. This version should now pass the failing test case provided.