Based on the analysis of the buggy function and the failing test, it seems that the bug is located in the `_clone_functional_model` function. The error occurs when the output tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)` is not found in the `tensor_map`, causing the assertion to fail.

It appears that the issue is related to how the function handles the computation and mapping of output tensors for the cloned model. The incorrect handling of input layers and nodes may also contribute to the incorrect behavior of the function.

To fix the bug, the function needs to be refactored to properly handle input layers and nodes, compute output tensors, and manage the layer mapping and caching. Additionally, the inconsistency in handling input layers, input tensors, and input layers should be addressed to ensure the correct behavior of the cloned model.

Here's the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    input_layers = []
    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.input.shape[1:], dtype=layer.input.dtype) for layer in model.input_layers]

    for original_layer, input_tensor in zip(model.input_layers, input_tensors):
        layer_map[original_layer] = input_tensor

    for node in model.nodes:
        layer = node.outbound_layer

        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
            
        layer = layer_map[layer]
        if isinstance(layer, InputLayer):
            continue
        
        reference_input_tensors = node.input_tensors
        computed_data = []
        
        for x in reference_input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])

        if len(computed_data) == len(reference_input_tensors):
            if node.arguments:
                kwargs = node.arguments
            else:
                kwargs = {}

            output_tensors = to_list(layer(*[x[0] for x in computed_data], **kwargs))
            for x, y in zip(node.output_tensors, output_tensors):
                tensor_map[x] = y

    output_tensors = [tensor_map[x] for x in model.output_tensors]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version aims to properly handle input layers, compute output tensors, and manage the layer mapping and caching. It should pass the failing test and resolve the issue reported in the GitHub bug.