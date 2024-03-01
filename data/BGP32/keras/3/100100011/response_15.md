### Analysis:
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones. The function is failing to properly clone a model with multi-output layers, leading to errors in the `test_clone_functional_model_with_multi_outputs` test.

The GitHub issue highlights a similar problem with the `clone_model` function, pointing out that the error occurs when using a functional model with multi-output layers without mask support, leading to a `Could not compute output Tensor` error.

### Bugs:
1. The function fails to properly handle multiple output layers when cloning a model.
2. When an output tensor does not have a mask, the function results in None values for `output_masks`.

### Bug Fix Strategy:
1. Ensure that the function can handle models with multiple output layers properly.
2. Modify the logic to handle cases where the mask for an output tensor is None.

### Bug-fixed Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(shape=layer.output_shape[1:])  # Use output shape to create input tensor
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor._keras_history[0]
    
    for layer, new_layer in zip(model._input_layers, input_tensors):
        layer_map[layer] = new_layer

    for node in model._nodes_by_depth():
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
            output_tensors = to_list(layer(computed_tensors, **kwargs))

            for x, y in zip(node.output_tensors, output_tensors):
                tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

The bug-fixed function addresses the issues with multiple output layers and the handling of masks for output tensors. It should now correctly clone a functional model instance.