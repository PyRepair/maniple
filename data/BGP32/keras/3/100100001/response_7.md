The bug in the `_clone_functional_model` function is related to the handling of the inputs and outputs of the model during the cloning process. Specifically, when a layer has multiple inputs, the function fails to correctly handle the computed data and output tensors.

To fix the bug, we need to ensure that the function correctly handles multiple inputs and outputs of layers during the cloning process.

Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_tensors = [Input(batch_shape=layer.output_shape[1:]) for layer in model.layers if getattr(layer, '_keras_history', None)]
    
    for original_layer, new_layer in zip(model.layers, input_tensors):
        layer_map[original_layer._keras_history[0]] = new_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for layer in model.layers:
        refer_input_tensors = [tensor_map[x][0] for x in layer._inbound_nodes[0].input_tensors]
        computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in refer_input_tensors if x in tensor_map]
        
        computed_tensors, computed_masks = zip(*computed_data)
        
        kwargs = layer._inbound_nodes[0].arguments if layer._inbound_nodes and layer._inbound_nodes[0].arguments else {}

        out_tensors = layer.compute_output_shape(layer.input_shape).as_list()
        computed_data = Input(shape=out_tensors[1:])(computed_tensors[0])

        tensor_map[layer._keras_history[0]] = (computed_data, None)

    output_tensors = []
    
    for output in model.outputs:
        assert output in tensor_map, 'Could not compute output ' + str(output)
        computed_tensor, _ = tensor_map[output]
        output_tensors.append(computed_tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)

```

This corrected version makes sure to properly handle multiple inputs and outputs of layers during the cloning process. By using information from the layers' history and input nodes, the function correctly creates new layers and computes output tensors. This should address the bug and enable the function to pass the failing test.