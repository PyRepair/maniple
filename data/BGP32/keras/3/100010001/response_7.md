## Analysis
The buggy function `_clone_functional_model` is meant to clone a functional `Model` instance in Keras, creating new layers and weights instead of sharing the existing ones. The error message indicates that the assertion for computing the model outputs is failing, as it is unable to find a tensor in the `tensor_map`.

## Issues
1. In the input tensor handling section, the created `input_layers` list is empty, leading to not adding the input layers properly.
2. The for loop iterating over `model._input_layers` is incorrectly trying to create input tensors based on their configurations but not using them later.
3. In the section where node inputs are evaluated, the logic to handle multiple input tensors does not account for the case where some tensors are not available in the `tensor_map`.
4. The erroneous instantiation of `input_layers` list in the first issue affects the subsequent creation of placeholders, invalidating the tensor mapping.
5. There is missing logic to properly handle multiple output tensors from a single layer.

## Fix Strategy
1. Generate placeholder input tensors properly based on each input layer's configuration.
2. Correctly handle the input tensor mapping when creating new input layers.
3. Adjust the logic when computing node inputs to handle cases where not all tensors are available in the `tensor_map`.
4. Modify the logic for multiple output tensors from a single layer to ensure all output tensors are mapped correctly.

## Updated Corrected Version
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape[1:], dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
                        for layer in model.input_layers]
        for original, cloned in zip(model.input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model.input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
        
    for depth in sorted(model._nodes_by_depth, reverse=True):
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
            
            input_tensors = [tensor_map[x][0] for x in node.input_tensors if x in tensor_map]
            if len(input_tensors) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = layer(input_tensors, **kwargs)
                output_tensors = to_list(computed_tensors)
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By implementing the above corrections in the `_clone_functional_model` function, the issue with computing the model outputs in the failing test should be resolved.