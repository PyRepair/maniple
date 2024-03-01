### Bug Analysis:
The bug in the `_clone_functional_model` function arises due to incorrect handling of the input tensors in the function when trying to clone a model with multiple outputs. The function fails to properly create placeholders for input tensors and fails to correctly map the corresponding output tensors.

- The function expects input tensors to be provided but fails to create appropriate input placeholders if not provided.
- The tensor_map does not correctly handle the mapping of tensors, leading to missing output tensors when creating the new model.

### Bug Fix Strategy:
To fix the bug in the `_clone_functional_model` function:
1. Ensure that input placeholders are correctly created if input_tensors are not provided.
2. Fix the mapping of input and output tensors in the tensor_map to ensure that all output tensors are computed.
3. Update the logic for handling input_tensors that are not Keras tensors.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    else:
        # Make sure that all input tensors come from a Keras layer
        input_tensors = to_list(input_tensors)
        input_layers = [layer for layer in model._input_layers]
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + model._input_layers[i].name)
                input_tensors[i] = input_tensor
                input_layers[i] = x._keras_history[0]
        layer_map = dict(zip(model._input_layers, input_layers))

    tensor_map = dict(zip(model.inputs, input_tensors))

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = [(tensor_map[x], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                computed_tensors, computed_masks = [], []
                for computed_tensor, computed_mask in computed_data:
                    computed_tensors.append(computed_tensor)
                    computed_masks.append(computed_mask)

                if has_arg(layer.call, 'mask'):
                    if len(computed_data) == 1:
                        kwargs['mask'] = computed_masks[0]
                    else:
                        kwargs['mask'] = computed_masks
                
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By fixing the input tensor handling and mapping of input and output tensors, the corrected function should now properly clone a functional model with multiple outputs.