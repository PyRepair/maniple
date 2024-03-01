### Analysis:
The error message indicates that the `assert` statement in the `_clone_functional_model` function fails, specifically when trying to check if a certain output tensor has been computed. The user reproducing the bug on GitHub provides a script that triggers this issue when using `clone_model` on a model with a layer that has multiple outputs without mask support.

### Potential Errors:
1. Incorrect handling of input tensors and creation of input layers.
2. Incorrect updating of the `tensor_map` dictionary during the computation process.
3. Lack of support for multiple output tensors without mask support in certain layers like Lambda.

### Bug Cause:
The bug is caused by the way the `tensor_map` is updated during the processing of the model's nodes. When encountering a layer with multiple outputs that does not support mask computation (such as the Lambda layer in the GitHub issue script), the `layer.compute_mask` function returns `None`, leading to incorrect behavior in storing and updating the output tensors in the `tensor_map`. This eventually results in the `assert` statement failure.

### Strategy for Fixing the Bug:
1. Update the logic related to handling input tensors and input layers.
2. Ensure correct mapping and updating of the `tensor_map` dictionary during node processing.
3. Account for layers with multiple outputs that do not support mask computation.

### Corrected Version of the Function:

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
        for i, layer in enumerate(model._input_layers):
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[model.inputs[i]] = input_tensor
        for _original, _cloned in zip(model._input_layers, input_layers):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                layer_map[model.inputs[i]] = input_tensor
            else:
                layer_map[model.inputs[i]] = x

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in range(len(model._nodes_by_depth)):
        for nodes in model._nodes_by_depth[depth]:
            layer = nodes.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = nodes.input_tensors
            reference_output_tensors = nodes.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if reference_input_tensors and len(computed_data) == len(reference_input_tensors):
                if nodes.arguments:
                    kwargs = nodes.arguments
                else:
                    kwargs = {}
                computed_tensors = [x[0] for x in computed_data]
                if len(computed_data) == 1:
                    computed_tensors = computed_tensors[0]
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

After applying the changes above, the `clone_model` function should now handle cases where layers have multiple outputs without mask support correctly, thereby resolving the reported issue.