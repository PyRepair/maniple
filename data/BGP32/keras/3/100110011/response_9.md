### Analysis:
1. The buggy function `_clone_functional_model` is designed to clone a functional `Model` instance by creating new layers and weights instead of sharing them. It iterates through the layers of the original model to create new layers and map input and output tensors accordingly.
   
2. The failing test function `test_clone_functional_model_with_multi_outputs` creates a model with multiple input and output layers, then attempts to clone this model using `keras.models.clone_model`. The `AssertionError` is raised in the failing test while trying to clone the model due to an issue in the `_clone_functional_model` function.

3. The error message indicates that the clone operation couldn't compute the output for a specific tensor, leading to the assertion failure.

4. The GitHub issue points out a related problem when using `clone_model` with models having multiple outputs without mask support in certain layers, like `Lambda`.

### Bug Cause:
The bug arises due to the incorrect handling of multiple outputs without mask support in certain layers during the model cloning process. When the original model has multiple output tensors, the cloned model fails to compute the output for one of the tensors, leading to the observed assertion error.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the clone function properly handles multiple output tensors without mask support in certain layers. One approach could involve modifying the logic related to computing output masks for layers with multiple outputs to handle cases where mask support is not provided correctly.

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
            input_layers.append(layer) # Store input layers.
            layer_map[layer] = input_tensor

        for original, cloned in zip(model._input_layers, input_layers):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[x._keras_history[0]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    # Iterate over every node in the reference model, in depth order.
    depth_keys = list(sorted(model._nodes_by_depth.keys(), reverse=True))
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []  
            for x in reference_input_tensors:
                computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                tensor_map.update(zip(reference_output_tensors, output_tensors))

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

After implementing these changes, the corrected version of the `_clone_functional_model` function should be able to clone models with multiple output tensors successfully, resolving the issue encountered in the failing test case and GitHub bug report.