### Analysis:
1. The buggy function `_clone_functional_model` is designed to clone a functional `Model` instance by creating new layers and weights instead of sharing the weights of the existing layers.
2. The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs and then attempts to clone it using `keras.models.clone_model`.
3. The failing test raises an AssertionError indicating that the output tensor of one of the layers couldn't be computed, leading to a failure in the cloning process.
4. The GitHub issue highlights a similar problem experienced by a user when using `clone_model` with multi_gpu_model, pointing out an issue with the usage of masks in certain layers like Lambda.

### Potential Error Locations:
1. Handling of input tensors when `input_tensors` is not provided.
2. Creation of new layers during cloning process.
3. Handling of computed data and output tensors during layer calls.

### Bug Cause:
The bug occurs because the function does not handle certain layers, like Lambda, which do not support masks correctly. This leads to an issue with computing the output tensors for these layers, resulting in the failure.

### Fix Strategy:
To fix the bug, we need to modify the logic for handling layers that do not support masks, such as Lambda layers. We can adjust the code to appropriately handle these layers during the cloning process.

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
            # Create placeholder input tensor if input_tensors is not provided
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask
    
    for layer in model.layers:
        if not hasattr(layer, 'compute_mask'):
            # Handle layers that do not support masks, like Lambda
            layer.compute_mask = lambda inputs, mask=None: mask

    for layer in model.layers:
        new_layer = layer.__class__.from_config(layer.get_config())
        layer_map[layer] = new_layer
    
    for node in model._nodes_by_depth[0]:
        for i, x in enumerate(node.input_tensors):
            tensor_map[x] = (input_tensors[i], None)

    for depth in model._nodes_by_depth:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = layer_map[node.outbound_layer]
            input_tensors, output_tensors = node.input_tensors, node.output_tensors
            computed_data = []
            for x in input_tensors:
                computed_data.append(tensor_map[x])
            for x, y, mask in zip(output_tensors, layer(computed_data), layer.compute_mask(computed_data)):
                tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

### After applying the corrections to the `_clone_functional_model` function, the fixed version should resolve the issue and allow the failing test to pass successfully.