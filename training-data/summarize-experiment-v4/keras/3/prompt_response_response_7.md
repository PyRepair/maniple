## Bug's cause:

The bug occurs in the `_clone_functional_model` method, where the error message "Could not compute output Tensor" is triggered. The error is caused by the failure to compute the output of the `swap_layer_1`.

This failure is likely due to the improper construction of the model during the cloning process, as indicated by the failure to compute the output with a specific shape and data type.


## Fixing the bug:

To fix the bug, we need to revisit the cloning process and ensure that the layers and nodes are constructed and initialized properly. Additionally, we should address any issues related to the construction of the model during the cloning process.


## Corrected code:

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
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        # Make sure that all input tensors come from a Keras layer.
        # If the tensor comes from an input layer: cache the input layer.
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                layer_map[x._keras_history[0]] = input_tensor._keras_history[0]
                input_tensors[i] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = sorted(list(model._nodes_by_depth.keys()), reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            # Get or create layer.
            if layer not in layer_map:
                # Clone layer.
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                # Reuse previously cloned layer.
                layer = layer_map[layer]
                # Don't call InputLayer multiple times.
                if isinstance(layer, InputLayer):
                    continue

            # Possibly optimize to check if all input tensors are available in tensor_map before computing.
            reference_input_tensors = node.input_tensors
            computed_data = [tensor_map[x] for x in reference_input_tensors if x in tensor_map]
        
            if len(computed_data) == len(reference_input_tensors):
                # Call layer.
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                computed_tensors, computed_masks = zip(*computed_data)
                if has_arg(layer.call, 'mask') and None not in computed_masks:
                    kwargs['mask'] = computed_masks
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                
                for x, y, mask in zip(reference_input_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```
With the corrected code, the function should now properly handle the cloning process and eliminate the previous error message.