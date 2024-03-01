### Analyzing the buggy function and failing test

1. The buggy function `_clone_functional_model` is designed to clone a functional Keras `Model`. It fails to properly handle the case where the input model is a `Sequential` model rather than a functional model.
2. The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple inputs and multiple outputs, including a custom layer that does not support masks. 
3. The error message indicates that the failure occurs at line 166 of `keras/models.py` where it asserts that the model outputs were computed. The error is due to the inability to compute the output of a layer that does not support masks.
4. The GitHub issue also highlights a similar error when using `clone_model` with `multi_gpu_model` in a specific scenario.

### Proposed Fix Strategy
1. Update the `_clone_functional_model` function to handle input models that are instances of `Sequential` properly and exclude inappropriate layers that don't support masks.
2. Modify the logic to avoid attempting to compute masks for layers that don't support them.

### Corrected Version of the Function

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
        
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(tensor_shape=layer._keras_shape) for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            # Recover the corresponding layer
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]

            if isinstance(layer, Lambda):
                # Skip Lambda layers
                continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.inbound_layer_args
                computed_tensors = [x[0] for x in computed_data]

                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                else:
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By skipping the Lambda layers in the cloning process and handling the model layers that don't support masks properly, the corrected function should resolve the failure in the provided test case.