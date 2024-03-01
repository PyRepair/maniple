### Analysis:
The error message indicates that the function `_clone_functional_model` failed to compute the output tensors of the model, specifically when given a model with multiple outputs. The error occurred when asserting that each output tensor is present in the `tensor_map`.

### Bug:
The bug lies in the mapping of output tensors to their corresponding tensors in the `tensor_map`. When the model has multiple outputs, the function fails to properly track and update the output tensors in the `tensor_map`.

### Fix Strategy:
1. Ensure that for each output tensor in the model, its corresponding tensor is correctly computed and stored in the `tensor_map`.
2. Update the logic to handle multiple outputs properly.

### Corrected Version:
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
            input_layers.append(layer)  # Store input layer for later mapping
            layer_map[layer] = input_tensor

    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor  # Replace non-Keras tensor with wrapper
                layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            computed_data = []
            for x in node.input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    computed_masks = [x[1] for x in computed_data]
                
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                computed_tensors = to_list(computed_tensors) if isinstance(computed_tensors, list) else [computed_tensors]
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks)) if hasattr(layer, 'compute_mask') and callable(layer.compute_mask) else [None] * len(output_tensors)
                
                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### Explanation of Changes:
1. Added a check to ensure `input_layers` are stored for mapping in the case of missing `input_tensors`.
2. Fixed the computation of `output_tensors` to consider proper handling of multiple outputs.
3. Updated the logic to correctly compute and store output tensors in the `tensor_map`.
4. Handled the case where `compute_mask()` might not be present in the layer.
5. Simplified the retrieval of output tensors for the final model creation.

Now, the corrected version should address the bug and allow the clone_model function to work correctly, passing the failing test.