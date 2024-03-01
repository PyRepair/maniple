### Analysis:
- The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones.
- The error message indicates an `AssertionError` at line 166, stating that the model failed to compute an output tensor.
- The function checks and processes the input model, input tensors, creates new layers, and populates `layer_map` and `tensor_map`.
- In one part of the function, it iterates through the nodes of the model to compute outputs based on input tensors.
- The error seems related to the computation of output tensors during this process.
- The GitHub issue points out that when using `clone_model()` with `multi_gpu_model()` and `cpu_relocation=True`, the error occurs due to missing mask support for some layers like Lambda, causing the issue in the `clone_model()` function.
- The specific issue arises when the layer's `compute_mask` results in None due to missing mask support.

### Bug:
The bug arises from handling the output masks for layers lacking mask support. In such cases, the function fails to correctly compute the output tensors, leading to the `AssertionError`.

### Fix Strategy:
To fix the bug, we need to handle the case where the output masks are None for layers without mask support. We should update the logic to correctly set the output masks and prevent the function from failing in such cases.

### Code Fix:
Here's the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.input_shape[1:]) for layer in model.layers if isinstance(layer, InputLayer)]
    for x, y in zip(to_list(model.inputs), to_list(input_tensors)):
        tensor_map[x] = (y, None)

    for depth in range(len(model.layers)):
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
            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    output_tensors = to_list(layer(computed_data[0][0], **kwargs))
                else:
                    output_tensors = to_list(layer([x[0] for x in computed_data], **kwargs))

                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, to_list(output_tensors), name=model.name)
```

This corrected version should address the issue and allow the function to handle cases where layers lack mask support appropriately.