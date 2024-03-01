### Analysis:
The `clone_model` function in Keras is calling the `_clone_functional_model` function to clone a functional model instance. The issue arises when the input tensors are being set incorrectly, leading to an assertion error when attempting to compute the model outputs. The failing test `test_clone_functional_model_with_multi_outputs` is checking the equality of the predictions from the original model and the cloned model, which fails due to the erroneous clone process.

### Bug Cause:
The error occurs because the `input_layers` list is being used before it is populated correctly in the `if input_tensors is None` block. This results in incorrect mappings between input layers and input tensors, leading to a failure in predicting the model outputs.

### Fix Strategy:
1. Ensure that the `input_layers` list is populated correctly based on the `model._input_layers`.
2. Correctly map the input tensors to the corresponding input layers.
3. Verify that the computed data for each node is correct before calling the layer.

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
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            input_layers.append(input_tensor)
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
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
                computed_tensors, computed_masks = zip(*computed_data)
                if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                    kwargs['mask'] = computed_masks
                    
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                if has_arg(layer.call, 'mask'):
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                    computed_tensors = [tensor for tensor, _ in computed_data]
                    computed_masks = [mask for _, mask in computed_data]
                else:
                    output_masks = [None] * len(output_tensors)

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_layers, output_tensors, name=model.name)
```

### Summary:
The corrected `_clone_functional_model` function addresses the issue by properly handling the input tensors, mapping them to the input layers, and ensuring the correct computation of the model outputs during the cloning process. This fix should resolve the AssertionError encountered in the failing test and reported in the GitHub issue.