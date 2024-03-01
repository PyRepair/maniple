### Analysis:
1. **Buggy Function Relationship with Test Code and Error Message**:
   - The test function `test_clone_functional_model_with_multi_outputs()` calls `keras.models.clone_model(model)` with a model having multiple outputs.
   - The error message occurs during the test execution indicating a failure in the `keras.models.clone_model(model)` call.
   - The error message states that a specific output tensor is not computed, leading to an assertion failure.

2. **Identified Bug**:
   - The bug arises during the execution of `_clone_functional_model` in the aspect of correctly cloning the model with multiple outputs.
   - The function fails to handle layers without masking support, which leads to the error when trying to compute the output tensor.

3. **Bug Cause**:
   - The error message points to the failure in computing the output tensor `<tf.Tensor 'swap_layer_1/Identity:0' shape=(?, 4) dtype=float32>`.
   - The issue relates to how the function handles layers without masking support like the Lambda layer, resulting in missing computations for output tensors.
   
4. **Bug Fix Strategy**:
   - Update the `_clone_functional_model` function to properly handle layers without masking support while processing the new model creation.
   - Avoid calling `layer.compute_mask()` on layers that do not support masking to prevent the issue observed in the failing test.

### Bug-fixed Function:
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
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
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
        tensor_map[x] = (y, None)

    for layer in model._layers:
        if layer._inbound_nodes:
            input_tensors = []
            for node_index, inbound_node in enumerate(layer._inbound_nodes):
                output_tensors = inbound_node.output_tensors
                computed_data = []
                for x in inbound_node.input_tensors:
                    if x in tensor_map:
                        computed_data.append(tensor_map[x])

                if len(computed_data) == len(inbound_node.input_tensors):
                    if inbound_node.arguments:
                        kwargs = inbound_node.arguments
                    else:
                        kwargs = {}

                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                    for x, y in zip(output_tensors, output_tensors):
                        tensor_map[x] = (y, None)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

After applying this fix, the corrected function should be able to handle multiple outputs, including those from layers without masking support, addressing the issue raised in the GitHub report and passing the failing test case.