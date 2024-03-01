### Bug Analysis:
The bug in the `_clone_functional_model` function seems to stem from the incorrect handling of the input tensors when creating a new model based on an existing model. The error message indicates that the function fails to compute an output tensor during the test case execution. This failure could be attributed to a mistake in the input tensor handling logic.

### Bug Location:
1. The function checks if the provided `model` is an instance of `Model`, but it does not handle the case where `model` might be an instance of `Sequential`. This oversight could result in the function raising an unnecessary error.
2. In the part where the function checks whether all input tensors come from a Keras layer, when creating new input layers for non-Keras tensors, it mistakenly appends these input layers to the `_input_tensors` list.
3. There's an issue in properly caching the newly created input layers when input tensors are provided.

### Bug Cause:
The root cause of the bug is the incorrect handling of the input tensors in multiple locations within the function. This leads to discrepancies in storing and using the input tensors and results in a failure to compute an output tensor during the test execution.

### Bug Fix Strategy:
To fix the bug in the function, we need to:
1. Handle the case where the provided `model` is an instance of `Sequential` to ensure the correct behavior.
2. Address the incorrect handling of input tensors by ensuring that the input layers are properly created and cached.
3. Verify that the input tensors are correctly mapped to the output tensors during model creation.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    input_layers = []
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape[1:], dtype=layer.dtype, sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            input_tensor = Input(tensor=x, name='input_wrapper_for_' + model._input_layers[i].name)
            input_layers.append(input_tensor)
            layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)
        
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                computed_tensors, computed_masks = zip(*computed_data)
                if 'mask' in kwargs and len(computed_data) == 1:
                    kwargs['mask'] = computed_masks[0]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        if x not in tensor_map:
            raise ValueError('Could not compute output ' + str(x))
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

With these corrections, the function should now properly handle the input tensors, create a new model, and compute the output tensors as expected.