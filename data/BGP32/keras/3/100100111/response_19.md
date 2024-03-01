### Analysis:
1. The `because layer.compute_mask(...)` part of the code seems to be the issue, as stated in the GitHub issue where `output_masks` is always `[None]`.
2. The failing test `test_clone_functional_model_with_multi_outputs`, when creating a model with multiple outputs that include a `Lambda` layer, triggers the error due to the issue in the `_clone_functional_model` function.
3. The issue is related to handling multiple outputs from a model that includes layers without mask support, like the `Lambda` layer in the failing test. This causes the `_clone_functional_model` function to attempt to compute masks even when they are not available.
4. To fix the bug, we need to modify the `_clone_functional_model` function to handle the case where certain layers don't support masks correctly.

### Bug Fix Strategy:
1. Update the code to check if the layer has mask support before trying to compute masks.
2. Modify the code to handle layers without mask support when dealing with multiple outputs in the model.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    input_layers = []

    if input_tensors is None:
        for layer in model._input_layers:
            input_layer = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_layers.append(input_layer)
            layer_map[layer] = input_layer
        input_tensors = input_layers

    for i, x in enumerate(input_tensors):
        if not K.is_keras_tensor(x):
            name = model._input_layers[i].name
            input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
            input_tensors[i] = input_tensor
            layer_map[x._keras_history.layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in range(model._output_rank):
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
            
            reference_inputs = node.input_tensors
            reference_outputs = node.output_tensors

            computed_data = []
            for x in reference_inputs:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            kwargs = node.arguments if node.arguments else {}
            if len(computed_data) == 1:
                computed_tensor, _ = computed_data[0]
                output_tensors = to_list(layer(computed_tensor, **kwargs))
            else:
                computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))

            for x, y in zip(reference_outputs, output_tensors):
                tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By making the above changes, the corrected `_clone_functional_model` function should now handle the case of layers without mask support when dealing with multiple outputs. This modification should resolve the issue reported on GitHub and make the failing test pass successfully.