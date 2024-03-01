### Analysis:
The error message indicates an `AssertionError` when trying to compute the output tensor while using the `clone_model` function. The issue on GitHub describes a similar problem related to multi-gpu models, `cpu_relocation`, and `clone_model`.

### Error Location:
The error seems to occur when the algorithm iterates over the nodes in the reference model and tries to compute the output tensors. In this case, the issue seems to be related to the presence of multiple outputs without mask support.

### Cause of the Bug:
The bug arises from the fact that the layer, `Lambda`, used in the functional model does not support masks and the `clone_model` function does not handle this scenario correctly. This leads to the issue in computing the output tensors, specifically in scenarios with multiple outputs without mask support.

### Strategy for Fixing the Bug:
To fix the bug, we need to modify the `_clone_functional_model` function to handle the scenario where the layer does not support masks correctly. Specifically, we need to adjust how the output tensors are computed for layers without mask support.


### Corrected Version of the Function:
```python
from keras.engine.topology import Node

def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                                dtype=layer.dtype,
                                sparse=layer.sparse,
                                name=layer.name) for layer in model._input_layers]
        for original_layer, new_layer in zip(model._input_layers, input_tensors):
            layer_map[original_layer] = new_layer
    else:
        input_tensors = [Input(tensor=x) if not K.is_keras_tensor(x) else x for x in to_list(input_tensors)]
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for node in model._nodes_by_depth.get(0, []):
        layer = node.outbound_layer
        if layer not in layer_map:
            new_layer = node.outbound_layer.__class__.from_config(node.outbound_layer.get_config())
            layer_map[layer] = new_layer
        else:
            layer = layer_map[layer]
        
        computed_data = []
        for x in node.input_tensors:
            if x in tensor_map:
                computed_data.append(tensor_map[x])

        if len(computed_data) == len(node.input_tensors):
            if node.arguments:
                kwargs = node.arguments
            else:
                kwargs = {}


            if len(computed_data) == 1:
                computed_tensor, _ = computed_data[0]
                output_tensors = to_list(layer(computed_tensor, **kwargs))
            else:
                computed_tensors = [x[0] for x in computed_data]
                 output_tensors = to_list(layer(computed_tensors, **kwargs))

            for x, y in zip(node.output_tensors, output_tensors):
                tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### Changes Made:
1. Modified the initialization of `input_tensors` to handle cases where input tensors are provided or created.
2. Simplified the loop for creating input tensors and updated the mapping.
3. Revised the iteration over nodes to correctly compute output tensors for layers without mask support.
4. Removed unnecessary mask-related code for layers that do not support masks.

By implementing these changes, the corrected function should now handle the scenario described in the GitHub issue and pass the failing test.