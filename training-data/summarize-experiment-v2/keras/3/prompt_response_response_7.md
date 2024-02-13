The bug in the `_clone_functional_model` function is likely caused by incorrect handling of input and output tensors, as well as improper caching and mapping of layers. This results in the assertion error indicating that the output tensor is not present in the `tensor_map`.

To fix this bug, the function needs to be refactored to properly handle input layers and nodes, compute output tensors, and handle input tensors consistently. Additionally, the layer mapping and caching should be carefully managed to avoid duplication and retain the intended behavior of the cloned model.

Here is the corrected version of the `_clone_functional_model` function that addresses the identified issues:

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
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]

    tensor_map = dict(zip(model.inputs, input_tensors))
    
    cloned_layers = {}
    for layer in model.layers:
        config = layer.get_config()
        new_layer = layer.__class__.from_config(config)
        new_layer.build(layer.input_shape)
        cloned_layers[layer] = new_layer

    for layer in model.layers:
        new_layer = cloned_layers[layer]
        if isinstance(layer, InputLayer):
            continue
        inbound_tensors = [tensor_map[x] for x in layer._inbound_nodes[0].input_tensors]
        kwargs = layer._inbound_nodes[0].arguments
        new_output_tensors = new_layer(inbound_tensors, **kwargs)
        for orig, new in zip(layer._inbound_nodes[0].output_tensors, new_output_tensors):
            tensor_map[orig] = new

    cloned_inputs = [tensor_map[x] for x in model.inputs]
    cloned_outputs = [tensor_map[x] for x in model.outputs]

    return Model(cloned_inputs, cloned_outputs, name=model.name)
```

This corrected version of the `_clone_functional_model` function should address the identified issues and pass the failing test. Additionally, it should also resolve the issue reported in the GitHub bug by properly handling input and output tensors, as well as caching and mapping of layers.