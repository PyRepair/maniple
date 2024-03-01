### Analysis:
- The error message is showing an `AssertionError` when trying to compute the output tensor of a `Model`.
- The error originates from the `_clone_functional_model` function in the `keras/models.py` file.

### Bug:
- The bug is happening because the provided function is not correctly handling models with multiple outputs. 
- In the given test case, the model has multiple outputs, and the bug in the function is leading to a failure when trying to compute the output tensor.

### Bug Fix Strategy:
- To fix the bug, we need to ensure that the function correctly handles models with multiple outputs.
- Check the logic for handling model outputs and make sure that the output tensors are correctly computed and added to the `tensor_map`.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {} 
    tensor_map = {} 
    if input_tensors is None:
        input_tensors = [Input(shape=layer.get_input_shape_at(0)[1:]) for layer in model.layers if len(layer._inbound_nodes) == 0]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for layer in model.layers:
        if not layer in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
        else:
            layer = layer_map[layer]

        reference_input_tensors = []
        for node in layer._inbound_nodes:
            reference_input_tensors += node.input_tensors

        computed_data = []
        for x in reference_input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])

        if len(computed_data) == len(reference_input_tensors):
            kwargs = getattr(layer, 'arguments', {})
            if len(computed_data) == 1:
                computed_tensor, computed_mask = computed_data[0]
                if has_arg(layer.call, 'mask'):
                    if 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask
                output_tensors = to_list(layer(computed_tensor, **kwargs))
                computed_tensors = [computed_tensor]
            else:
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                if has_arg(layer.call, 'mask'):
                    if 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                output_tensors = to_list(layer(computed_tensors, **kwargs))

            for x, y in zip(layer._outbound_nodes, output_tensors):
                tensor_map[x.outbound_layer] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### Changes Made:
1. Replaced the logic for input tensor creation to handle models with multiple outputs correctly.
2. Updated the logic for iterating over layers and connecting them based on their inbound nodes.
3. Fixed the computation of output tensors and their addition to the `tensor_map`.

### This corrected version of the `_clone_functional_model` function should pass the failing test now.