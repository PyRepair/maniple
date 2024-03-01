### Bug Analysis:
The bug arises from the `_clone_functional_model` function in the `keras/models.py` file. The function is responsible for cloning a functional `Model` instance by creating new layers and weights instead of sharing the existing ones. The bug occurs when the function tries to clone a model that contains multiple outputs with distinct names.

The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs and then attempts to clone it using `keras.models.clone_model`. This triggers an assertion error in the function, indicating that the output tensor could not be computed during the cloning process.

#### Error:
The assertion error is raised at line 166 of `keras/models.py`, indicating that the function failed to compute the output tensor during the cloning process. This error is likely due to the handling of multiple output tensors within the model that causes an issue during the cloning process.

### Bug Fix Strategy:
To fix the bug, we need to update the function logic in `_clone_functional_model` to correctly handle models with multiple outputs. Specifically, we need to adjust the code that processes the output tensors to ensure that all output tensors are correctly computed and mapped during the cloning process.

### Corrected Function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    # Initialize dictionaries to cache created layers and map tensors
    layer_map = {}
    tensor_map = {}

    # Check if input_tensors is provided, otherwise create placeholders
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]

    if not all(K.is_keras_tensor(x) for x in input_tensors):
        input_tensors = [Input(tensor=x) if not K.is_keras_tensor(x) else x for x in input_tensors]

    tensor_map = dict(zip(model.inputs, input_tensors))

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            computed_data = []

            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                output_tensors = to_list(new_layer(computed_data[0], **kwargs)) if len(computed_data) == 1 else to_list(new_layer(computed_data, **kwargs))
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = y

    output_tensors = [tensor_map[x] for x in model.outputs]

    return Model(input_tensors, output_tensors, name=model.name)
```

By updating the `_clone_functional_model` function as shown above, we ensure that the cloning process correctly handles models with multiple outputs. This corrected version should now pass the failing test case by handling the computation of all output tensors during the model cloning process.