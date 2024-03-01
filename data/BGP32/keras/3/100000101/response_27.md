The bug in the provided function `_clone_functional_model` seems to originate from the incorrect implementation of handling the input tensors and corresponding layers when creating a clone of a functional `Model`. 

The buggy function fails to correctly handle the mapping of input tensors to corresponding layers and cache the created layers effectively. This results in the incorrect computation of model outputs and, eventually, the creation of the cloned model.

To fix the bug, we need to ensure that the input tensors are correctly mapped to the corresponding layers, and the cache of created layers is properly maintained throughout the function execution.

Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape[1:], dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    else:
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model.input_names[i]
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in range(len(model._nodes_by_depth)):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = [], []
                for tensor, mask in computed_data:
                    computed_tensors.append(tensor)
                    computed_masks.append(mask)

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                if callable(getattr(layer, 'compute_mask', None)):
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                else:
                    output_masks = [None] * len(output_tensors)

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version ensures proper mapping of input tensors, maintains the cache of created layers, and correctly computes the model outputs. It should now satisfy the expected input/output values provided in the test cases.