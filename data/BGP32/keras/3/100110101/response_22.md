### Bug Analysis
- The buggy function `_clone_functional_model` is supposed to clone a functional model instance by creating new layers and new weights instead of sharing the weights of existing layers.
- The function first checks if the input `model` is an instance of `Model` and if it is not an instance of `Sequential`. If either of these conditions is not met, it raises a `ValueError`.
- The function then creates placeholders for input tensors if `input_tensors` is not provided explicitly.
- It iterates through the nodes of the model and tries to clone layers and build a new model based on the input tensors and output tensors of the model.

### Bug Explanation
- In the failing test, the function `test_clone_functional_model_with_multi_outputs` creates a model with non-trivial layer connections involving Lambda and custom layers.
- The model is then passed to `keras.models.clone_model`, which internally calls `_clone_functional_model`.
- The assertion fails during the execution of `_clone_functional_model` because the function fails to correctly handle the cloning of layers and does not successfully compute the output tensors of the model.

### Bug Fix Strategy
1. Ensure that the layer cloning mechanism correctly handles the Lambda layers and the custom layers like `SwapLayer` in the failing test.
2. Check the logic related to iterating through nodes, cloning layers, and computing output tensors to ensure all parts are functioning as expected.

### Corrected Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  
    tensor_map = {}  

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]

    for original, cloned in zip(model._input_layers, input_tensors):
        layer_map[original] = cloned

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for x in model.outputs:
        tensor_map[x] = (x, None)

    for depth in model._nodes_by_depth:
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            reference_input_tensors = node.input_tensors
            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors]

            kwargs = node.arguments if node.arguments else {}
            output_tensors = to_list(layer(computed_data, **kwargs))

            for x, y in zip(node.output_tensors, output_tensors):
                tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

After fixing the `_clone_functional_model` function as shown above, the corrected version should be able to correctly handle the input model with multiple outputs as in the failing test and successfully clone the functional model.