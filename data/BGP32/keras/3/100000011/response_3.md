### Analysis:
The bug in the `_clone_functional_model` function is related to the issue raised on GitHub titled `'Could not compute output Tensor' error when I‘m using clone_model()`. The issue is caused due to incorrect handling of output masks for layers that do not support masks, specifically in the case of using `Lambda` layer which doesn't support masks.

### Potential Error Locations:
1. Handling of output masks generation for layers without mask support.
2. Incorrect assumption of output masks being present in the `output_masks` list.

### Cause of the Bug:
The bug occurs because the function tries to generate output masks for layers that do not support masks, such as the `Lambda` layer in the provided GitHub issue script. Due to this, the `output_masks` list will always be `[None]` instead of the expected `[None, None]`, resulting in an assertion error when trying to compute the output tensor.

### Strategy for Fixing the Bug:
To fix this bug, we need to handle the scenario where a layer does not support masks gracefully, by not trying to compute masks for such layers. Instead, we can directly set the output masks to `None` for those layers.

### Corrected Version of the Function:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.input.shape.as_list(), dtype=layer.input.dtype, name=layer.name) for layer in model.input_layers]
    else:
        input_tensors = [Input(tensor=x, name='input_wrapper_for_' + model_input_layer.name) if not K.is_keras_tensor(x) else x for x, model_input_layer in zip(to_list(input_tensors), model._input_layers)]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth, nodes in model._nodes_by_depth.items():
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

                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

In this corrected version:
- We handle the scenario where a layer does not support masks by setting the output masks to `None`.
- We simplify the code logic for input tensor creation and model cloning.

This corrected version should resolve the issue reported on GitHub and allow the functional model cloning to work correctly even with layers that do not support masks.