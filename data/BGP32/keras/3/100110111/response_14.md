### Analysis:
1. **Buggy function's behavior**: The `_clone_functional_model` function is intended to clone a functional `Model` instance with new layers and weights instead of sharing existing ones.
   
2. **Error location**: The error seems to originate from the function's inability to properly compute the output tensors due to the absence of masks for the layers involved.

3. **Cause of the bug**: The failing test `test_clone_functional_model_with_multi_outputs` tries to clone a model with multiple outputs, where one of the layers involved (`Lambda`) doesn't support masks. This results in the assertion failure when attempting to compute tensors without masks.

4. **Strategy for fixing the bug**:
   - Ensure that the code handles layers without mask support correctly, considering the absence of masks in such cases.
   - Use conditional checks to verify if the layer supports masks before trying to compute them.
   - Modify the code to work seamlessly with layers that do not require masks.

### Corrected Function:
```python
from keras.layers import Input

def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    
    if not input_tensors:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                                dtype=layer.dtype,
                                sparse=layer.sparse,
                                name=layer.name) for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for node in model._nodes_by_depth[0]:
        layer = node.outbound_layer
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer
            layer = new_layer
        else:
            layer = layer_map[layer]
            if isinstance(layer, InputLayer):
                continue

        computed_data = [tensor_map[x] for x in node.input_tensors if x in tensor_map]

        if len(computed_data) == len(node.input_tensors):
            kwargs = node.arguments if node.arguments else {}
            if len(computed_data) == 1:
                computed_tensor, _ = computed_data[0]
                output_tensors = to_list(layer(computed_tensor, **kwargs))
            else:
                computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))

            for x, y in zip(node.output_tensors, output_tensors):
                tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

Now, the corrected function should handle the scenario where a layer does not support masks properly, ensuring smooth computation of output tensors.