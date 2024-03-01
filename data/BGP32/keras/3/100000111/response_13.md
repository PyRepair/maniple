### Analysis:
1. The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones.
2. The function is meant to handle models with different types of layers, including `Lambda` layers, which might not support masking.
3. The issue reported on GitHub involves using `clone_model` with `multi_gpu_model` and `cpu_relocation=True`, resulting in an error related to not being able to compute an output tensor.
4. The cause of the bug seems to be related to the handling of output masks for layers that do not support masking, such as `Lambda` layers.
5. To fix this bug, we need to update the handling of output masks specifically in cases where the layer does not support masks.

### Suggested Strategy for Fixing the Bug:
1. Identify the point where the output masks are handled in the function.
2. Check if the layer supports masking before trying to compute masks.
3. Modify the logic to handle layers without mask support appropriately.
4. Ensure that the `Model` instance is still correctly reproduced with the new inputs and outputs.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
                         for layer in model._input_layers]
        layer_map = {layer: input_layer for layer, input_layer in zip(model._input_layers, input_tensors)}
    else:
        input_tensors = to_list(input_tensors)
        for i, tensor in enumerate(input_tensors):
            if not K.is_keras_tensor(tensor):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=tensor, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            computed_data = [(tensor_map[x] if x in tensor_map else None) for x in node.input_tensors]
            if all(computed_data):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                computed_tensors = computed_tensors if len(output_tensors) == 1 else output_tensors
                tensor_map.update({x: (y, None) for x, y in zip(node.output_tensors, output_tensors)})

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### Explanation of the Correction:
1. Modified the creation of input tensors and the mapping between input layers and tensors.
2. Updated the handling of computed data to check for available tensors in tensor_map.
3. Adjusted the logic for output tensor computation to handle layers without mask support.
4. Ensured that the output tensors are correctly updated in the tensor_map.
5. Returned a new `Model` instance with the correct input and output tensors.