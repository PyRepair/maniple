### Analysis:
1. The buggy function `_clone_functional_model` is supposed to clone a functional `Model`, creating new layers and new weights without sharing weights from the original model.
2. The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple output tensors and then tries to clone it using `keras.models.clone_model`.
3. The error message indicates that the assertion `assert x in tensor_map` fails, specifically for the output tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`. This suggests that the output tensor is not found in the `tensor_map`, meaning it was not computed while trying to clone the model.
4. The potential cause of the bug lies in how the input tensors are being processed and mapped to new tensors in the `tensor_map` dictionary. The function may not properly track the relationships between input and output tensors during the cloning process.

### Strategy to Fix the Bug:
1. Ensure that all input tensors are properly mapped to corresponding output tensors in the `tensor_map` dictionary while cloning the model.
2. Check the condition where computed input tensors need to be matched with reference input tensors and adjust the logic to handle all cases correctly.
3. Verify that the layer mapping is correctly implemented for both new and reused layers during the cloning process.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
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
            input_layer = model._input_layers[i]
            if not K.is_keras_tensor(x):
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + input_layer.name)
                layer_map[input_layer] = input_tensor
            else:
                layer_map[input_layer] = x

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in range(len(model._nodes_by_depth)):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            computed_data = []
            for x in node.input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                input_data = [x[0] for x in computed_data]
                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = [x[1] for x in computed_data]
                output_tensors = to_list(layer(input_data, **kwargs))
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

After applying the suggested fixes and adjustments to the function, it should be able to correctly clone the functional model while correctly tracking input and output tensors, passing the failing test successfully.