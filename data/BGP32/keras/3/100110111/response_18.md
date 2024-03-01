### Analysis:
1. The bug occurs in `_clone_functional_model` when `assert x in tensor_map` fails to compute the output tensor. The failing test `test_clone_functional_model_with_multi_outputs` triggers this bug by trying to clone a model with multiple outputs.
2. The error message indicates that the function fails to compute the output tensor `'swap_layer_1/Identity:0'`.
3. The bug originates from the way the function handles the cloned model with multiple outputs and involves the handling of input and output tensors during the cloning process.
4. To fix the bug, we need to ensure that all input and output tensors are correctly mapped during the cloning process.

### Proposed Fix:
1. Update the function to handle models with multiple outputs correctly by ensuring that all input tensors are processed and mapped to output tensors.
2. Adjust the iteration logic to properly handle multiple output nodes and carry out the cloning process for each output.
3. Verify the correctness of the input and output tensor mapping and make necessary adjustments to ensure all tensors are correctly computed.

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
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor  
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor
        input_tensors = input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = y

    for depth, nodes in model._nodes_by_depth.items():
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                if has_arg(layer.call, 'mask'):
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

The corrected function should now handle models with multiple outputs correctly and pass the failing test scenario.