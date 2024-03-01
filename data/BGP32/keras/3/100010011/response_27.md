### Analysis:
The bug occurs in the `_clone_functional_model` function when trying to clone a multi-output functional model. The root cause of the issue is that the function does not handle layers with multiple outputs correctly when they do not have mask support. This leads to an assertion error when trying to compute the output tensors.

### Potential Error Locations:
1. Handling multiple outputs without mask support.
2. Incorrect handling of output tensors for nodes with multiple inputs and outputs.

### Cause of the Bug:
The bug occurs because the function does not properly handle layers with multiple outputs when mask support is not provided. This leads to an assertion error when trying to compute the output tensors.

### Strategy for Fixing the Bug:
The function should be modified to handle layers with multiple outputs correctly, especially when mask support is not available. By updating the logic to accommodate layers without mask support and multiple output tensors, the bug can be fixed.

### Corrected Version:
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
        input_tensors = [Input(batch_shape=layer.input_shape,
                                dtype=layer.dtype,
                                sparse=layer.sparse,
                                name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[x._keras_history[0]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in reversed(range(len(model._nodes_by_depth))):
        for node in model._nodes_by_depth[depth]:
            if node.outbound_layer not in layer_map:
                new_layer = node.outbound_layer.__class__.from_config(node.outbound_layer.get_config())
                layer_map[node.outbound_layer] = new_layer

            inbound_tensors = [tensor_map[x][0] for x in node.input_tensors]
            kwargs = node.arguments if node.arguments else {}
            output_tensors = to_list(layer_map[node.outbound_layer](inbound_tensors, **kwargs))

            for x, y in zip(node.output_tensors, output_tensors):
                tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the function updates the logic to properly handle layers with multiple outputs when mask support is not provided, resolving the issue reported on GitHub.