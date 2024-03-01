### Bug Explanation
The bug in the `_clone_functional_model` function arises from incorrectly handling the input tensors when cloning a functional model. When creating a new model by cloning an existing one, the function fails to properly track the input tensors and their associated layers. This results in an assertion error when computing the model outputs, indicating that an output tensor is missing.

### Bug Location
The issue lies in the conditional block that handles the case when `input_tensors` is None or if it contains non-Keras tensors. The function fails to correctly assign input_tensors to newly created input layers or existing layers, leading to inconsistencies later in the function.

### Bug Fix Strategy
To fix the bug, we need to ensure that the input tensors passed to the model are correctly mapped to the corresponding layers. Specifically, when creating or reusing input layers, the function needs to accurately update the `layer_map` and `tensor_map` dictionaries to maintain consistency throughout the cloning process.

### Corrected Function
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = y

    for depth in range(max(model._nodes_by_depth.keys()), -1, -1):
        nodes = model._nodes_by_depth.get(depth, [])
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = [(tensor_map[x], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
                    if has_arg(new_layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_mask
                    output_tensors = to_list(new_layer(computed_tensor, **kwargs))
                else:
                    computed_tensors, computed_masks = zip(*computed_data)
                    if has_arg(new_layer.call, 'mask') and 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                    output_tensors = to_list(new_layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = y

    output_tensors = [tensor_map[x] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version ensures correct mapping of input tensors to corresponding layers and resolves the issue of missing output tensors during the cloning process.