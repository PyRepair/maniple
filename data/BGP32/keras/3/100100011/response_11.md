### Analysis:
The provided buggy function `_clone_functional_model` is intended to clone a functional `Model` instance in Keras. The function iterates over the model's nodes and creates new layers based on the original ones. The bug arises when dealing with multiple outputs from a layer that does not support masks. The failing test `test_clone_functional_model_with_multi_outputs` is trying to clone a model with multiple outputs where one of the intermediate layers does not support masks, leading to the bug.

### Bug Cause:
The bug occurs when `output_masks = to_list(layer.compute_mask(...))` always returns `None` due to the inability to compute masks for certain layers like `Lambda`. This leads to missing masks being passed to subsequent layers, causing issues in the model cloning process.

### Bug Fix Strategy:
To fix the bug:
1. Adjust the logic to handle layers that do not support masks, ensuring that appropriate masks are passed or handled properly.
2. Check for `None` values in the mask computation to prevent issues with missing masks for subsequent layers.

### Bug-free version of the function:
Here's the corrected version of the `_clone_functional_model` function:

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
            input_tensor = Input(batch_shape=layer.input_shape)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    
    # Handle different cases for input_tensors
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + model._input_layers[i].name)
                input_tensors[i] = input_tensor
                layer_map[x._keras_history[0]] = input_tensor

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
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                if len(computed_data) == 1:
                    computed_tensors = computed_tensors[0]
                output_tensors = layer(computed_tensors, **kwargs)
                for x, y in zip(reference_output_tensors, to_list(output_tensors)):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

After applying the fixes, the corrected function should successfully clone functional models, including cases with multiple outputs and layers that do not support masks.