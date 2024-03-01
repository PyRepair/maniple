### Analysis:
1. The buggy function `_clone_functional_model` is attempting to clone a functional model instance by creating new layers and new weights instead of sharing the existing ones.
2. The failed test case `test_clone_functional_model_with_multi_outputs` is trying to clone a functional model with multiple outputs. It constructs layers and models to verify the cloning process.
3. The error message indicates that the issue arises during the computation of output tensors in the cloning process, resulting in an assertion error.
4. The GitHub issue provides a similar scenario where the use of `clone_model` function fails due to problems in handling output masks.
   
### Bug Cause:
The bug arises from a discrepancy in handling output masks for layers that do not support masks. In specific cases, the output masks are always None, leading to an assertion error when trying to compute the output tensors.

### Strategy for Fixing the Bug:
To fix this bug, we need to address how output masks are handled, especially for layers that do not have mask support. Conditional checks and modifications in the code related to masks should be adjusted to ensure the smooth computation of output tensors during model cloning.

### Updated Fixed Function:
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
        input_tensors = [Input(batch_shape=layer.input_shape,
                                dtype=layer.dtype,
                                sparse=layer.sparse,
                                name=layer.name) 
                         for layer in model._input_layers]
    else:
        input_tensors = [Input(tensor=x) if not K.is_keras_tensor(x) else x
                         for x in to_list(input_tensors)]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask
    
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]
                if isinstance(new_layer, InputLayer):
                    continue

            computed_data = []
            for x in node.input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(node.input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

### Conclusion:
The updated function now handles the computation of output tensors and masks for layers that may not support masks. By adjusting the logic and checks related to masks, the cloning process of functional models with multiple outputs should work correctly and address the assertion error observed in the failing test.