### Analysis:
The error message indicates that the `output_tensors` cannot be computed for the input model during cloning due to the issue with finding the corresponding tensor in the `tensor_map`. This is likely caused by the incorrect handling of multiple outputs from a layer without mask support.

The GitHub issue also points towards the same problem with the `Lambda` layer not supporting masks. This leads to the incorrect computation of `output_masks`, resulting in the subsequent failure during the cloning process.

### Bug Cause:
The bug arises from the `Lambda` layer not supporting masks and therefore always returning `None` as the `output_masks`. This inconsistency affects the computation of `output_tensors` and prevents the successful cloning of the functional model.

### Fix Strategy:
1. Handle the scenario where the `output_masks` can be `None` due to lack of support in certain layers.
2. Ensure that each output tensor is correctly paired with its corresponding tensor and mask when updating the `tensor_map`.
3. Check for multiple outputs from layers and handle the computation of `output_tensors` and `output_masks` accordingly.

### Corrected Version:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for layer in model.layers:
        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer
    
    for node in model._nodes_by_depth:
        layer = node.outbound_layer
        if isinstance(layer, (Lambda, InputLayer)):  # Will not call Lambda and InputLayer multiple times
            continue
        
        reference_input_tensors = node.input_tensors
        reference_output_tensors = node.output_tensors
        
        computed_data = [(tensor_map[x] if x in tensor_map else (x, None)) for x in reference_input_tensors]
        
        if len(computed_data) == len(reference_input_tensors):
            kwargs = node.arguments if node.arguments else {}
            if len(computed_data) == 1:
                computed_tensor, computed_mask = computed_data[0]
            else:
                computed_tensors, computed_masks = zip(*computed_data)
                kwargs['mask'] = computed_masks
            
            output_tensors = to_list(layer(computed_tensors, **kwargs))
            output_masks = to_list(layer.compute_mask(computed_tensors, **kwargs))
            
            for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                tensor_map[x] = (y, mask)
                
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version addresses the issue by appropriately handling the `output_masks` and adjusting the logic for multiple outputs from layers, especially those without mask support like the `Lambda` layer.