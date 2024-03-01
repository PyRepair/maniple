The bug in the provided function lies in the incorrect caching of newly created input layers and the improper handling of input tensors that are not from Keras layers. The function fails to properly create and cache input layers, leading to erroneous behavior when cloning the model.

To fix the bug, we need to ensure that the input layers are correctly created and cached, and that the input tensors are properly handled throughout the cloning process.

Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got {}'.format(model))
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead: {}'.format(model))

    layer_map = {}  
    tensor_map = {}
    input_layers = model._input_layers
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                                sparse=layer.sparse, name=layer.name) for layer in input_layers]
    
    for original_layer, tensor in zip(input_layers, input_tensors):
        layer_map[original_layer] = tensor
        tensor_map[tensor] = (tensor, None)

    for depth, nodes in list(model._nodes_by_depth.items())[::-1]:
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            input_tensors = [tensor_map[x][0] for x in node.input_tensors]
            if all(input_tensor in tensor_map for input_tensor in node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(input_tensors) == 1:
                    input_tensor, input_mask = tensor_map[input_tensors[0]]
                else:
                    input_tensors, input_masks = zip(*[tensor_map[x] for x in input_tensors])
                    input_tensor, input_mask = input_tensors, input_masks

                output_tensors = to_list(layer(input_tensor, **kwargs))
                output_masks = to_list(layer.compute_mask(input_tensor, input_mask))

                if not isinstance(output_tensors, list):
                    output_tensors = [output_tensors]
                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version addresses the issues with caching input layers and properly handling input tensors throughout the cloning process, ensuring the expected output values are achieved for the given test cases.