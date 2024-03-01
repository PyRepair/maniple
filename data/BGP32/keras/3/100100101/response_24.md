### Bug Explanation:
The bug in the `_clone_functional_model` function lies in the handling of input tensors when cloning a model. When cloning a model with multiple outputs, the function is not correctly setting up the input tensors and mapping them to the corresponding layers. This leads to a mismatch between the original model and the cloned model, resulting in incorrect predictions.

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the input tensors are properly created and mapped to the corresponding layers during the model cloning process. This involves correctly handling the input tensors and updating the layer mappings to maintain consistency between the original and cloned models.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in reversed(range(len(model._nodes_by_depth))):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            computed_data = [
                tensor_map[x] if x in tensor_map else (x, None) for x in reference_input_tensors
            ]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                output_tensors = to_list(layer([x[0] for x in computed_data], **kwargs))
                output_masks = to_list(layer.compute_mask([x[0] for x in computed_data], [x[1] for x in computed_data]))

                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

After applying this correction, the `_clone_functional_model` function should now properly handle the cloning of a functional model with multiple outputs as expected, passing the failing test case provided.