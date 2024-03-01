## Strategy for fixing the bug
The bug occurs because the function `_clone_functional_model` incorrectly expects the input model to be an instance of `Model` but not of `Sequential` type. This leads to the check raising an error even with a valid functional model. 

To fix the bug:
1. Remove the check for `Sequential` type since functional models can be of different types.
2. Modify the conditions and flow of the function to handle any type of functional model correctly.
3. Ensure that the creation and mapping of layers and tensors are done accurately without skipping important steps.

## The corrected version of the function

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    # Retrieve existing input layers or create new ones
    input_layers = []
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]

    for orig_layer, input_tensor in zip(model._input_layers, input_tensors):
        layer_map[orig_layer] = input_tensor

    for orig_tensor, input_tensor in zip(model.inputs, input_tensors):
        tensor_map[orig_tensor] = (input_tensor, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)

    for depth in depth_keys:
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            
            # Get or create the layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            # Gather inputs to call the new layer
            input_tensors = [tensor_map[x][0] for x in node.input_tensors]

            # Call the layer and update tensor_map
            kwargs = {} if not node.arguments else node.arguments
            output_tensors = to_list(layer(*input_tensors, **kwargs))

            for orig_tensor, output_tensor in zip(node.output_tensors, output_tensors):
                tensor_map[orig_tensor] = (output_tensor, None)

    # Check that all model outputs have been computed
    output_tensors = [tensor_map[x][0] for x in model.outputs]

    # Return the new cloned model
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version should pass the failing test and provide the expected outputs for the given scenarios.