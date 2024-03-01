### Analysis:
The issue reported on GitHub indicates that when using `clone_model()` with `multi_gpu_model()` and `cpu_relocation=True`, an error "Could not compute output Tensor" is raised. The traceback suggests that the bug lies within the `clone_model()` function in the `keras.models` module. The specific issue seems to be related to the behavior of Lambda layers and the handling of masks during cloning.

### Potential Error Locations:
1. Line 153: `output_masks = to_list(layer.compute_mask...)` always returning `None` for Lambda layers without mask support.
2. Line 157: Zip operation on `reference_output_tensors` and `output_tensors` where output_masks might be `None`.

### Cause of the Bug:
The bug occurs because Lambda layers do not support masks, leading to `output_masks` being consistently `None`. This discrepancy in the number of masks expected causes the "Could not compute output Tensor" error.

### Strategy for Fixing the Bug:
To fix the bug, we need to handle the case of Lambda layers not supporting masks appropriately in the cloning process to prevent the error from being raised.

### Corrected Version of the Function:
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
            layer_map[layer] = input_tensor._keras_history[0]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

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
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                tensor_map.update(zip(reference_output_tensors, output_tensors))

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the `_clone_functional_model` function should address the issue reported on GitHub by handling Lambda layers without mask support correctly during the model cloning process.