### Analysis:
The `_clone_functional_model` function is intended to clone a functional model by creating new layers and weights. However, there are several potential errors within the function that could be causing bugs:
1. Incorrect handling of input layers and their corresponding placeholders.
2. Possible errors in creating input layer placeholders.
3. Mismanagement of input tensors when not provided explicitly.
4. Issues with caching input layers and corresponding tensors.
5. Mismatch between the reference input tensors and actual input tensors.
6. Incorrect handling of multiple computed data inputs.
7. Potential errors in updating the tensor_map with output tensors.

### Bug Cause:
The bug in the function arises from the incorrect handling of the creation and mapping of input tensors and layers when input_tensors are not provided explicitly. This leads to discrepancies in the caching of input layers, reference tensors, and newly created tensors. Additionally, issues with handling the computed data from reference input tensors result in incorrect mappings and computations.

### Bug Fix Strategy:
To fix the bug in the function, we need to focus on correcting the creation and mapping of input layers and tensors, ensuring proper handling of computed data inputs, and correctly updating the tensor_map with output tensors. Additionally, we should ensure that the model outputs are correctly computed and included in the final cloned model.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  

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

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in range(len(model._nodes_by_depth) - 1, 0, -1):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensor, computed_mask))
                    computed_tensors = [computed_tensor]
                    computed_masks = [computed_mask]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By restructuring the creation and mapping of input tensors and layers, correcting the computed data inputs handling, and ensuring the proper update of tensor_map with output tensors, the corrected version of the function should now work as intended.