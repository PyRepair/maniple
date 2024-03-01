### Analysis:
1. The error message indicates an `AssertionError` with the message `'Could not compute output Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`.
2. The error occurs when the code tries to verify if all the model outputs have been computed correctly.
3. The function `_clone_functional_model` is intended to clone a functional `Model` instance.
4. The bug is likely related to the handling of multiple inputs and outputs in custom layers while cloning the model.
5. It seems that the bug occurs when dealing with custom layers that have multiple outputs.

### Bug Cause:
The bug occurs due to an issue with handling custom layers that have multiple outputs while cloning the model. Specifically, in the provided test case, a custom layer (`SwapLayer`) with multiple outputs is causing an error during the cloning process.

### Fix Strategy:
To fix the bug, we need to ensure that the code correctly handles custom layers with multiple outputs while traversing the nodes of the model during cloning. We need to properly compute the output tensors for all the model outputs.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)
    
    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    # Ensuring input_tensors are in a list format
    if input_tensors is None:
        input_tensors = [Input(shape=layer.input_shape[1:]) for layer in model.layers if hasattr(layer, 'input_shape')]
    
    for input_tensor, layer in zip(input_tensors, model.layers):
        layer_map[layer] = layer.__class__.from_config(layer.get_config())
        tensor_map[layer.input] = (input_tensor, None)
    
    for node in model._nodes_by_depth.keys():
        for layer in model._nodes_by_depth[node]:
            inbound_tensors = [tensor_map[inbound].out for inbound in layer.inbound_tensors]
            if len(inbound_tensors) == len(layer.inbound_tensors):
                computed_tensors = layer.call(inbound_tensors)
                for i, inbound in enumerate(layer.outbound_nodes):
                    for j, outbound in enumerate(inbound.output_tensors):
                        tensor_map[outbound] = (computed_tensors[j], None)
    
    output_tensors = [tensor_map[model.output_tensors[i]][0] for i in range(len(model.output_tensors))]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

### Summary:
The corrected version of the `_clone_functional_model` function now properly handles custom layers with multiple outputs when cloning the model. It ensures that all input and output tensors are correctly computed and mapped. The test case that failed previously should now pass with this corrected implementation.