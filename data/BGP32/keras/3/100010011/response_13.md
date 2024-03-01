### Analysis:
The error message indicates that the `clone_model` function encounters an `AssertionError` because it fails to compute the output tensor during the model cloning process. This error is related to an issue reported on GitHub where the user encounters a similar problem when using `clone_model` with multi-layer outputs.

### Bug Identification:
The bug seems to originate from the `_clone_functional_model` function. Specifically, when handling multiple outputs in the model, the function fails to correctly compute and assign the output tensors to the `tensor_map`.

### Bug Cause:
1. The function is not correctly handling the case where a layer produces multiple outputs without mask support.
2. The issue with Lambda layers not supporting masks causes the `output_masks` to be None, leading to an assertion error.

### Bug Fix Strategy:
1. Ensure that when a layer produces multiple outputs, the function handles them correctly in terms of computing and assigning output tensors.
2. Address the issue related to Lambda layers and their lack of mask support to prevent `output_masks` from being None.

### Bug-fixed Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                                 sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    nodes = []
    for node in reversed(model._nodes_by_depth.values()):
        nodes.extend(node)
    
    for node in nodes:
        layer = node.outbound_layer
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
    
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
            
            output_tensors = layer(computed_tensors, **kwargs)
            output_tensors = to_list(output_tensors)
            
            for x, y in zip(reference_output_tensors, output_tensors):
                tensor_map[x] = (y, None)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

Now the corrected version of the `_clone_functional_model` function should handle multiple outputs correctly and avoid the `AssertionError` that was occurring in the failing test.