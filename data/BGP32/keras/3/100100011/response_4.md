### Analysis
The buggy function `_clone_functional_model` is responsible for cloning a functional `Model` instance. The function is tasked with creating new layers and new weights instead of sharing existing weights. 

The test function `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs, applying some operations on the input using lambda layers and a custom layer. Then, it attempts to clone the model using `keras.models.clone_model` and compare the predictions of the original model and the cloned model.

The GitHub issue highlights a similar problem with `clone_model` when using a functional model with a layer that has more outputs without mask support.

### Bug
The bug in the `_clone_functional_model` function lies in the creation of output masks for layers that do not support masks. This leads to the inability to compute the output tensors correctly, resulting in the error seen in the failing test and the GitHub issue.

### Fix Strategy
To fix the bug, we need to handle the case where the layer does not support masks correctly when computing output tensors and masks.

### Corrected Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
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
                kwargs = node.arguments or {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = [None] * len(output_tensors)
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = [None] * len(output_tensors)
                
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)
    
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected version of the `_clone_functional_model` function now correctly handles the creation of output masks for layers that do not support masks, ensuring that the output tensors are computed successfully. This correction should resolve the issue in the failing test and the reported GitHub issue.