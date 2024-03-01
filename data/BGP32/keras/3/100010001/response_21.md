### Analyzing the Buggy Function and Error Message:

The buggy function `_clone_functional_model` is designed to clone a functional `Model` instance, creating new layers with new weights instead of sharing the weights of existing layers. The error message from the failing test indicates that during the cloning process, the function was not able to compute the output for a specific tensor (identified as 'swap_layer_1/Identity:0' in this case).

### Error Location and Cause:
The error occurs when the function tries to compute the outputs for the layers in the input model and update the `tensor_map`. The issue lies in the lines where the function iterates over the `model.outputs` and checks if each output tensor is present in the `tensor_map`. In this case, the specific output tensor 'swap_layer_1/Identity:0' is missing from the `tensor_map`, causing the error.

### Bug Fix Strategy:
To fix the bug, we need to ensure that all output tensors from the input model are correctly computed and added to the `tensor_map`. This involves properly mapping the input tensors to their corresponding newly computed tensors during the layer cloning process.

### Corrected Version of the Function:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  
    if input_tensors is None:
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer
    else:
        input_tensors = to_list(input_tensors)
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
                output_tensors = to_list(layer([x[0] for x in computed_data], **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### Changes Made:
1. Rewritten the input tensor creation logic in the function.
2. Step through the depth of nodes in reverse order to ensure dependencies are maintained.
3. Properly update the `tensor_map` with the computed tensors for each node.
4. Ensure that all output tensors are correctly computed and added to the `output_tensors` list.

By making these changes, the corrected version of the function should now pass the failing test without raising any `AssertionError`.