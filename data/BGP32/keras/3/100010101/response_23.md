### Analysis
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance with new layers and weights. The error message indicates that the function fails during the test case when trying to compute the output tensors. This failure suggests that the cloning process encounters an issue, possibly related to incorrect mapping of input and output tensors.

### Bug in the code
The bug is likely related to the mapping of input and output tensors during the cloning process. The tensors are expected to be correctly mapped in the `tensor_map` dictionary, but something goes wrong resulting in the failure to compute the output tensor for the model during the test.

Initially, there seems to be an issue with the creation of `input_layers` and `input_tensors`, as they are empty lists but are intended to store new input layers and input tensors. Additionally, the handling of the layers and tensors in the model during the iteration through nodes might be causing the incorrect mapping.

### Proposed Fix
To fix the bug:
1. Ensure that new input layers and input tensors are correctly added to the `input_layers` and `input_tensors` lists when `input_tensors` is initially `None`.
2. Update the handling of nodes and their corresponding layers and tensors to properly map the inputs and outputs in the `tensor_map` dictionary.

### Corrected Code
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        # Create placeholders to build the model on top of
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            input_layers.append(layer)
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                # Call layer
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor = computed_data[0][0]
                    computed_tensors = [computed_tensor]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(new_layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    # Check if model outputs can be computed
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
``` 

This corrected version should address the issues with the original function and pass the failing test case.