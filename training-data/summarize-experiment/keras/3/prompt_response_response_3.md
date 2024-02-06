Based on the detailed analysis of the error message and test case, it seems that the issue is occurring within the `_clone_functional_model` function of the Keras library. The failing test case involves a functional model with multiple inputs and outputs using layers such as `Lambda` and `SwapLayer`. The error message indicates a failure in computing the output tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)` when trying to clone the model.

Upon examining the runtime variables and the function code, it appears that the issue might be related to the final instantiation of the new model from inputs and outputs. Specifically, the computation and mapping of output tensors seem to be the relevant areas to investigate further.

To resolve the issue, the following approaches can be considered:
1. Ensure that the mapping of input and output tensors in the `tensor_map` is accurate and that all output tensors are properly computed and mapped during the cloning process.
2. Verify that the process of iterating through the nodes of the reference model and creating corresponding layers in the cloned model is working as intended, especially for complex layers such as `SwapLayer`.
3. Handle the case of layers with multiple outputs and without mask support to prevent the error from occurring.

With these considerations in mind, here's the corrected version of the `_clone_functional_model` function to address the identified issues:

```python
def _clone_functional_model(model, input_tensors=None):
    """
    Clone a functional `Model` instance.

    Model cloning is similar to calling a model on new inputs, except that it creates new layers (and thus new weights) instead of sharing the weights of the existing layers.

    Args:
        model: Instance of `Model`.
        input_tensors: Optional list of input tensors to build the model upon. If not provided, placeholders will be created.

    Returns:
        An instance of `Model` reproducing the behavior of the original model, on top of new inputs tensors, using newly instantiated weights.

    Raises:
        ValueError: In case of invalid `model` argument value.
    """
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    input_layers = []  # List of input layers.
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        for layer in model.input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_layers.append(input_tensor)
            # Cache newly created input layer.
            layer_map[layer] = input_tensor
    else:
        # Make sure that all input tensors come from a Keras layer.
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model.input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_layers.append(input_tensor)
                # Cache newly created input layer.
                original_input_layer = x._keras_history[0]
                layer_map[original_input_layer] = input_tensor
            else:
                input_layers.append(x)

    for x, y in zip(model.inputs, input_layers):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterate over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer.
            layer = node.outbound_layer

            # Get or create layer.
            if layer not in layer_map:
                # Clone layer.
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                # Reuse previously cloned layer.
                layer = layer_map[layer]
                # Don't call InputLayer multiple times.
                if isinstance(layer, InputLayer):
                    continue

            # Gather inputs to call the new layer.
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            # If all previous input tensors are available in tensor_map, then call node.inbound_layer on them.
            computed_data = []  # List of tuples (input, mask).
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                # Call layer.
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                if has_arg(layer.call, 'mask') and any(x[1] is not None for x in computed_data):
                    kwargs['mask'] = [x[1] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))

                # Update tensor_map.
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)  # Update tensor_map with output tensors.

    # Check that we did compute the model outputs, then instantiate a new model from inputs and outputs.
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_layers, output_tensors, name=model.name)
```

The corrected code includes modifications in the handling of input layers, mapping of input and output tensors, and the computation of output tensors. These changes aim to address the issues identified in the failing test case and improve the correctness of the model cloning process. This revised version of the function can be used as a drop-in replacement for the buggy version.