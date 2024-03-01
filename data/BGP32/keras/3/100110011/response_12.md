### Analysis:
1. The buggy function `_clone_functional_model` is designed to clone a functional Keras model by creating new layers instead of sharing existing ones.
2. The failing test case `test_clone_functional_model_with_multi_outputs` is trying to clone a model with multiple outputs.
3. The error message shows that the model output tensor was not computed during the cloning process.
4. The GitHub issue points out a similar problem where the `layer.compute_mask` function always returns `None` for layers without mask support, leading to the error.

### Bug Cause:
The bug is caused by the `layer.compute_mask` function returning `None` for layers without mask support, resulting in missing output computations during model cloning.

### Fix Strategy:
To fix the bug, we should update the logic to handle layers without mask support properly during the cloning process.

### Corrected Version:
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
        layer_map = {layer: input_tensor for layer, input_tensor in zip(model._input_layers, input_tensors)}
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + model._input_layers[i].name)
                input_tensors[i] = input_tensor
                layer_map[x._keras_history[0]] = input_tensor._keras_history[0]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                if len(computed_tensors) == 1:
                    computed_tensors = computed_tensors[0]
                output_tensors = layer(computed_tensors, **kwargs)
                if not isinstance(output_tensors, list):
                    output_tensors = [output_tensors]

                for ref_out_tensor, out_tensor in zip(node.output_tensors, output_tensors):
                    tensor_map[ref_out_tensor] = (out_tensor, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the `_clone_functional_model` function should address the issue and pass the failing test case.