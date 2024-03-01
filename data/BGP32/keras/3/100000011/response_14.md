### Analysis:
The GitHub issue describes an error that occurs when using `clone_model()` with `multi_gpu_model` and `cpu_relocation=True`. The issue points to a bug in the `clone_model()` function where the output tensors are not correctly computed in some cases, leading to the 'Could not compute output Tensor' error.

### Potential Error Locations:
1. The computation of output tensors within the `clone_model()` function.
2. Handling of multiple output tensors when a layer does not support masks.

### Cause of the Bug:
The bug occurs because the `clone_model()` function does not handle multiple output tensors correctly, especially if a layer does not support masks. This leads to the output_masks being [None], which causes the 'Could not compute output Tensor' error.

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the output tensors are correctly computed for multiple output tensors, even when a layer does not support masks. This might involve handling the computation of masks more effectively and updating the tensor map appropriately.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    input_layers, input_tensors, layer_map, tensor_map = [], [], {}, {}

    if input_tensors is None:
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            input_layers.append(layer)
            layer_map[layer] = input_tensor
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_layers.append(model._input_layers[i])
                layer_map[model._input_layers[i]] = input_tensor
                tensor_map[x] = (input_tensor, None)
            else:
                tensor_map[x] = (x, None)

    for depth in reversed(range(len(model._nodes_by_depth))):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

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
                
                if has_arg(layer.call, 'mask') and None not in computed_masks:
                    kwargs['mask'] = computed_masks
                
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                if has_arg(layer.call, 'mask') and None not in computed_masks:
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                    for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                        tensor_map[x] = (y, mask)
                else:
                    for x, y in zip(reference_output_tensors, output_tensors):
                        tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

### Changes Made:
1. Fixed the generation of `input_layers` to correctly cache the input layers.
2. Updated the handling of input tensors to ensure caching and mapping.
3. Enhanced the computation of output tensors and masks for layers that don't support masks.
4. Updated the handling of multiple output tensors appropriately.

By incorporating these changes, the `clone_model()` function should now correctly compute the output tensors and resolve the issue described in the GitHub bug report.