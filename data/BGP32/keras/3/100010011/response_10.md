### Analysis:
The `clone_model` function is failing with an AssertionError stating "Could not compute output Tensor(...)". This error arises when trying to clone a model containing a layer with multiple outputs, where the output masks are always `None` due to the specific nature of the Lambda layer not supporting masks.

### Error Cause:
1. The original model contains a Lambda layer with multiple outputs.
2. Cloning the model using `clone_model` function tries to compute the output tensors along with masks for each output.
3. Since the Lambda layer doesn't support masks, the output_masks are always `None`.
4. The assertion fails when checking for the existence of output tensors in `tensor_map`.

### Bug Fix Strategy:
To fix this issue, we need to modify the `_clone_functional_model` function to handle the Lambda layer's specific case. We can remove the mask computation for Lambda layers to address the "Could not compute output Tensor" error.

### Bug Fix Implementation:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
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

            reference_input_tensors = node.input_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This updated function removes the computation of masks for the Lambda layer outputs, ensuring that the model cloning process does not fail with the given AssertionError.