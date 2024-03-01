### Analysis:
1. The buggy function `_clone_functional_model` is responsible for cloning a functional `Model` instance in Keras.
2. The test function `test_clone_functional_model_with_multi_outputs` fails when trying to clone a model with multiple outputs using the `clone_model` method.
3. The GitHub issue reported a related bug when using `clone_model` with multi_gpu_model and cpu_relocation=True. The issue pointed out that the `clone_model` method was not handling multi-output layers without mask support correctly, leading to the error: "Could not compute output Tensor".

### Bug Location:
The bug seems to be related to how the function `_clone_functional_model` handles layers with multiple outputs without mask support.

### Bug Cause:
The bug occurs when the function encounters a layer with multiple outputs without mask support, resulting in the `output_masks` being set to `None`, which leads to the error described in the GitHub issue.

### Bug Fix Strategy:
To fix the bug, we need to address how the function handles layers with multiple outputs without mask support by adjusting the creation of `output_masks` to handle the case where multiple outputs are expected but no masks are provided.

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
            newly_created_input_layer = input_tensor._keras_history
            layer_map[layer] = newly_created_input_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
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

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments or {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                tensor_map.update(zip(reference_output_tensors, output_tensors))

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

### Additional Notes:
The corrected function modifies the handling of output tensors and masks to ensure that multiple outputs without mask support are correctly handled during the cloning process. Make sure to test the corrected function to verify that it passes the failing test and resolves the issue reported on GitHub.