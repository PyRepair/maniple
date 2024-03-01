### Analysis:
1. The `clone_functional_model` function is intended to clone a functional Keras `Model` instance.
2. The error message received is an `AssertionError` stating that it could not compute the output tensor.
3. This error occurs when trying to compute the output tensor in the cloned model.
4. The function iterates over the nodes in the model, cloning the layers and computing the output tensor based on the input tensors. The issue likely lies in how the input tensors are being managed or transformed.

### Bug in the Code:
1. The issue arises when trying to compute the output tensor in the cloned model. The input tensors might not be correctly mapped, leading to the failure to compute the output tensor.

### Fix Strategy:
1. Ensure that the correct input tensors are mapped to the corresponding layers during the cloning process.
2. Check how input tensors are handled in the code, especially for situations where multiple outputs are involved from a single layer.

### Corrected Version:
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
        for layer in model.inputs:
            input_tensor = Input(tensor=layer)
            layer_map[layer] = input_tensor
            input_tensors.append(input_tensor)
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model.inputs[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                layer_map[model.inputs[i]] = input_tensor
                input_tensors[i] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for node in model._nodes_by_depth[model._depth]: 
        inbound_layers = node.inbound_layers
        computed_data = []  # List of tuples (input, mask).
        for x in node.input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])

        if len(computed_data) == len(node.input_tensors):
            kwargs = node.arguments if node.arguments else {}
            if len(computed_data) == 1:
                computed_tensor, computed_mask = computed_data[0]
            else:
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                kwargs['mask'] = computed_masks if has_arg(node.outbound_layer.call, 'mask') else None

            output_tensors = to_list(node.outbound_layer(computed_tensors, **kwargs))
            output_masks = to_list(node.outbound_layer.compute_mask(computed_tensors, computed_masks))

            if len(output_tensors) == 1:
                output_tensors = output_tensors[0] 
                output_masks = output_masks[0]

            for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, to_list(output_tensors), name=model.name)
```

This corrected version of the `_clone_functional_model` function should properly clone the functional Keras `Model` instance while correctly handling the input tensors and computing the output tensors.