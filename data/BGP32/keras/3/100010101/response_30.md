### Analysis
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and weights instead of reusing existing ones. The function iterates through the model's nodes to recreate the structure with new layers. The error occurs when asserting that the model's outputs have been computed during the cloning process, specifically failing to find the output tensor for the `SwapLayer` node.

### Issues
1. The input tensors in the `SwapLayer` node are not properly handled and stored in the `tensor_map`.
2. The computed output tensors are not correctly updated in the `tensor_map`.

### Bug Fix Strategy
1. Ensure that the input tensors from the `SwapLayer` are correctly added to the `tensor_map`.
2. Update the output tensors correctly in the `tensor_map` after calling the new layer in each node.

### Bug Fix
Here is the corrected version of the `_clone_functional_model` function:

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
            layer_map[layer] = input_tensor
            
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        
        for i, x in enumerate(input_tensors):
            if K.is_keras_tensor(x):
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = x
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

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

                if has_arg(new_layer.call, 'mask') and isinstance(computed_data[0][1], (list, tuple)):
                    kwargs['mask'] = computed_masks

                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                # Compute masks for layers that support masking
                if has_arg(new_layer.call, 'mask'):
                    output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))
                else:
                    output_masks = [None] * len(output_tensors)

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version ensures that the input tensors are correctly handled for the `SwapLayer` node and that the output tensors are properly updated in the `tensor_map`.