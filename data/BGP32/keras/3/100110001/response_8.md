### Analysis:
The buggy function `_clone_functional_model` is responsible for cloning a Keras functional Model instance. The function first checks if the input `model` is an instance of `Model` and not a `Sequential` model. Then it creates placeholders if `input_tensors` are not provided or handles input tensors if they are provided. Next, it iterates over the model nodes and creates new layers for the cloned model.

The failing test `test_clone_functional_model_with_multi_outputs` creates a multi-output model and tries to clone it using `keras.models.clone_model`. The error message indicates that during the cloning process, the output tensor of one of the layers (`swap_layer_1`) was not computed. This suggests an issue in the cloning logic of the `_clone_functional_model` function.

### Bug:
The bug occurs when the model is being cloned, and the output tensors of certain layers are not properly computed and stored in the `tensor_map`. This leads to missing output tensors when building the new model.

### Fix:
The issue arises from how the output tensors of each layer are handled during the cloning process. To fix this, we need to ensure that all the input tensors required for each layer operation are correctly mapped and computed based on the input tensor dependencies.

### Corrected Version:
Below is the corrected version of the `_clone_functional_model` function that addresses the bug:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.input_shape, dtype=layer.input_dtype, name=layer.name) 
                         for layer in model._input_layers]

    for orig_input, input_tensor in zip(model._input_layers, input_tensors):
        layer_map[orig_input] = input_tensor

    for depth in range(len(model._nodes_by_depth)):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            inbound_layers = [layer_map[in_node.outbound_layer] for in_node in node.inbound_nodes]
            kwargs = node.arguments
        
            if len(inbound_layers) == 1:
                layer = node.outbound_layer.__class__.from_config(node.outbound_layer.get_config())
                output_tensor = layer(inbound_layers[0], **kwargs)
                layer_map[node.outbound_layer] = layer
                tensor_map[node.output_tensors[0]] = (output_tensor, None)
            else:
                input_tensors = [tensor_map[in_node.outbound_layer][0] for in_node in node.inbound_nodes]
                layer = node.outbound_layer.__class__.from_config(node.outbound_layer.get_config())
                output_tensor = layer(input_tensors, **kwargs)
                layer_map[node.outbound_layer] = layer
                tensor_map[node.output_tensors[0]] = (output_tensor, None)
    
    output_tensors = [tensor_map[orig_out_tensor][0] for orig_out_tensor in model.outputs]
    return Model(inputs=input_tensors, outputs=output_tensors, name=model.name)
```

By updating the logic to properly compute and store the output tensors of each layer during the cloning process, this corrected version should pass the failing test case.