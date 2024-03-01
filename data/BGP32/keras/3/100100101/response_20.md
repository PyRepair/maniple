The bug in the `_clone_functional_model` function could be related to the incorrect handling of input tensors, layer mappings, and tensor mappings during the cloning process. To fix the bug, we need to adjust how input layers and tensors are created and mapped, ensure that all tensors are properly taken into account, and correctly propagate the tensors through the model.

Here is a corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    # Create placeholders if input_tensors is not provided
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, 
                               dtype=layer.dtype, 
                               sparse=layer.sparse, 
                               name=layer.name) for layer in model._input_layers]
    
    layer_map = {}
    tensor_map = {}
    
    # Map input_layers to created input_tensors
    for orig_input, new_input in zip(model._input_layers, input_tensors):
        layer_map[orig_input] = new_input
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterate over the nodes of the model and clone layers
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]
            
            computed_data = [tensor_map[t] for t in node.input_tensors if t in tensor_map]

            if len(computed_data) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                new_outputs = to_list(new_layer([t[0] for t in computed_data], **kwargs))
                new_masks = to_list(new_layer.compute_mask([t[0] for t in computed_data], [t[1] for t in computed_data]))

                for out_t, new_out, mask in zip(node.output_tensors, new_outputs, new_masks):
                    tensor_map[out_t] = (new_out, mask)

    output_tensors = [tensor_map[out_t][0] for out_t in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version ensures that input tensors are correctly created and mapped to the original model's input layers. It also correctly propagates tensors and masks through the model, ensuring that all output tensors are computed and returned as expected.

With this correction, the `test_clone_functional_model_with_multi_outputs` should pass successfully, and the expected values and types mentioned in the test cases should align with the corrected function's outputs.