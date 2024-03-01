The bug in the `_clone_functional_model` function is due to the incorrect handling of the mapping between original input tensors and cloned input tensors. The function fails to correctly update the `layer_map` and `tensor_map` dictionaries during the cloning process, leading to incorrect mapping and mismatch in the output tensors of the cloned model.

To fix this bug, we need to ensure that the mapping between the original input tensors and cloned input tensors is correctly maintained throughout the cloning process. This involves updating the `layer_map` and `tensor_map` dictionaries appropriately for each input tensor and its corresponding layer.

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
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = y

    # Clone the model layer by layer
    layer_config = model.get_config()
    layers = []
    for layer in layer_config['layers']:
        class_name = layer['class_name']
        new_layer = K.layer.deserialize(layer, custom_objects={})
        layers.append(new_layer)

    new_model = Model(input_tensors, [layer.output for layer in layers], name=model.name)
    return new_model
```

By correctly updating the `layer_map` and `tensor_map` dictionaries and cloning the model layer by layer, we ensure that the input tensors are correctly mapped in the cloned model, addressing the bug.