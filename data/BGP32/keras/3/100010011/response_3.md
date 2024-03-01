### Analysis:
The buggy function `_clone_functional_model` is supposed to clone a functional model instance. The error message indicates an issue with computing the output tensor during the cloning process, specifically when dealing with multiple outputs from a layer without mask support.

The GitHub issue highlights a similar problem when using `clone_model` with a functional model containing a layer with multiple outputs and lacking mask support. The issue is related to the inability to compute the output tensor correctly, leading to the AssertionError.

### Identified Issue:
The bug arises due to the incorrect handling of multiple output tensors from a layer without mask support. When cloning the model, the function fails to properly handle the situation where a layer generates multiple output tensors without corresponding masks.

### Bug Fix Strategy:
To resolve the bug, the function needs to be updated to appropriately handle multiple output tensors from a layer without mask support. This involves ensuring that the correct number of output masks (or None if not supported) are generated and associated with each output tensor.

### Bug Fix and Corrected Version:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}
    tensor_map = {}
  
    if input_tensors is None:
        input_tensors = model.inputs
  
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    for layer in model.layers:
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer

        reference_input_tensors = layer.input
        reference_output_tensors = layer.output

        computed_data = []
        for x in reference_input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])

        if len(computed_data) == len(reference_input_tensors):
            kwargs = {} if not layer._arg_names else {k: getattr(layer, k) for k in layer._arg_names}
            computed_tensors = [x[0] for x in computed_data]
            computed_masks = [x[1] for x in computed_data]
            if 'mask' in kwargs and computed_masks:
                kwargs['mask'] = computed_masks
            output_tensors = to_list(layer(computed_tensors, **kwargs))
            output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

            for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version improves the handling of multiple output tensors without mask support, addressing the issue mentioned in the GitHub report.