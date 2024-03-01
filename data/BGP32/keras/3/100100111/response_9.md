## Analysis
The `__clone_functional_model` function is designed to clone a functional Keras model by recreating new layers and weights. The bug in the current implementation seems to arise when the function encounters a layer with multiple outputs without mask support, leading to an issue with computing the output tensors correctly.

The failing test case `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs and attempts to clone it using the `clone_model` function. However, due to the bug in the `__clone_functional_model` function, the output tensors cannot be computed correctly, leading to assertion errors.

Based on the GitHub issue provided, the issue seems to be related to cases where a layer does not support masks, causing the output_masks to always be `None`. This impacts the correct computation of output tensors in the cloning process.

## Bug Explanation
The bug in the `__clone_functional_model` function arises when a layer with multiple outputs without mask support is encountered. This results in the output_masks being set to `None` which prevents the function from correctly computing the output tensors for the model. This leads to assertion errors when trying to predict using the cloned model.

## Bug Fix Strategy
To fix the bug, we need to modify the handling of layers without mask support in the cloning process. By ensuring that the output_masks are correctly set according to the actual behavior of the layers, we can address the issue raised in the failing test case and the related GitHub issue.

## Bug-fixed Function
Here's the corrected version of the `__clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                               sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    else:
        input_tensors = [Input(tensor=x, name='input_wrapper_for_' + layer.name) if not K.is_keras_tensor(x) else x
                         for x, layer in zip(input_tensors, model._input_layers)]

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
            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                inputs = [x[0] for x in computed_data]
                masks = [x[1] for x in computed_data]
                if len(inputs) == 1:
                    output_tensors = to_list(layer(inputs[0], **kwargs))
                    output_masks = to_list(layer.compute_mask(inputs[0], masks[0] if masks[0] is not None else None))
                else:
                    output_tensors = to_list(layer(inputs, **kwargs))
                    output_masks = to_list(layer.compute_mask(inputs, masks))

                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

In this corrected version, we modify how output_masks are handled when computing tensors for layers with multiple outputs. By ensuring that the output_masks are correctly set based on the behavior of each layer, the function should now be able to clone functional models correctly, including cases with multiple outputs without mask support.