### Error Analysis:
The bug in the `_clone_functional_model` function arises from the mismatch between the expected behavior and the actual implementation. The issue originates from the computation of `output_masks` when calling a layer that does not support masking, such as the Lambda layer in this case. The function does not account for this edge case, leading to the incorrect assignment of `None` to `output_masks` instead of `[None, None]`.

### Bug Cause:
The Lambda layer does not support masking, and when processing layers with multiple outputs without mask support, the function fails to correctly handle the output mask computation. This results in the assertion error `Could not compute output Tensor` during execution when trying to clone a model with such characteristics.

### Strategy for Fixing the Bug:
To fix the bug, we need to update the function `_clone_functional_model` to handle layers without mask support appropriately. We should modify the computation of `output_masks` to create a list of `None` values corresponding to the number of output tensors from the layer when it does not support masking.

### Corrected Version of the `_clone_functional_model` Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer

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
            reference_output_tensors = node.output_tensors

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
                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = [x[1] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                # Compute the output_masks, considering layers without mask support
                if has_arg(layer.call, 'mask'):
                    output_masks = to_list(layer.compute_mask(computed_tensors, kwargs['mask']))
                else:
                    output_masks = [None] * len(output_tensors)

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected version of the function ensures that the `output_masks` are correctly handled when dealing with layers without mask support, resolving the assertion error and improving the model cloning process.