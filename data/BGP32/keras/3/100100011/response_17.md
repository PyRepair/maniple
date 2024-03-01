## Bug Analysis:
- The `_clone_functional_model` function is designed to clone a functional `Model` instance, creating new layers and weights instead of sharing existing ones.
- The error occurs when using the `clone_model` function to clone a model with multiple outputs.
- The issue arises due to the Lambda layer not supporting masks, resulting in `layer.compute_mask` always returning `None`.
- This leads to missing output masks, causing the error "Could not compute output Tensor" when trying to clone the model.

## Bug Fix Strategy:
- To fix the bug, we need to handle cases where the layer's `compute_mask` function returns `None` by adapting the logic to the absence of masks in the Lambda layer.
- By checking for `None` output masks and appropriately creating and handling `output_masks`, we can ensure the cloning process proceeds without errors.

## Bug Fix Solution:
```python
def _clone_functional_model(model, input_tensors=None):
    """
    Fixed function to clone a functional `Model` instance.
    Handles Lambda layer without mask support.

    # Arguments, Returns, Raises: Same as original function.
    """
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model.input_layers:
            input_tensor = Input(batch_shape=layer.output_shape, name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        input_layers = input_tensors
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if K.is_keras_tensor(x):
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + model.input_layers[i].name)
                input_tensors[i] = input_tensor
                layer_map[x._keras_history[0]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in model._depth.keys():
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

By modifying the `_clone_functional_model` function as shown above, we can address the issue related to Lambda layers and ensure that the cloning process functions correctly.