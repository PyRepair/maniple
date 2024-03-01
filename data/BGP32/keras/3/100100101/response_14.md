The bug in the `_clone_functional_model` function leads to incorrect copying of the model layers and their connections. The bug prevents the correct creation of a cloned model, resulting in failing test cases.

### Bug Explanation:
The bug is primarily due to the misuse of input layers and the missing linkage in the layer mapping process. When creating placeholders and input layers during cloning, the relationships between the original layers and the newly created layers are not correctly stored in the `layer_map`. This causes inconsistencies in handling input tensors and propagating the changes through the model structure.

### Bug Fix Strategy:
1. Ensure that the relationships between original layers and newly created layers are correctly mapped in the `layer_map`.
2. Make sure to populate and maintain the `layer_map` consistently throughout the layer cloning process.
3. Properly link the input tensors in the `tensor_map` to reflect the relationships between the original and cloned layers.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                               sparse=layer.sparse, name=layer.name) for layer in model._input_layers]

        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in range(len(model._nodes_by_depth)):
        nodes = model._nodes_by_depth[depth]

        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                cloned_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = cloned_layer

            cloned_layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(cloned_layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask
                    output_tensors = to_list(cloned_layer(computed_tensor, **kwargs))
                    output_masks = to_list(cloned_layer.compute_mask(computed_tensor, computed_mask))
                    computed_tensors = [computed_tensor]
                    computed_masks = [computed_mask]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    if has_arg(cloned_layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                    output_tensors = to_list(cloned_layer(computed_tensors, **kwargs))
                    output_masks = to_list(cloned_layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected function fixes the issues in mapping the layers and correctly propagating the relationships between the original layers and the cloned layers, ensuring the cloning process operates as expected.