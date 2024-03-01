### Analysis:
- The error message indicates an `AssertionError` at line 166 of the `models.py` file, where the function `_clone_functional_model` is implemented.
- The `assert` statement checks if the output tensor `x` is present in the `tensor_map`. If it is not present, an AssertionError is raised with the message `'Could not compute output ' + str(x)`.
- The specific tensor causing the error is `swap_layer_1/Identity:0`, which means that during the clone operation, the mapping for this tensor is missing in the `tensor_map`.

### Potential Error Locations:
1. The creation and update of `tensor_map` might be incorrect.
2. The logic for gathering and calling the new layers might be missing or incorrect.
3. Potential issues with handling different layer types may exist.

### Bug Cause:
The bug is caused by the missing entry for the output tensor `swap_layer_1/Identity:0` in the `tensor_map` dictionary during the cloning process. This indicates that either the tensor is not mapped correctly, or it is not processed as expected when creating new layers.

### Strategy for Fixing the Bug:
1. Ensure that all output tensors are correctly mapped to their corresponding tensors in the `tensor_map`.
2. Verify that all layers are appropriately cloned and called to avoid missing tensors during the cloning process.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_layers = []
        input_tensors = []
        layer_map = {}  # Clear previous layer map entries
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            input_layer = input_tensor._keras_history[0]
            layer_map[layer] = input_layer
        
    for x, y in zip(model._input_layers, input_tensors):
        tensor_map[x] = (y, None)  # Add input tensors to tensor map
    
    for depth in model._nodes_by_depth:
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            
            if layer not in layer_map:
                # Clone layer.
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            layer = layer_map[layer]
            
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            
            computed_data = []  # List of tuples (input, mask).
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
            
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments or {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                
                if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                    kwargs['mask'] = computed_masks
                
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                
                # Update tensor_map.
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)
    
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

### Changes Made:
1. Clear previous entries in `layer_map` before creating new input layers.
2. Validate that the output tensors are mapped correctly and present in the `tensor_map`.
3. Refactor the loop for processing nodes to correctly process and map input and output tensors.

By applying the suggested corrections and ensuring proper mapping of input and output tensors in the clone process, the fixed version of the `_clone_functional_model` function should now pass the failing test.