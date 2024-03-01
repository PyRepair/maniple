### Analysis:
1. The error message indicates an `AssertionError` occurring due to an output tensor not being computed. This implies that the model cloning process is not able to correctly compute the output.
2. The bug seems to be related to the computation and mapping of tensors within the `_clone_functional_model` function.
3. Looking at the function, we can see that the layer computation and mapping of input/output tensors is where the issue may lie. It could be related to how tensors are processed and mapped during the cloning process.
4. The potential cause of the bug could be incorrect processing of input tensors, layer mapping, or output tensor computation while cloning the model.
5. To fix the bug, we need to ensure that the tensors are correctly computed and mapped during the cloning process.

### Bug Fix:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(shape=layer.output_shape[1:]) for layer in model._input_layers]

    for original_input, new_input in zip(model._input_layers, input_tensors):
        tensor_map[original_input.output] = (new_input, None)

    for depth in range(len(model._nodes_by_depth)):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                # Clone layer.
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            input_tensors = [tensor_map[x][0] for x in node.input_tensors if x in tensor_map]

            if len(input_tensors) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                output_tensors = to_list(layer.call(input_tensors, **kwargs))
                output_mask = to_list(layer.compute_mask(input_tensors, None))

                for x, y, mask in zip(node.output_tensors, output_tensors, output_mask):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By following this bug fix, the function should now be able to clone the functional model correctly and compute the output tensors successfully.