### Analysis:
The GitHub issue points out an error occurring when using `clone_model()` function with `multi_gpu_model()` and `cpu_relocation=True`, resulting in an error message: "Could not compute output Tensor." The issue stems from the `clone_model()` function, specifically the `output_masks` assignment, due to the absence of mask support in certain layers like Lambda.

### Potential Error Locations:
1. Incorrect handling of `output_masks` in the `clone_model()` function.
2. Expecting masks from layers that do not support masks.

### Cause of the Bug:
The bug arises from a mismatch in the expected output masks in the `clone_model()` function, particularly due to layers like Lambda not supporting masks but the code expecting them. This mismatch leads to the error message during execution.

### Strategy for Fixing the Bug:
To fix the bug, we need to update the `clone_model()` function to handle the absence of masks from layers that do not support them, such as Lambda layers. This involves adjusting the logic around the retrieval and usage of `output_masks`.

### Corrected Version:
Here's the corrected version of the `_clone_functional_model()` function:

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
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    else:
        input_tensors = to_list(input_tensors)

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
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
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

This version handles the issue described in the GitHub thread by adjusting how the function manages output masks from layers that do not support them, like Lambda layers.