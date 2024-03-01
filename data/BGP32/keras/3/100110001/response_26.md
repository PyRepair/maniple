### Analysis:
1. The failing test is trying to call `keras.models.clone_model(model)` where `model` is an instance of `keras.Model`.
2. The error message indicates that the code is failing at the assertion `assert x in tensor_map, 'Could not compute output ' + str(x)`.
3. The error occurs in the `_clone_functional_model` function, specifically in the part where it checks if the output tensor has been computed correctly.
4. The error is likely due to the output tensor `x` not being found in the `tensor_map`, indicating that the computation for that output was not successful.
5. The bug is likely related to the handling of input and output tensors during the cloning process within the `_clone_functional_model` function.

### Bug Fix Strategy:
1. Improve the handling of input and output tensors during the cloning process.
2. Ensure that input and output tensors are correctly mapped in the `tensor_map`.
3. Check the computation of each output tensor so that they are properly calculated and stored in the `tensor_map`.

### Bug Fix and Corrected Version:
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
            # Cache newly created input layer.
            input_layers.append(input_tensor)
            layer_map[layer] = input_tensor

        for _original, _cloned in zip(model._input_layers, input_layers):
            layer_map[_original] = _cloned

    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []

        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)

        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)

    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]

        for node in nodes:
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
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                if has_arg(layer.call, 'mask'):
                    if 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
``` 

The corrected version of the `_clone_functional_model` function modifies the logic for handling input and output tensors during the cloning process to ensure that the computations are properly stored in the `tensor_map`. This updated version should resolve the bug and pass the failing test.