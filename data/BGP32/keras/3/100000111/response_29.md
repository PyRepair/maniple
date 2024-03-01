### Analysis:
- The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones. 
- The function takes `model` as input, which is expected to be an instance of the `Model` class. It also accepts an optional `input_tensors` list.
- The bug seems to be related to the incorrect construction of `output_masks`, leading to an error when trying to compute the output tensors.

### Bug Explanation:
- The issue arises from the fact that the `output_masks` are always set to `[None]`, as the function `layer.compute_mask` returns `None` when the layer is a Lambda layer that does not support masks. This results in an incorrect number of masks for the output tensors.
- The error mentioned in the GitHub issue is due to the mismatch in the expected and actual number of output masks.

### Bug Fix Strategy:
- Update the logic for handling output masks to correctly account for cases where the layer does not support masks. If the `layer.compute_mask` returns `None`, the output masks should be set as `None` for those output tensors.
- Ensure that the `output_masks` list matches the number of output tensors to avoid the assertion error during model computation.

### Corrected Function:
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

    for input_tensor, input_layer in zip(model.inputs, input_tensors):
        tensor_map[input_tensor] = (input_layer, None)

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
            reference_output_tensors = node.output_tensors
            computed_data = []

            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}

                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = [computed_mask] if 'mask' in kwargs and has_arg(layer.call, 'mask') else [None]
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = [computed_mask for computed_mask in computed_masks] if 'mask' in kwargs and has_arg(layer.call, 'mask') else [None] * len(computed_data)
                
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected function now properly handles the building of new layers and the tracking of input and output tensors and masks, ensuring that the output masks match the number of output tensors.