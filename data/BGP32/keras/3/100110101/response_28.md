### Bug Analysis:
The bug in the `_clone_functional_model` function arises from the incorrect usage of the `layer_map` and `tensor_map` dictionaries. Due to improper initialization and handling of these dictionaries, the function fails to correctly create new layers and tensors, leading to an assertion error when attempting to compute the model outputs.

#### Issues:
1. The `input_layers` list is incorrectly initialized to an empty list but is never used afterward, resulting in a discrepancy when working with the original input layers.
2. Layer mapping is not properly done when processing the input tensors, leading to the loss of information about the original layers.
3. The `input_tensors` list is overwritten without maintaining a mapping to the original input layers, causing a loss of correspondence.
4. The mapping between reference and computed tensors in the `tensor_map` dictionary is not handled correctly, leading to missing keys during the model output computation.

### Bug Fix Strategy:
To address the issues identified, the following steps should be taken:
1. Ensure that the mapping between the original layers and the new layers is consistently maintained.
2. Correctly handle the initialization of input layers and maintain the mapping between the original input layers and the new input tensors.
3. Verify that the mapping between the reference and computed tensors is preserved in the `tensor_map` dictionary.
4. Update the function to correctly compute and map the model outputs based on the processed input tensors.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    input_layers = []
    
    if input_tensors is None:
        input_tensors = []
        for layer in model._input_layers:
            input_layer = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_layers.append(layer)
            input_tensors.append(input_layer)
            layer_map[layer] = input_layer
    else:
        input_tensors = to_list(input_tensors)
        for i, layer in enumerate(model._input_layers):
            x = input_tensors[i]
            if not K.is_keras_tensor(x):
                input_layer = Input(tensor=x, name='input_wrapper_for_' + layer.name)
                input_tensors[i] = input_layer
                layer_map[layer] = input_layer
            else:
                layer_map[layer] = x

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in range(len(model._nodes_by_depth)):
        for node in model._nodes_by_depth[depth]:
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
                computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask
                    output = layer(computed_tensor, **kwargs)
                    computed_tensors = [computed_tensor]
                    computed_masks = [computed_mask]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                    output = layer(computed_tensors, **kwargs)
                
                output_tensors = to_list(output)
                for x, (y, mask) in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

By incorporating the corrections mentioned above, the `_clone_functional_model` function should now work correctly and pass the failing test case provided.