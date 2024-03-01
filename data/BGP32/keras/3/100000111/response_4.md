### Analysis:
1. The bug occurs when using `clone_model` with a multi-layer model that includes layers without mask support, like the Lambda layer in the GitHub issue.
2. The bug is likely caused by not handling cases where layers do not support masks correctly, leading to issues in computing output tensors and masks.
3. The critical point of failure seems to be related to handling output masks from layers that do not support masks, leading to the `Could not compute output Tensor` error.
4. To fix the bug, we need to adjust how the code deals with layers lacking mask support during the model cloning process.

### Bug Fix Strategy:
1. Modify the code to handle cases where layers do not support masks correctly by omitting mask-related operations for these layers to prevent the `Could not compute output Tensor` error.
2. Ensure that the model cloning process considers the specific case of layers without mask support, like the Lambda layer in the GitHub issue, to address the root cause of the bug.

### Bug Fix - Corrected Version:
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
                layer_map[x._keras_history[0]] = input_tensor
        input_tensors = to_list(input_tensors)
    
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

            computed_data = []  
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            computed_tensors, computed_masks = [], []
            for x, mask in computed_data:
                computed_tensors.append(x)
                computed_masks.append(mask)

            output_tensors = to_list(layer(computed_tensors))
            if layer.supports_masking:
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

            for i, (x, mask) in enumerate(zip(node.output_tensors, output_tensors)):
                tensor_map[x] = (mask, output_masks[i] if layer.supports_masking else None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

By modifying the `clone_functional_model`, specifically how it handles layers without mask support, the corrected version aims to resolve the `Could not compute output Tensor` error when using `clone_model`.