### Analysis:
1. The buggy function is `_clone_functional_model` which is used to clone a functional `Model` instance in Keras.
2. The bug seems to be related to the handling of input tensors and layers in the function, leading to incorrect mapping and computation of output tensors.
3. The failing test case `test_clone_functional_model_with_multi_outputs` aims to test the cloning of a model with multiple outputs but encounters an assertion error indicating a failure in computing the output tensors correctly.
4. The cause of the bug seems to be incorrect handling of input layers and tensors mapping, especially when dealing with multiple input and output layers in the functional model.
5. To resolve the bug, the function needs to correctly map input and output tensors, ensuring that the computation of output tensors is done accurately based on the model's structure.

### Bug Fix Strategy:
1. Ensure correct mapping between input and output tensors in the functional model.
2. Properly handle multiple input and output layers in the cloning process.
3. Correctly compute the output tensors based on the input tensors and layer operations.

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
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    else:
        input_tensors = to_list(input_tensors)
        for idx, inp_tensor in enumerate(input_tensors):
            if not K.is_keras_tensor(inp_tensor):
                inp_layer = model._input_layers[idx]
                input_tensor = Input(tensor=inp_tensor, name='input_wrapper_for_' + inp_layer.name)
                input_tensors[idx] = input_tensor

    for idx, x in enumerate(model.inputs):
        tensor_map[x] = (input_tensors[idx], None)

    for depth in reversed(sorted(model._nodes_by_depth.keys())):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in node.input_tensors if x in tensor_map]

            if len(computed_data) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                    if has_arg(layer.call, 'mask'):
                        kwargs['mask'] = computed_masks
                    computed_tensor = layer(computed_tensors, **kwargs)
                output_tensors = to_list(computed_tensor)
                tensor_map.update({out: (y, mask) for out, (y, mask) in zip(node.output_tensors, output_tensors)})

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

With this fix, the function should correctly clone a functional `Model` instance, including cases with multiple input and output tensors, as seen in the failing test `test_clone_functional_model_with_multi_outputs`.