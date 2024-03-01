### Analysis:
1. The `clone_model` function in the failing test is supposed to clone a functional model but encounters an issue related to `clone_functional_model`.
2. The failing test aims to clone a model with multiple outputs, including a Lambda layer and a custom layer, resulting in the error while trying to compute the output tensor from a SwapLayer.
3. The error message indicates that the `tensor_map` does not contain the output tensor of the layer "swap_layer_1/Identity:0".
4. The bug seems to be related to the handling of multiple output layers and the absence of masks for specific layers, causing a mismatch in tensor mapping.
5. To fix the bug, adjustments need to be made in the logic of creating layers and mapping tensors to ensure all output tensors are correctly accounted for.

### Fix Strategy:
1. Ensure that all output tensors are appropriately mapped in `tensor_map`.
2. Check the conditions for handling different types of layers such as InputLayer and avoid unnecessary re-calling of InputLayer.
3. Implement robust layer cloning logic to handle multiple outputs and the absence of computed masks.

### Corrected Function:
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
            layer_map[layer] = input_tensor
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[x._keras_history[0]] = input_tensor
        input_tensors = input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    depth_keys = sorted(model._nodes_by_depth.keys(), reverse=True)
    for depth in depth_keys:
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
                computed_masks = [x[1] for x in computed_data]

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
The corrected function addresses the issues related to mapping tensor outputs and handling different layer types to ensure the proper cloning of the functional model.