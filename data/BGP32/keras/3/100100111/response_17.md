## Analysis
The buggy function `_clone_functional_model` is designed to clone a functional Keras `Model` instance. The main issue seems to be that when a model with multiple outputs that do not support masks is cloned, the function fails to compute the output correctly. This bug is related to an issue posted on GitHub about the `clone_model` function not working properly when used in a specific scenario.

### Error Locations Identified:
1. The function does not handle the case where a layer does not support masks correctly, leading to the failure to compute outputs.
2. The `output_masks` creation lacks correct handling for layers without mask support.
3. Issues with input tensors and the overall mapping process.

### Cause of the Bug:
In the failing test case, the model being cloned has a layer that does not support masks (`Lambda` layer). When this layer is encountered during the cloning process, the function fails to correctly compute the output tensors and masks, leading to an assertion error during prediction due to incorrect output computation. This bug is related to the behavior explained in the GitHub issue, where the mask computation in layers like `Lambda` may not work as expected.

### Bug Fix Strategy:
1. Modify the computation of `output_tensors` and `output_masks` to account for layers without mask support.
2. Ensure proper handling of layers that do not support masks during the cloning process.
3. Verify and update the input tensors and mapping logic to prevent any issues related to layer mappings.

## Corrected Version
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    # Cache for created layers.
    layer_map = {}
    
    # map {reference_tensor: (corresponding_tensor, mask)}
    tensor_map = {}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
        
        for orig, cloned in zip(model._input_layers, input_tensors):
            layer_map[orig] = cloned
    else:
        input_tensors = [Input(tensor=x) if not K.is_keras_tensor(x) else x for x in to_list(input_tensors)]
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                orig_input_layer = x._keras_history[0]
                layer_map[orig_input_layer] = input_tensor._keras_history[0]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    # Iterate over nodes in depth order
    depth_keys = sorted(model._nodes_by_depth.keys(), reverse=True)
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
                
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = [None] * len(output_tensors)

                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
``` 

By making these corrections, the function should now properly handle layers without mask support during the cloning process, resolving the issue encountered in the failing test and matching the expected behavior described in the GitHub issue.