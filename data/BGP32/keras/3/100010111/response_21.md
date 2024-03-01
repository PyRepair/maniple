### Analysis:
1. The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and new weights.
2. The error message occurs when the function fails to compute the output tensors for the cloned model.
3. The error message indicates that a specific tensor (`Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`) could not be computed.
4. The issue reported on GitHub suggests that the error arises when using `clone_model()` in conjunction with `multi_gpu_model()` and `cpu_relocation=True`.
5. The issue involves a Lambda layer with multiple outputs and no mask support, causing the function to not compute the output correctly.

### Bug:
The bug arises from the function's inability to handle multiple outputs from a Lambda layer without mask support, leading to the failure of computing the output tensors.

### Fix strategy:
To resolve the bug, we need to modify the logic for handling multiple outputs from layers without mask support, especially in cases involving Lambda layers.

### Corrected function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    input_layers = []
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                               sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    
    for new_input_layer, original_input_layer in zip(input_tensors, model._input_layers):
        layer_map[original_input_layer] = new_input_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in reversed(range(len(model._nodes_by_depth))):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            if isinstance(new_layer, InputLayer):
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
                if len(computed_data) == 1:
                    computed_tensors = computed_tensors[0]
                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                
                if len(reference_output_tensors) == 1:
                    output_tensors = [output_tensors]

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By updating the handling of multiple outputs and adding the missing connection between `input_layers` and `input_tensors`, the corrected function should now correctly compute the output tensors for the cloned model with multiple outputs.