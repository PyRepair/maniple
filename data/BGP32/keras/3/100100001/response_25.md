### Analysis:
- The `_clone_functional_model` function is intended to clone a functional model by creating new layers and weights instead of sharing existing ones.
- The function checks whether the input model is an instance of `Model` and not `Sequential`, as cloning is specifically for `Model` instances.
- The function handles creating placeholders for input tensors or using provided input tensors to clone the model layer by layer.
- It iterates over the nodes in the model to recreate the layers and connections in the new model.
- It encounters a bug where the cloned model does not match the original model when multiple outputs are involved.

### Bug Identification:
- The main issue causing the bug is that when there are multiple output tensors, the function fails to properly handle the output tensors and their corresponding calculations.
- Specifically, the function is not properly handling multiple output tensors from a layer.
- Due to this, the cloned model outputs do not match the original model outputs when there are multiple outputs involved.

### Bug Fix Strategy:
- To fix the bug, we need to correctly handle the case where there are multiple output tensors from a layer.
- This involves ensuring that the outputs from the layer are correctly processed and stored in the `tensor_map`.
- We need to adjust the logic for handling multiple output tensors and their corresponding computations.

### Corrected Function:

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
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
            input_layers.append(newly_created_input_layer)

    for i, layer in enumerate(model.layers):
        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer

        input_tensors = [tensor_map[in_layer].output for in_layer in new_layer._inbound_nodes[0].inbound_layers]
        output_tensors = new_layer(input_tensors)
            
        for in_layer, out_tensor in zip(new_layer._inbound_nodes[0].inbound_layers, output_tensors):
            tensor_map[in_layer] = out_tensor

    new_inputs = [tensor_map[in_layer] for in_layer in model.inputs]
    new_outputs = [tensor_map[out_layer] for out_layer in model.outputs]

    return Model(new_inputs, new_outputs, name=model.name)
```

After fixing the issues in the function, the corrected version should properly handle multiple output tensors and ensure that the cloned model produces the same outputs as the original model when tested.