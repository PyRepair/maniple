### Analysis:
1. The `_clone_functional_model` function is intended to clone a given functional `Model` instance by creating new layers and new weights instead of sharing existing ones. The function checks if the input `model` is of type `Model` and not of type `Sequential` before proceeding.
2. The test function `test_clone_functional_model_with_multi_outputs` creates a model with multiple input and output layers, including a Lambda layer and a custom SwapLayer. After creating the model, it tries to clone it using `keras.models.clone_model`, which internally calls the `_clone_functional_model` function.
3. The error occurs during the test because the "Could not compute output" assertion fails in the `_clone_functional_model` function due to the incorrect identification of tensors. The issue in GitHub also highlights a similar problem during model cloning with multi-gpu support.
   
### Cause of the Bug:
The bug arises from the tensor mapping in the `_clone_functional_model` function not properly handling the case where output tensors come from layers that can't provide masks (such as Lambda layers). This leads to a discrepancy in the mapping of output tensors resulting in the "Could not compute output" error. The bug is highlighted in the failing test function when trying to clone a model with multiple outputs.

### Suggested Fix:
To fix the bug, we need to enhance the logic around handling output tensors and masks, especially when dealing with layers like Lambda that do not support masking. We need to ensure that the output masks are handled correctly during the cloning process.

### Corrected Code:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, input_tensor in enumerate(input_tensors):
            if not K.is_keras_tensor(input_tensor):
                name = model._input_layers[i].name
                new_input_tensor = Input(tensor=input_tensor, name='input_wrapper_for_' + name)
                input_tensors[i] = new_input_tensor
                layer_map[input_tensor._keras_history[0]] = new_input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in reversed(range(len(model._nodes_by_depth))):
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
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    for x in model.outputs:
        if x not in tensor_map:
            raise AssertionError('Could not compute output ' + str(x))
    
    return Model(input_tensors, [tensor_map[x][0] for x in model.outputs], name=model.name)
```

The corrected code enhances the logic for handling input tensors, mapping tensors, and computing output tensors and masks during the model cloning process, ensuring that the output tensors are correctly computed and mapped. This updated function should now pass the failing test and address the reported issue on GitHub.