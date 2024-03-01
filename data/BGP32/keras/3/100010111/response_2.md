### Bug Analysis:
The bug occurs when the `_clone_functional_model` function is called to clone a functional `Model` instance. The bug prevents the correct cloning of the model, leading to an assertion error when trying to compute the model outputs due to issues related to the cloning process.

1. The function fails to properly handle the case where a layer does not support masking, leading to incorrect behavior when trying to compute the output masks.
2. When iterating over the nodes in the model, the function does not correctly handle the case where a layer has multiple outputs.
  
### Bug Fix Strategy:
To fix the bug, the function needs to be updated to handle the scenario where layers have multiple outputs and to handle cases where a layer does not support masking properly.

### Corrected Function:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got {}'.format(model))
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead: {}'.format(model))

    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_tensors = [Input(shape=layer.batch_input_shape[1:]) for layer in model._input_layers]
    else:
        input_tensors = to_list(input_tensors)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]
            
            reference_input_tensors = node.input_tensors
            computed_data = [tensor_map[x] for x in reference_input_tensors if x in tensor_map]
            
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                kwargs['mask'] = [m for t, m in computed_data if m is not None]
                
                computed_tensors = [t for t, _ in computed_data]
                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                for x, y, mask in zip(node.output_tensors, output_tensors, kwargs.get('mask', [None]*len(output_tensors))):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version of the function addresses the issues related to handling multiple outputs of layers and proper masking support while cloning the model. The function should now be able to correctly clone a functional model without encountering the assertion error.