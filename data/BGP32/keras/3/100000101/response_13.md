The bug in the provided `_clone_functional_model` function lies in the incorrect creation and update of input_tensors and layer_map dictionaries, leading to a mismatch and inconsistency in tensor mappings and layer mapping. To fix this bug, we need to ensure that the input tensors are correctly created and mapped to the corresponding layers.

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
        # Create placeholders to build the model on top of.
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
        
    for orig_input_layer, cloned_input_layer in zip(model._input_layers, input_tensors):
        layer_map[orig_input_layer] = cloned_input_layer

    for node in model._nodes_by_depth:
        reference_input_tensors = node.input_tensors
        reference_output_tensors = node.output_tensors

        computed_data = []
        for x in reference_input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])
        
        if len(computed_data) == len(reference_input_tensors):
            computed_tensors, computed_masks = zip(*computed_data)
            kwargs = {} if not node.arguments else node.arguments
            output_tensors = to_list(layer(*computed_tensors, **kwargs))
            output_masks = to_list(layer.compute_mask(*computed_tensors, **kwargs))

            for ref_output, out_tensor, out_mask in zip(reference_output_tensors, output_tensors, output_masks):
                tensor_map[ref_output] = (out_tensor, out_mask)

    output_tensors = [tensor_map[output_tensor][0] for output_tensor in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

By correcting the handling of input_tensors creation and mapping, as well as ensuring consistency in updating tensor_map and layer_map dictionaries, the function should now correctly clone the functional model with the provided input tensors.

Make sure to test this corrected version with the provided expected values and types of variables to validate its correctness.