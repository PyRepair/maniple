The bug in the `_clone_functional_model` function seems to be related to the input handling and layer mapping. 
The function fails to correctly handle the creation of input tensors and mapping of input layers when they are not provided in the `input_tensors` parameter.

To fix the bug, we need to ensure that the input layers and input tensors are correctly handled and mapped to newly created input layers. We should also update the `input_layers` list based on the input tensors for the sequential model.

Here is the corrected version of the function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    
    if input_tensors is not None:
        input_tensors = to_list(input_tensors)
    else:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
    
    for original_layer, input_tensor in zip(model._input_layers, input_tensors):
        layer_map[original_layer] = input_tensor
        
    for layer, nodes in model._nodes_by_depth.items():
        for node in nodes:
            outbound_layer = node.outbound_layer

            if outbound_layer not in layer_map:
                new_layer = outbound_layer.__class__.from_config(outbound_layer.get_config())
                layer_map[outbound_layer] = new_layer

            inbound_tensors = [tensor_map[tensor][0] for tensor in node.input_tensors]
            kwargs = node.arguments if node.arguments else {}
            output_tensors = to_list(layer_map[outbound_layer](inbound_tensors, **kwargs))

            for original_tensor, output_tensor in zip(node.output_tensors, output_tensors):
                tensor_map[original_tensor] = (output_tensor, None)

    output_tensors = [tensor_map[output][0] for output in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version should now correctly handle the creation of input tensors, mapping of layers, and computing the output tensors based on input tensors. It accommodates the expected input and output values provided in the test case.