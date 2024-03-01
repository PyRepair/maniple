After analyzing the buggy function and the failing test, we can identify the following potential error locations in the `_clone_functional_model` function:
1. The incorrect initialization of the `input_layers` list could cause issues in creating new input layers in the model.
2. There is a problem with the creation of `_input_tensors` list in the section where input tensors are validated to come from a Keras layer. This could lead to missing input tensors in the cloned model.
3. The iteration through model nodes might not handle cases where the layer does not support mask computation correctly, leading to issues in computing the output tensors.

The cause of the bug described in the GitHub issue is related to the issue in handling output masks when using a layer without mask support, such as the Lambda layer in the provided test script. This results in the error of not being able to compute the output tensor, as the output masks are consistently set to None.

To fix the bug, we need to ensure that the output masks are correctly handled when calling the layers, especially for layers without mask support.

Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

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
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for input_index, x in enumerate(input_tensors):
            if K.is_keras_tensor(x):
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_' + str(input_index))
                _input_tensors.append(input_tensor)
                layer_map[model._input_layers[input_index]] = input_tensor
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in range(model._output_coordinates[-1][0] + 1):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
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
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))

                output_tensors = to_list(output_tensors)
                for x, y in zip(reference_input_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

With this corrected version of the function, the issue reported in the GitHub bug report should be resolved, and the test function `test_clone_functional_model_with_multi_outputs` should now pass without any `Could not compute output Tensor` errors.