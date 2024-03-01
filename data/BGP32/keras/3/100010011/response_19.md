After analyzing the buggy function `_clone_functional_model` and the corresponding error message, it is clear that the issue arises from the way the function handles multiple outputs without mask support. The error message `AssertionError: Could not compute output Tensor(...)` indicates that the function fails to compute the output tensor due to the lack of mask support.

The cause of the bug is related to how the function `_clone_functional_model` attempts to calculate the output tensors and masks for layers with multiple outputs. In cases where the layer does not support masks, the function incorrectly sets the output_masks to be None.

To fix the bug, we need to modify the function to handle layers without mask support correctly, ensuring that the output_masks are appropriately handled for all cases.

Here is a corrected version of the `_clone_functional_model` function:

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
            input_layers.append(layer)
            layer_map[layer] = input_tensor
        for _original, _cloned in zip(model._input_layers, input_layers):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for layer in model.layers:
        if layer not in layer_map:
            config = layer.get_config()
            new_layer = layer.__class__.from_config(config)
            layer_map[layer] = new_layer

    for x in model.inputs:
        for node in x._keras_history:
            tensor_map[node] = (x, None)

    for layer in model.layers:
        inbound_nodes = []
        for node in layer._inbound_nodes:
            new_node_key = layer_map[node.outbound_layer]
            node_args = [tensor_map[x][0] for x in node.input_tensors]
            node_args += [tensor_map[x][1] for x in node.input_masks]
            new_node = Node(outbound_layer=layer_map[layer], inbound_layers=node_args, node_indices=node.node_indices, tensor_indices=node.tensor_indices, arguments=None)
            inbound_nodes.append(new_node)
        layer._inbound_nodes = inbound_nodes

    output_tensors = to_list([layer.output for layer in model.layers[-1].outbound_nodes])
    
    return Model(input_tensors, output_tensors, name=model.name)
```

After implementing these changes, the function should now correctly handle layers with multiple outputs without mask support and no longer throw the AssertionError mentioned in the GitHub issue.