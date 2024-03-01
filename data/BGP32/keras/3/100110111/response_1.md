### Analysis:
1. The function `_clone_functional_model` is designed to clone a functional `Model` instance by creating new layers and weights. The issue seems to arise when dealing with multi-output layers that do not support masks. The failing test involves a model with multi outputs and a `Lambda` layer that does not support masks.
2. The error occurs when trying to compute the output tensor of the model. The failing assertion checks if the output tensor is present in the `tensor_map`, which it is not due to the lack of mask support with certain layers.
3. The failing test requires cloning a model with multiple outputs where one of the layers does not support masks. The error message indicates that the expected output tensor could not be computed.
4. To address this issue, we need to modify the logic inside the `_clone_functional_model` function to handle cases where layers do not support masks properly. We should skip mask-related computations for such layers.
5. Let's propose a corrected version of the `_clone_functional_model` function.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                computed_tensors = [x[0] for x in computed_data]
                
                if len(computed_data) == 1:
                    output_tensors = to_list(layer(computed_tensors[0], **kwargs))
                else:
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version avoids handling masks for layers that do not support them, enabling the successful cloning of models with multi-output layers, as encountered in the failing test.