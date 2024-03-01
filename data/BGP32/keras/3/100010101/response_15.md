### Bug analysis:
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and new weights instead of sharing existing ones. However, there are several issues in the current implementation:
1. The check to verify if the input `model` is an instance of `Model` is incorrect. It's raising an error with the wrong format and is redundant since the following condition already checks if it's an instance of `Sequential`. 
2. The creation of `input_tensors` and `input_layers` is flawed, resulting in an empty `input_layers` list and missing input tensors.
3. There is an issue in computing the output tensors, as revealed by the failing test.

### Bug fix strategy:
1. Correct the error message format for the type check on `model` to follow a proper format.
2. Fix the creation process of `input_tensors` and `input_layers` to ensure the correct assignment of input tensors.
3. Address the issue in computing the output tensors to stabilize the function's behavior.

### Corrected function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, not {}'.format(type(model)))
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, not a `Sequential` instance')

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    else:
        # Ensure all input tensors are from a Keras layer
        input_tensors = to_list(input_tensors)
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterate over every node in the reference model, in depth order
    depth_keys = sorted(model._nodes_by_depth.keys(), reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer
            layer = node.outbound_layer

            # Get or create layer
            if layer not in layer_map:
                # Clone layer
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                # Reuse previously cloned layer
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    # Check that we computed the model outputs and instantiate a new model
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By applying the corrections outlined above in recognizing the correct type of `model`, handling input tensor creation, and refining the output tensor computation section, the fixed function should pass the failing test case and work correctly across different scenarios.