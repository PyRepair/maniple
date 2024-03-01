### Analysis:
- The buggy function `_clone_functional_model` is designed to clone a functional `Model` instance, creating new layers and weights without sharing them from the original model.
- The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs and then tries to clone it using `keras.models.clone_model(model)`.
- The error message indicates that the failing point is at the assertion that checks if the output tensors of the model were computed successfully, and in this case, it fails for the tensor `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`.

### Potential Error Locations:
1. The creation of placeholders for input tensors seems to be incorrect.
2. Handling of input tensors may lead to issues, especially when the functional model has multiple inputs.
3. Cloning layers and handling the mapping between original and cloned layers could be problematic.

### Bug Cause:
After running through the code, the cloning of layers and handling of input tensors weren't correctly managed. In the case where the model has multiple outputs, the function wasn't able to compute the corresponding output tensors due to errors in handling the reference input tensors. This led to the failure of the test.

### Bug Fix Strategy:
1. Correctly generate placeholder input tensors for cases where input tensors are not provided.
2. Ensure proper handling of input tensors to map original input layers to cloned input layers.
3. Carefully clone the layers and maintain the mapping between original and cloned layers correctly.

### Bug Fix and Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            layer_map[layer] = input_tensor._keras_history[0]
    else:
        input_tensors = to_list(input_tensors)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask
        
    for depth_key in sorted(model._nodes_by_depth.keys(), reverse=True):
        for nodes in model._nodes_by_depth[depth_key]:
            layer = nodes.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            computed_data = []

            for x in nodes.input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
            
            if len(computed_data) == len(nodes.input_tensors):
                if nodes.arguments:
                    kwargs = nodes.arguments
                else:
                    kwargs = {}
                
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(nodes.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected version updates the handling of input tensor creation, mapping, and cloning of layers to ensure the successful computation of output tensors in the functional model cloning process.