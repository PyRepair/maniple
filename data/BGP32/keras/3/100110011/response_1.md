### Analysis:
1. The buggy function `_clone_functional_model` is used to clone a functional `Model` instance. It creates new layers and new weights instead of sharing existing ones.
2. The error message indicates that the assertion `assert x in tensor_map, 'Could not compute output ' + str(x)` fails. This means that the output tensor is not computed correctly during the model cloning process.
3. The GitHub issue also points out a similar issue related to multi-output layers without mask support causing an error with `clone_model`.
   
### Error Cause:
The error occurs because the function is not handling multi-output layers correctly, especially when there is no mask support for certain layers like `Lambda`. The issue arises during the computation of output tensors and masks for these layers.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the function to properly handle multi-output layers without mask support. This can be achieved by checking for mask support for each layer and updating the computation of output tensors accordingly.

### Corrected Version of the Function:
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
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        modified_input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                modified_input_tensors.append(input_tensor)
                layer_map[x] = input_tensor
            else:
                modified_input_tensors.append(x)
        input_tensors = modified_input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in range(len(model._nodes_by_depth) - 1, -1, -1):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]
            if isinstance(new_layer, InputLayer):
                continue
            
            computed_data = []
            for x in node.input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                
                if has_arg(new_layer.call, 'mask') and any(x[1] is not None for x in computed_data):
                    kwargs['mask'] = [x[1] for x in computed_data]

                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                # Update tensor_map
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By updating the function to handle multi-output layers without mask support properly, we can resolve the issue with the failing test case and address the problem reported in the GitHub issue.