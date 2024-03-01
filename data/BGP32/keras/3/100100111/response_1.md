### Analysis:
1. The `clone_model` function is used to replicate a functional `Model` instance. The buggy function `_clone_functional_model` aims to create new layers and weights instead of sharing existing ones.
2. The bug seems to be related to the iteration over the model nodes and handling of input tensors.
3. The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple inputs and outputs, including a Lambda layer and a custom SwapLayer. When attempting to clone the model using `clone_model`, the function fails to correctly map the input and output tensors, leading to the assertion errors as the output tensors are not correctly computed.
4. To fix the bug, the function `_clone_functional_model` should properly map the input and output tensors for each layer, ensuring that the computed data is correctly associated with the tensors. Additionally, the handling of multiple inputs and outputs should be revised to match the model structure.
5. By modifying the logic for mapping tensors and ensuring that the correct input/output relationships are maintained, the bug can be fixed.

### Correction:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.input_shape, dtype=layer.dtype) for layer in model._input_layers]

    for original, new in zip(model._input_layers, input_tensors):
        layer_map[original] = new

    for node, depth in model._iterate_nodes():
        inbound_layers = node.inbound_layers
        reference_inbound_nodes = node.inbound_nodes

        inputs = []
        for layer, node_index, tensor_index in reference_inbound_nodes:
            tensor = inbound_layers[node_index].output
            if tensor in tensor_map:
                inputs.append(tensor_map[tensor][0])
            else:
                inputs.append(tensor)

        kwargs = node.arguments if node.arguments else {}
        output_tensor = layer_map[node.outbound_layer](inputs, **kwargs)
        tensor_map[node.outbound_node] = (output_tensor, None)

    output_tensors = [tensor_map[out_node][0] for out_node in model.output_layers]
    return Model(inputs=input_tensors, outputs=output_tensors, name=model.name)
```

Now, the corrected `_clone_functional_model` function should correctly replicate the model structure and handle models with multiple inputs and outputs without causing assertion errors.