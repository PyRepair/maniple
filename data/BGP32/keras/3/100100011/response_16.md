### Analysis:
1. The buggy function `_clone_functional_model` is used to clone a functional Keras `Model` instance. It is designed to create a new model with new layers and weights instead of sharing the existing ones.
2. The bug seems to stem from the incorrect handling of the input layer creation and mapping of tensors within the function.
3. The GitHub issue describes a similar error scenario when using `clone_model` with multi_gpu_model and `cpu_relocation=True`. The issue highlighted that `output_masks` is always `[None]` due to a lack of mask support in Lambda layers, leading to the error in computing the output tensor.
4. To fix the bug, we need to ensure the correct mapping of input layers, handle cases where masks are not supported, and ensure proper cloning of the layers during model duplication.

### Bug Fix Strategy:
1. Check and correct the creation and mapping of input layers in the function.
2. Handle the situations where layer masks are `None` or not supported by the layers being cloned.
3. Ensure consistent handling of output tensor computation and mapping.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}
    tensor_map = {}

    # Input layer creation and mapping
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer batch_input_shape, dtype=layer.dtype,
                                 sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        # Handle non-Keras input tensors
        input_tensors = to_list(input_tensors)
        cloned_input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                cloned_input_tensors.append(input_tensor)
                layer_map[x._keras_history[0]] = input_tensor._keras_history[0]
            else:
                cloned_input_tensors.append(x)
        input_tensors = cloned_input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in reversed(range(len(model._nodes_by_depth))):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                layer_map[layer] = layer.__class__.from_config(layer.get_config())

            layer = layer_map[layer]
            if isinstance(layer, InputLayer):
                continue

            reference_input_tensors = node.input_tensors
            computed_data = [tensor_map[x] for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data if x[1] is not None]

                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data if x[1] is not None]

                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = computed_masks if computed_masks else None

                output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

After applying these fixes, the `_clone_functional_model` function should now correctly handle the cloning of a functional Keras model while addressing the issue reported in the GitHub bug.