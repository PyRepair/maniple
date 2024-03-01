### Analysis:
1. The function `_clone_functional_model` is supposed to clone a functional `Model` instance.
2. The error message indicates that the function fails with an assertion error stating that it could not compute the output for a specific tensor.
3. The function checks if the input `model` is an instance of `Model` and not a `Sequential` instance.
4. The error suggests that the tensor map does not contain the necessary information to compute the output properly.

### Bug:
The bug occurs because the tensor map does not contain the required information for computing the output of the model correctly.

### Fix:
We need to ensure that the tensor map accurately stores the values for the input and output tensors of the model.

### Revised Code:
Below is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    """Clone a functional `Model` instance.
    
    Model cloning is similar to calling a model on new inputs,
    except that it creates new layers (and thus new weights) instead
    of sharing the weights of the existing layers.
    
    # Arguments
        model: Instance of `Model`.
        input_tensors: optional list of input tensors
            to build the model upon. If not provided,
            placeholders will be created.
    
    # Returns
        An instance of `Model` reproducing the behavior
        of the original model, on top of new inputs tensors,
        using newly instantiated weights.
    
    # Raises
        ValueError: in case of invalid `model` argument value.
    """
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ' + str(model))
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead: ' + str(model))
    
    layer_map = {}
    tensor_map = {}
    
    if not input_tensors:
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
    
    for layer in model.layers:
        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer
    
    for node in reversed(model._nodes_by_depth[0]):
        layer = layer_map[node.outbound_layer]
        computed_data = [tensor_map[x] for x in node.input_tensors]
        
        if len(computed_data) == len(node.input_tensors):
            kwargs = node.arguments if node.arguments else {}
            computed_tensors, computed_masks = zip(*computed_data)
            if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                kwargs['mask'] = computed_masks
            output_tensors = to_list(layer(computed_tensors, **kwargs))

            for i, x in enumerate(node.output_tensors):
                tensor_map[x] = (output_tensors[i], None)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This revised version ensures that the tensor map stores the correct values for the input and output tensors of the model, allowing the function to successfully clone the functional model as expected.