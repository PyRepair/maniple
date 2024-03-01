### Analysis:
- The `_clone_functional_model` function is supposed to clone a functional model instance by creating new layers (and weights) instead of sharing the existing ones.
- The function goes through the model and builds a new model based on the original model, handling layers, inputs, and outputs.
- The bug seems to be related to the handling of input layers and tensors.

### Potential Error Locations:
1. The creation and handling of input placeholders in the case when input tensors are not provided.
2. Mapping input tensors to their respective layers.
3. Checking the output tensors at the end to ensure they were computed correctly.

### Bug Explanation:
The bug causes the function to fail when trying to clone a model with multiple outputs. It fails to correctly handle the input layers and their respective tensors, leading to incorrect computation of the outputs in the cloned model.

### Strategy for Fixing the Bug:
1. Ensure that the input layers and tensors are correctly mapped and handled during the cloning process.
2. Verify that the computation of output tensors is done accurately and that the model's outputs are correctly computed in the cloned model.

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
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer

    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer

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

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                for x, y in zip(reference_input_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### Summary:
The corrected version of the `_clone_functional_model` function addresses the issue related to cloning a model with multiple outputs by ensuring that input layers and tensors are correctly mapped, and the output tensors are computed accurately. This correction should allow the function to pass the failing test successfully.