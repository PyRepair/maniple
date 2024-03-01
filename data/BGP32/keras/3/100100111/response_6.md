### Analysis:
1. The `clone_model()` function is intended to create a clone of a functional model with newly instantiated weights and layers.
2. The buggy function `_clone_functional_model` is failing to properly handle the case of a multi-output model with a layer that does not support masks, leading to an error when calling `model.predict(x_test)`.
3. The main cause of the bug is related to the handling of mask support for layers inside the model.
4. The issue reported on GitHub highlights the specific case where the error occurs and points to the issue with `output_masks` always being `[None]` instead of `[None, None]`.
5. To fix this bug, the mask handling for layers that do not support masks needs to be adjusted in the `_clone_functional_model` function.

### Proposed Fix:
1. Modify the `output_masks` calculation to handle the case when the layer does not support masks properly.
2. Check if the layer supports masks before trying to get the computed mask from the layer.
3. If the layer supports masks, update the `output_masks` accordingly, else set it to `[None]`.
4. Return the corrected model with the updated handling of masks.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

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
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    depth_keys = sorted(list(model._nodes_by_depth.keys()), reverse=True)
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
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = [computed_mask] if has_arg(layer.call, 'mask') else [None]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = [computed_masks] if has_arg(layer.call, 'mask') else [None]
                
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)
    
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
``` 

After applying this fix, the `test_clone_functional_model_with_multi_outputs` test case should pass without any errors.