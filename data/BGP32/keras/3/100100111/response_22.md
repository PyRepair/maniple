### Analysis:
1. The buggy function `_clone_functional_model` is responsible for creating a clone of a functional `Model` instance with new layers and weights instead of sharing existing ones.
2. The function loops through the nodes of the model, creates new layers, and builds the clone model based on the newly created layers and input tensors.
3. The failing test `test_clone_functional_model_with_multi_outputs` creates a functional model with multiple outputs, then attempts to clone the model and compares the predictions between the original and cloned models.
4. The failing test fails due to issues with cloned layers and input tensors not being correctly mapped.
5. The GitHub issue references a similar problem related to `clone_model` failing with multiple outputs and not handling masks correctly for layers like Lambda.
   
### Bug:
The bug arises from `output_masks` always being set to `[None]` when it is expected to be `[None, None]`. This leads to issues in computing the output tensors correctly, causing the failing test to fail.

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the `output_masks` are correctly set to `[None, None]` when needed. Additionally, handling multiple outputs and layers without mask support needs to be addressed.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            newly_created_input_layer = input_tensor._keras_history[0]
            layer_map[layer] = newly_created_input_layer

    for _original, _cloned in zip(model._input_layers, input_tensors):
        layer_map[_original] = _cloned

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterated over every node in the reference model, in depth order.
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            # Recover the corresponding layer.
            layer = node.outbound_layer

            # Get or create layer.
            if layer not in layer_map:
                # Clone layer.
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                # Reuse previously cloned layer.
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            # Gather inputs to call the new layer.
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []  # List of tuples (input, mask).
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                # Call layer.
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                computed_tensors = [x[0] for x in computed_data]
                kwargs['mask'] = [x[1] for x in computed_data if x[1] is not None]

                output_tensors = to_list(layer(computed_tensors, **kwargs))

                tensor_map.update({x: (y, mask) for x, y, mask in zip(reference_output_tensors, output_tensors, kwargs['mask'])})

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By updating how `output_masks` are handled and ensuring proper mapping of input tensors and layers, the corrected function should now address the issues causing the failing test to fail and align with the expected input/output values while addressing the bug reported in the GitHub issue.