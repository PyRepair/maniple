### Analysis:
- The error message indicates that the function is unable to compute the output for a specific tensor, leading to an assertion error.
- The function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones. It involves copying layers, handling input tensors, and computing output tensors.
- The expected values and types provided give insight into the state of variables before the return, showing discrepancies in assignments and processing.
- The GitHub issue points out a scenario where the error occurs due to the absence of mask support in a layer, leading to the failure of computing output masks.

### Bug:
The bug in the function arises from incorrect handling of input tensors, missing layer cloning, and issues with computing output tensors especially when masks are involved.

### Fix Strategy:
1. Ensure correct creation and mapping of input tensors.
2. Address the cloning of layers and reusing already cloned layers to avoid duplication.
3. Handle situations where layers do not support masks during output computation.

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
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor

    input_tensors = to_list(input_tensors)
    for i, x in enumerate(input_tensors):
        if not K.is_keras_tensor(x):
            name = model._input_layers[i].name
            input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
            input_tensors[i] = input_tensor
            layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in list(model._nodes_by_depth):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            computed_data = []

            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(new_layer(computed_tensor, **kwargs))
                else:
                    computed_tensors, _ = zip(*computed_data)
                    output_tensors = to_list(new_layer(computed_tensors, **kwargs))

                if len(output_tensors) != len(reference_output_tensors):
                    raise ValueError('Inconsistent number of output tensors!')

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        if x not in tensor_map:
            raise ValueError('Could not compute output', x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```