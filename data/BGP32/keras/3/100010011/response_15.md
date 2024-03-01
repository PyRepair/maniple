### Analysis:
The buggy function `_clone_functional_model` is responsible for cloning a functional `Model` instance in Keras. The function encounters an error when trying to compute the output tensors for a model containing multiple outputs, specifically when a layer does not support masks. The error message states that the function could not compute the output tensor for a specific layer.

The GitHub issue highlights a scenario where the `clone_model` function fails when used in conjunction with `multi_gpu_model` and `cpu_relocation=True` settings. The issue arises due to the inconsistency in handling output masks for layers that do not support masks, such as the Lambda layer in the provided script.

### Bug:
The bug occurs in the `_clone_functional_model` function where the output masks are expected to be computed for layers that do not support masks, leading to an assertion error when the output tensor computation fails for a layer without a mask.

### Fix Strategy:
To fix the bug, we need to handle the case of layers without mask support correctly. Specifically, when creating new output tensors for layers that do not support masks, we should ensure that the output masks remain `None`.

### Corrected Version:
Below is the corrected version of the `_clone_functional_model` function that addresses the bug and should pass the failing test:
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

    for i, orig_input in enumerate(model.inputs):
        tensor_map[orig_input] = (input_tensors[i], None)

    for node in model._nodes_by_depth:
        for layer in node.outbound_layer:
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

        for node in nodes:
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                output_tensors = to_list(layer(computed_data, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By ensuring that we handle layers without mask support correctly in the revised function, we can overcome the error encountered during output tensor computation for layers like the Lambda layer that lack mask functionality. This corrected version should help resolve the failing test and the issue described in the GitHub post.