### Analysis:
- The function `_clone_functional_model` is intended to create a cloned version of a given functional model but with new layers and new weights instead of sharing existing ones.
- The error message indicates an assertion failure during the cloning process, specifically in checking if the output tensors of the model have been computed.
- The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs and then attempts to clone it.
- The error message shows that the function fails to compute the output corresponding to a specific Tensor in the model, leading to the assertion error.

### Bug Cause:
- The bug occurs because the function fails to properly compute the output tensors while cloning the model, resulting in missing output tensors.
- The code in the function that iterates over nodes and computes the outputs is not correctly updating the `tensor_map` for all output tensors.

### Bug Fix Strategy:
1. Check the computation logic for updating the `tensor_map` with the correct output tensors.
2. Ensure that all references to input and output tensors are correctly handled during the cloning process.

### Corrected Function:
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
            input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            input_layers.append(input_tensor)
            layer_map[layer] = input_tensor

        for original, cloned in zip(model._input_layers, input_layers):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[x] = input_tensor

        for x, y in zip(model.inputs, input_tensors):
            tensor_map[x] = y, None

    for depth in list(model._nodes_by_depth.keys())[::-1]:
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
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

                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask

                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensor, computed_mask))
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                    if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks

                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = y, mask

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

After applying the necessary corrections to the `tensor_map` updates, the function should now correctly clone the functional model without encountering the assertion error in the failing test.