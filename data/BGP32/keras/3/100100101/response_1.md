The bug in the `_clone_functional_model` function lies in the creation of input placeholders and the mapping of input tensors.

### Bug Explanation:
1. In the initial `if input_tensors is None` block, the code fails to create `input_layers` list which is intended to store the input layers. This results in an empty `input_layers` list which leads to missing mappings in `layer_map`.
2. Due to the missing input layers in `input_layers`, the subsequent loop to assign mappings from original to newly created input layers fails to assign correct values to `layer_map`.
3. This bug causes incorrect mappings in `tensor_map` and ultimately leads to the model not being able to compute the output correctly.

### Fix Strategy:
To fix this bug, we need to ensure that the `input_layers` list is properly created and used to maintain the correct mapping in `layer_map`.

### Corrected Code:
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
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        # Create placeholders to build the model on top of
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_layers.append(input_tensor._keras_history[0])
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor._keras_history[0]

    else:
        # Make sure that all input tensors come from a Keras layer
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Rest of the function remains unchanged
```

By making the above fixes, the `_clone_functional_model` function should now be able to correctly clone the model as intended.