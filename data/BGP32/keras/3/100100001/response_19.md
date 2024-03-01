### Analysis:
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance in Keras, creating new layers with newly instantiated weights. The function iterates over nodes in the reference model, creates new layers if necessary, and builds up a map of input and output tensors. The bug causing the function to fail when cloning models with multiple outputs is likely related to how the output tensors are handled.

### Bug:
The bug arises from how output tensors are mapped in the function. When cloning a model with multiple outputs, the `output_tensors` are not correctly mapped to the corresponding output tensors of the cloned layers. This leads to incorrect outputs in the cloned model when they are copied over.

### Fix Strategy:
To fix the bug, we need to ensure that when a layer is called with multiple inputs or outputs, all the corresponding tensors and masks are correctly handled and mapped in the `tensor_map` dictionary. This involves modifying the section of the code where the output tensors are computed and mapped to their corresponding tensors in the `tensor_map`.

### Corrected Version:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                                dtype=layer.dtype,
                                sparse=layer.sparse,
                                name=layer.name) for layer in model.input_layers]

    for original, cloned in zip(model.input_layers, input_tensors):
        layer_map[original] = cloned

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in model._depth_nodes.keys():
        for node in model._depth_nodes[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]

            reference_input_tensors = node.input_tensors

            # Gather all the previous computed tensors and masks
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            # Call the layer
            computed_tensors = [data[0] for data in computed_data]
            computed_masks = [data[1] for data in computed_data]
            if has_arg(layer.call, 'mask'):
                kwargs = {'mask': computed_masks}
            else:
                kwargs = {}
                
            output_tensors = to_list(layer(computed_tensors, **kwargs))

            for node_output, output_tensor in zip(node.output_tensors, output_tensors):
                tensor_map[node_output] = (output_tensor, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version should now correctly clone the functional models with multiple outputs as intended.