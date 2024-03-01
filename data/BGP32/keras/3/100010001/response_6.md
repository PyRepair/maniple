### Bug Analysis:
1. The error message indicates that the function `clone_model` is failing due to an assertion error. The assertion error is raised because the code is unable to compute the output tensors for the model during the process of cloning.
2. The key issue lies in the computation of the output tensors, specifically in the loop where the code iterates over model outputs and checks if the corresponding tensors are available in the `tensor_map` dictionary.

### Bug Fix Strategy:
1. The issue arises from the fact that during the transformation process, the expected tensors are not properly stored in the `tensor_map` dictionary.
2. To address this bug, the code must ensure that each output tensor generated during the cloning process is correctly matched and stored in the `tensor_map`.
3. The computation of output tensors should be closely monitored to ensure that all the necessary tensors are accurately assigned for further mapping and model reconstruction.

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
        input_layers = []
        input_tensors = []
        
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        
        for original_layer, cloned_layer in zip(model._input_layers, input_tensors):
            layer_map[original_layer] = cloned_layer
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask
    
    for node in model._nodes_by_depth:
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
            
            for x, y, mask in zip(reference_output_tensors, output_tensors, computed_masks):
                tensor_map[x] = (y, mask)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By following the corrected version of the `_clone_functional_model` function provided above, the bug causing the function to fail should be resolved. This corrected version ensures that the output tensors are correctly computed and matched in the `tensor_map` dictionary during the cloning process.