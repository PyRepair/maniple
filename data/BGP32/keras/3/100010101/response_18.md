## Bug Analysis
- The function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers with new weights instead of sharing existing weights.
- The bug arises from improperly checking the type of the input `model` argument and raising a `ValueError` based on that incorrect check.
- The error message shows an `AssertionError` occurring at line 166. The message indicates that the output tensor of a layer is not found in the `tensor_map`.
- The code fails to correctly map the input tensors of the model to the corresponding tensors in the `tensor_map` during the cloning process, leading to the error.

## Bug Fix Strategy
- The bug can be fixed by ensuring that the input model is checked for the correct type before proceeding with the cloning process.
- Additionally, the `tensor_map` should be properly updated during the iteration over the nodes in the model to ensure all tensors are correctly accounted for.
- Correctly handling the creation of new input layers, mapping input tensors, and ensuring that all output tensors are included in the `tensor_map` will resolve the issue.

## Bug Fix and Updated Function
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got {}'.format(type(model)))

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
                         for layer in model._input_layers]
    else:
        if not all(K.is_keras_tensor(x) for x in input_tensors):
            input_tensors = [Input(tensor=x, name='input_wrapper_for_' + model._input_layers[i].name)
                             if not K.is_keras_tensor(x) else x
                             for i, x in enumerate(input_tensors)]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                computed_tensors = to_list(computed_tensors)
                tensor_map.update({x: (y, mask) for x, y, mask in zip(reference_output_tensors, output_tensors, computed_masks)})

    output_tensors = [tensor_map[x][0] for x in model.outputs]

    return Model(input_tensors, output_tensors, name=model.name)
```

By properly updating the `tensor_map` and ensuring the correct type check for the input model, the function should now correctly clone the functional `Model` instances without any errors.