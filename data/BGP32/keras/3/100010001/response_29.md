## Analysis:
The error message indicates that the issue occurs during the cloning of a functional model. The specific error is related to not being able to compute the output tensor for a layer named 'swap_layer_1'. This error suggests that there is a problem in the `_clone_functional_model` function where the output tensors are not being properly computed or mapped.

## Bug:
The bug in the `_clone_functional_model` function is due to incorrect handling when cloning layers and their respective tensors. The issue arises during the computation and mapping of output tensors, leading to the inability to compute the final output tensor.

## Solution:
To fix the bug, we need to ensure that the mapping of input tensors is done correctly, and the computation of output tensors is properly handled for all layers in the model.

## Corrected Function:
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
        input_tensors = [Input(shape=layer.input.shape[1:]) for layer in model.layers if isinstance(layer, InputLayer)]

    for orig_input, new_input in zip(model.inputs, input_tensors):
        tensor_map[orig_input] = new_input

    for layer in model.layers:
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer

    for layer in model.layers:
        new_layer = layer_map[layer]
        node_indices = [model.locate_inbound_nodes(tensor) for tensor in layer.input]
        inputs = [tensor_map[x] for x in layer.input]
        if len(inputs) == 1:
            new_tensor = new_layer(inputs[0])
        else:
            new_tensor = new_layer([K.identity(x) for x in inputs])

        new_output = new_tensor
        if isinstance(new_output, list):
            for output_index in range(len(layer.output)):
                tensor_map[K.identity(layer.output[output_index])] = K.identity(new_output[output_index])
        else:
            tensor_map[K.identity(layer.output)] = K.identity(new_output)

    output_tensors = [tensor_map[x] for x in model.outputs]
    return Model(inputs=input_tensors, outputs=output_tensors)
```

By revising the function to properly handle the mapping of input and output tensors for all layers, the bug should be fixed. This corrected version will ensure that the functional model is cloned with proper computation and mapping of tensors.