In the provided buggy function `_clone_functional_model`, the issue lies in the incorrect handling of the input tensors when cloning a model with multiple outputs. The function fails to correctly create and map the input layers when dealing with multiple outputs, leading to the failure of the test `test_clone_functional_model_with_multi_outputs`.

To fix this bug, we need to ensure that the input tensors are properly handled when creating the new model instance. Specifically, we need to correctly map the input tensors to the corresponding layers and handle the case where the model has multiple outputs.

Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
      
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    else:
        input_tensors = to_list(input_tensors)
        assert len(input_tensors) == len(model._input_layers), "Number of input tensors does not match the number of input layers"
        for i, layer in enumerate(model._input_layers):
            input_tensor = input_tensors[i]
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    def construct_model_from_input_layer(input_layer):
        input_tensors = [input_layer.input]
        layer = input_layer
        while True:
            if layer in layer_map:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    break
            else:
                raise ValueError("Layer mapping missing for layer: ", layer)
            input_tensors.append(layer.input)

        for node in model._container_nodes.values():
            for idx, inbound_layer, node_index, tensor_index, _ in node.inbound_layers:
                if inbound_layer not in layer_map:
                    inbound_layer = layer_map[inbound_layer]
                inbound_node = inbound_layer._inbound_nodes[node_index]
                inbound_tensor = inbound_node.output_tensors[tensor_index]
                tensor_map[inbound_tensor] = (inbound_tensor, None)  # tensor, mask

        output_tensors = [tensor_map[o][0] for o in model.outputs]
        return Model(input_tensors, output_tensors, name=model.name)

    return construct_model_from_input_layer(model._input_layers[0])
```

By incorporating the modifications mentioned above, the corrected `_clone_functional_model` function should now be able to correctly clone a functional model with multiple outputs and pass the failing test `test_clone_functional_model_with_multi_outputs`.