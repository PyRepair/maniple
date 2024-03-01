### Analysis:
1. **Error Message**: The error message states that an assertion fails because the output Tensor is not found in the `tensor_map`.
2. **Input**: The input parameters are valid instances of the required types.
3. **Expected Output**: The function should create a new model by cloning the original model while handling multiple inputs and outputs accurately.
4. **Bug Cause**: The bug likely arises from incorrect handling of various layers and their output tensors. The code might not properly update the `tensor_map` with the output tensors of the layers in the model, leading to the assertion failure.
5. **GitHub Issue**: The issue relates to using `clone_model` with `multi_gpu_model` where the error occurs due to mismatched output masks for layers without mask support.

### Fix Strategy:
1. We need to ensure that the `tensor_map` is correctly updated with the output tensors of each layer in the model.
2. Address the issue of incorrect mask handling for layers without mask support.
3. Ensure that the input tensors are properly cached and handled when cloning the model.

### Correction:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
                         for layer in model._input_layers]
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]
                if isinstance(new_layer, InputLayer):
                    continue
            
            ref_input_tensors = node.input_tensors
            computed_data = [(tensor_map[x][0], None) for x in ref_input_tensors if x in tensor_map]
            
            if len(computed_data) == len(ref_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                if has_arg(new_layer.call, 'mask') and ref_input_tensors:
                    kwargs['mask'] = computed_masks
                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                tensor_map.update({y: (x, mask) for x, y, mask in zip(ref_input_tensors, output_tensors)})
    
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        output_tensors.append(tensor_map[x][0])
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version ensures that the output tensors are properly tracked and updated in the `tensor_map`, addressing the issue of failing to find the output tensors during model cloning.