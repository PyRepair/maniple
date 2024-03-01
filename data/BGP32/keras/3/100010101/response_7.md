### Strategy for fixing the bug
1. The error message indicates that the function expects the input model to be a `Model` instance, but it is receiving a `Sequential` instance. To fix this, we need to modify the function to handle this case appropriately.
2. We need to ensure that the input tensors provided belong to Keras layers.
3. In the provided test case, there are multiple outputs from the layers involved. We need to ensure that the correct tensors are computed and mapped during the cloning process.

### Code Fix
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        # Create placeholders to build the model on top of
        input_tensors = [Input(batch_shape=input_layer.batch_input_shape, dtype=input_layer.dtype, 
                               sparse=input_layer.sparse, name=input_layer.name) for input_layer in model._input_layers]
    else:
        # Ensure all input tensors are from a Keras layer
        input_tensors = [Input(tensor=x) if not K.is_keras_tensor(x) else x for x in to_list(input_tensors)]

    # Populate tensor_map with input tensors
    tensor_map.update({x: (y, None) for x, y in zip(model.inputs, input_tensors)})

    # Iterate over each node in the model
    for depth in model._nodes_by_depth:
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            # Get or create layer
            if layer not in layer_map:
                layer_config = layer.get_config()
                new_layer = layer.__class__.from_config(layer_config)
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            # Get inputs and call the new layer
            computed_data = [tensor_map[x] for x in node.input_tensors if x in tensor_map]

            if len(computed_data) == len(node.input_tensors):
                # Call the layer
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                if len(computed_data) == 1:
                    computed_tensors = computed_tensors[0]
                    computed_mask = computed_masks[0]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask
                else:
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                if hasattr(layer, 'compute_mask'):
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                else:
                    output_masks = [None] * len(output_tensors)

                # Update tensor_map
                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    # Check if all model outputs were computed and generate the new model
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
``` 

The corrected function ensures that the inputs are validated, layers are cloned correctly, and the model is reconstructed with the expected output tensors.