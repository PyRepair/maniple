The bug in the `_clone_functional_model` function is due to the incorrect handling of the input layers and their corresponding tensors. In the function, it fails to correctly map the input tensors to the input layers, resulting in incorrect processing and subsequent errors in model cloning.

To fix the bug, we need to ensure that the input tensors are correctly mapped to the input layers and that the model's outputs are accurately computed based on the input tensors.


Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape[1:],
                                 dtype=layer.dtype,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor

    else:
        # Make sure that all input tensors come from a Keras layer.
        # If tensor comes from an input layer: cache the input layer.
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                layer_map[model._input_layers[i]] = input_tensor
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer.
            inbound_layers = []
            for i in range(len(node.inbound_layers)):
                x = node.input_tensors[i]
                if x in tensor_map:
                    inbound_layers.append(tensor_map[x][0])
            kwargs = {}
            if node.arguments:
                kwargs = node.arguments
            new_node = node.__class__(node.outbound_layer,
                                      inbound_layers,
                                      node.node_indices,
                                      node.tensor_indices,
                                      kwargs)
            for x, y in zip(node.output_tensors, new_node.output_tensors):
                tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

By correcting the mapping of input tensors to input layers and ensuring correct computation of output tensors, the corrected `_clone_functional_model` function should now pass the failing test function `test_clone_functional_model_with_multi_outputs`.