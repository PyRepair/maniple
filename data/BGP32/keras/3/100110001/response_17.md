### Analysis
The function `_clone_functional_model` is used to clone a functional Model instance in Keras. The failing test is trying to clone a model with multiple outputs, indicating an issue with the handling of multiple outputs in the cloning process.

### Issue
The bug in the `_clone_functional_model` function arises from the handling of multiple outputs in the model. The function fails to correctly handle models with multiple outputs, leading to an assertion error when trying to compute the outputs in the cloning process.

### Solution
To fix the bug, we need to ensure that the function correctly handles multiple outputs when cloning a model. This involves updating how the output tensors are computed and stored in the `tensor_map`.

### The corrected function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)
    
    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        input_tensors = [Input(shape=layer.output.shape[1:]) for layer in model.layers if isinstance(layer, InputLayer)]
        input_tensors += [Input(batch_shape=layer.batch_input_shape[1:], dtype=layer.dtype, name=layer.name) for layer in model.layers if isinstance(layer, InputLayer)]
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask
    
    for layer in model.layers:
        if isinstance(layer, InputLayer):
            continue
        
        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer
    
    for node in model._nodes_by_depth.values():
        for layer in node:
            new_layer = layer_map[layer]
            reference_input_tensors = layer._inbound_nodes[0].input_tensors
            
            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in reference_input_tensors if x in tensor_map]
            
            if len(computed_data) == len(reference_input_tensors):
                kwargs = layer.get_config()
                computed_tensors, computed_masks = zip(*computed_data)
                if has_arg(new_layer.call, 'mask'):
                    kwargs['mask'] = [mask for tensor, mask in computed_data]
                outputs = new_layer(computed_tensors, **kwargs)
                for i, x in enumerate(layer._inbound_nodes[0].output_tensors):
                    tensor_map[x] = (outputs[i], None)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the function now correctly handles models with multiple outputs and should pass the failing test.