### Analysis:
1. The buggy function `_clone_functional_model` is supposed to clone a functional model instance, creating new layers and weights. It iterates through the nodes of the model, creating new layers and mapping input/output tensors accordingly.
2. The function encounters an issue when dealing with multiple output layers that do not support masks. This leads to the computation error mentioned in the failing test.
3. The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs, one of which is a Lambda layer that does not support masks. When the model is cloned using `clone_model`, the bug surfaces due to how the function handles layers without masking support.
4. To fix the bug, we need to update the logic in `_clone_functional_model` where it deals with layers that lack mask support when computing outputs.
5. The corrected version should handle layers without mask support appropriately while cloning the model.

### Bug Fix:
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
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    else:
        input_tensors = [l if K.is_keras_tensor(l) else Input(tensor=l) for l in to_list(input_tensors)]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth, nodes in model._nodes_by_depth.items():
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments or {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = [None for _ in output_tensors]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = [None for _ in output_tensors]

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
    return Model(input_tensors, [tensor_map[x][0] for x in model.outputs], name=model.name)
```

The corrected function optimizes the process of mapping input tensors, handling multiple output layers, and addressing layers without mask support during the cloning of the model.

By implementing this fix, the function should properly handle the scenario described in the failing test and address the issue reported on GitHub.