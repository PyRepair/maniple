### Analysis
1. The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance. It encounters an issue when handling a model with multiple outputs and one of the layers doesn't support masks, resulting in the assertion error.
2. The bug occurs because the function doesn't properly handle the case where a layer doesn't support masks but is part of a model with multiple outputs.
3. The failing test `test_clone_functional_model_with_multi_outputs` tries to clone a model with multiple outputs which exposes the bug in `_clone_functional_model`.
4. To fix the bug, we need to ensure proper handling of layers without mask support during the cloning process.

### Strategy for Fixing the Bug
1. Check each layer for mask support before calling `layer.compute_mask`.
2. Only pass masks to layers that support them.
3. Update the tensor map with the computed output tensors after calling the layer.

### Corrected Version of the Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for layer in model.layers:
        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for layer in model.layers:
        for node in layer._inbound_nodes:
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            computed_data = []

            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    output_tensor = layer(computed_tensor, **kwargs)
                    output_tensors = to_list(output_tensor)
                    computed_tensors = [computed_tensor]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

Now, the corrected function should properly handle models with multiple outputs and layers without mask support, satisfying the failing test and fixing the bug.