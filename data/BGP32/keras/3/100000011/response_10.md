## Analysis:
The buggy function `_clone_functional_model` is responsible for cloning a functional `Model` instance. The bug mentioned in the GitHub issue is related to the `clone_model()` function raising an error when using `multi_gpu_model` with `cpu_relocation=True`. The error message states that it could not compute the output tensor, indicating a problem during the cloning process. The issue seems to stem from the handling of masks in layers, especially when a layer does not support masks.

## Potential Error Locations:
1. The handling of masks in layers which may result in `output_masks` being `[None]`.
2. The computation of output tensors and masks when calling a layer.
3. The `AssertionError` raised when computing model outputs.

## Cause of the Bug:
The bug arises from the incorrect handling of masks in layers, particularly when using `Lambda` layers without mask support. This leads to the `output_masks` list containing only `[None]`, causing issues during the computation of output tensors and masks.

## Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the logic related to masks in layers is correctly handled, especially when dealing with `Lambda` layers that do not support masks. The `clone_model()` function should be updated to handle such cases appropriately.

## Corrected Version of the Function:
Here is the corrected version of the `_clone_functional_model` function that addresses the bug mentioned in the GitHub issue:

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
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
    for original, cloned in zip(model._input_layers, input_tensors):
        layer_map[original] = cloned

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
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                computed_tensors = [x[0] for x in computed_data]
                output_tensors = layer(computed_tensors, **kwargs)
                
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version adjusts the handling of masks and output tensors during the cloning process to prevent the reported issue when using `clone_model()`.