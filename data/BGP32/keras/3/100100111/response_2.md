### Analysis
The buggy function `_clone_functional_model` is designed to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones. The function iterates over the nodes in the model and attempts to compute the output tensors for the clone model.

The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs and then attempts to clone it, but the clone produced by the buggy function does not match the original model. This discrepancy leads to the failure of the test.

The bug seems to be related to the incorrect mapping of input and output tensors in the `_clone_functional_model` function, causing issues when creating a clone model with multiple outputs.

### Bug Explanation
The bug lies in the incorrect handling of output masks when iterating over the nodes in the model. Specifically, the function expects `layer.compute_mask(...)` to return a list of masks, but for some layers like `Lambda`, the `compute_mask` method returns `None`.

This issue results in `output_masks` being set to `None` instead of a list of masks, leading to inconsistencies when creating the output tensors for the clone model.

### Solution Strategy
To fix the bug, we need to handle the case where the `compute_mask` method of a layer returns `None` properly. We should update the logic related to handling output masks to ensure that it accommodates different layer types correctly.

### Corrected Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        input_tensors = [Input(tensor=layer.output) for layer in model._input_layers]

    for layer in model.layers:
        if layer in layer_map:
            continue

        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer

    for node in model._nodes_by_depth:
        layer = node.outbound_layer

        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
        else:
            new_layer = layer_map[layer]

        reference_input_tensors = node.input_tensors
        computed_data = []
        for x in reference_input_tensors:
            computed_data.append(tensor_map.get(x, (x, None)))

        output_masks = []
        if all(data[1] is not None for data in computed_data):
            output_masks = new_layer.compute_mask([data[0] for data in computed_data], [data[1] for data in computed_data])

        output_tensors = to_list(new_layer([data[0] for data in computed_data]))

        for x, y, mask in zip(node.input_tensors, output_tensors, output_masks):
            tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the `_clone_functional_model` function addresses the issue of handling output masks correctly for layers like `Lambda` that return `None` from the `compute_mask` method. By ensuring proper mapping and handling of input and output tensors, the function should now be able to create a clone model with multiple outputs successfully.