### Analysis:
1. The function `_clone_functional_model` is intended to clone a functional model instance by creating new layers and new weights instead of sharing existing ones.
2. The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs and then tries to clone it using `keras.models.clone_model`.
3. The error occurs when trying to compute the output tensors in the function, specifically during the assertion check `assert x in tensor_map`.
4. The expected output tensors are not being computed correctly due to issues with the input data and layer configurations.
5. The GitHub issue points out a similar error related to the `clone_model` function, where the output masks are expected to be `[None, None]` but are `[None]` instead. This hints at a possible bug in the handling of multi-output layers.
   
### Bug:
The bug lies in the logic for computing output tensors and masks when dealing with multiple outputs, especially in cases where masks are not supported by the layers.

### Fix Strategy:
1. Check if the layers support masking before trying to compute masks.
2. Ensure that the output masks are handled correctly, especially for layers that do not support masks.
3. Update the logic for computing output tensors and masks to handle multiple outputs appropriately.
4. Verify that the input data and layer configurations are processed accurately to prevent errors during output computation.

### Corrected Version:
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
                               sparse=layer.sparse, name=layer.name)
                         for layer in model._input_layers]

    input_layers = [input_tensor._keras_history[0] for input_tensor in input_tensors]
    for original, cloned in zip(model._input_layers, input_layers):
        layer_map[original] = cloned

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    depth_keys = sorted(model._nodes_by_depth.keys(), reverse=True)
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
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = computed_masks
                output_tensors = layer(computed_tensors, **kwargs)
                output_masks = [layer.compute_mask(t, m) for t, m in zip(computed_tensors, computed_masks)]

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
``` 

By updating the logic for computing output tensors and masks and handling multiple outputs correctly, the corrected `clone_functional_model` should now resolve the issue and pass the failing test.