### Analysis:
1. The error message indicates that the assertion `assert x in tensor_map` is failing, specifically for the output tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`.
2. This error occurs while trying to compute the output tensors in the function `_clone_functional_model`.
3. The function `_clone_functional_model` is intended to clone a functional `Model` instance, but there seems to be an issue with correctly mapping the input and output tensors during the cloning process.
4. The function needs to correctly build the new model by creating new layers and input tensors based on the existing model and input tensors provided.

### Bug Fix Strategy:
1. The issue arises from incomplete mapping of input and output tensors during the cloning process.
2. Verify that all input tensors are mapped correctly and used to compute the output tensors for the new model.
3. Revisit the logic for creating and mapping input placeholders if input tensors are not provided.
4. Ensure that the logic for creating new layers and processing input/output tensors is correctly handled.
5. Update the cloning process to accurately replicate the model behavior with new layers and input tensors.

### Bug Fixed Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_layers = []
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
                input_tensor = Input(tensor=x, shape=x.shape[1:], name='input_wrapper_for_' + name)
                tensor_map[model._input_layers[i]] = (input_tensor, None)
                layer_map[model._input_layers[i]] = input_tensor
            else:
                tensor_map[model._input_layers[i]] = (x, None)
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer.
            layer = node.outbound_layer

            # Get or create layer.
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            # Gather inputs to call the new layer.
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
            
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data] if any(x[1] is not None for x in computed_data) else None

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                if computed_masks:
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                else:
                    output_masks = None
                
                # Update tensor_map.
                for i, x in enumerate(reference_output_tensors):
                    tensor_map[x] = (output_tensors[i], output_masks[i] if output_masks else None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model([tensor_map[x][0] for x in model.inputs], output_tensors, name=model.name)
```

After applying the corrections, the `_clone_functional_model` function should now correctly clone the functional `Model` instance and avoid any errors related to missing or incorrect mappings of input and output tensors during the cloning process.