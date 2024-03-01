### Analysis:
- The function `_clone_functional_model` is meant to clone a functional Keras model instance.
- The issue reported on GitHub suggests that there is an error in the `clone_model()` function leading to an error related to the output tensor computation.
- The key problem lies in the handling of masks by the layers during the cloning process when the layers do not support masks.
- The function tries to compute masks for each output tensor, assuming they are produced by layers that support masks, leading to the error mentioned in the GitHub issue.

### Bug Cause:
- The bug occurs when the original model contains layers that do not support masks.
- During the cloning process, the function tries to compute masks for the output tensors based on the layers' mask computation methods, which results in `None` being returned for all the masks when they are not supported.
- This results in an inconsistency where more than one output tensor is expected to produce masks, but actually, none are provided.

### Bug Fix Strategy:
- Modify the cloning process to handle cases where the layers do not support masks properly.
- Update the function to only attempt to compute masks for output tensors when the layer supports mask computation. Otherwise, treat them as `None`.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

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

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    
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
                if has_arg(layer.call, 'mask'):
                    computed_masks = [x[1] for x in computed_data]
                    kwargs['mask'] = computed_masks
                else:
                    computed_masks = [None] * len(computed_data)

                output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y, mask in zip(reference_output_tensors, output_tensors, computed_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected function should address the issue raised in the GitHub report by properly handling the computation of masks for output tensors from layers that do not support masks.