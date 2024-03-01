### Analysis:
1. The function `_clone_functional_model` is designed to clone a functional model instance by creating new layers and weights instead of sharing existing ones.
2. The error message indicates that the assertion fails at line 166, where the function couldn't compute the output tensor for one of the layers.
3. The expected input values include the model's layers, nodes, inputs, and outputs along with their types. The function should create new layers and input tensors if needed.
4. The bug arises due to the creation of input layers and tensors while missing the actual input tensors in the input list. Additionally, the handling of layer masks is causing issues.
5. To resolve the bug, we should ensure that all input tensors are properly mapped, and mask handling should align with the layer support.

### Bug Fix:
Here is the corrected version of `_clone_functional_model` function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {} 

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape[1:], dtype=layer.dtype, name=layer.name) for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in range(len(model._nodes_by_depth)):
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

            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}  
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    tensor_map.update(zip(reference_output_tensors, [(t, None) for t in output_tensors]))
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                    tensor_map.update(zip(reference_output_tensors, [(t, None) for t in output_tensors]))

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

With this correction, the issue identified in the GitHub report and the failing test case should be resolved.