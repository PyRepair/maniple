### Analysis:
The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones. The function iterates over the nodes in the model to recreate the layers and build a new model based on the input and output tensors.

The issue lies in the incorrect handling of `input_layers` and `input_tensors` when the `input_tensors` parameter is provided. The input layers are not correctly created, leading to a mismatch and resulting in errors in reproducing the model's behavior.

### Bug Explanation:
When `input_tensors` are provided in the failing test, the function fails to correctly handle the creation of input layers and updating the necessary mappings (`layer_map`, `tensor_map`). This results in missing input tensors and incorrect computations during the layer cloning process, leading to errors in predicting the output of the cloned model.

### Bug Fix Strategy:
1. Ensure that the input_layers are correctly created based on the provided `input_tensors` list to maintain consistency.
2. Update the `input_layers` and `input_tensors` mappings appropriately when creating input layers to capture the correct relationship between original input layers and newly created ones.

### Corrected Version of the `_clone_functional_model` Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    input_layers = []
    input_tensors = []
    for layer in model._input_layers:
        input_tensor = Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
        input_layers.append(input_tensor)
        layer_map[layer] = input_tensor._keras_history[0]

    for i, x in enumerate(input_tensors):
        if not K.is_keras_tensor(x):
            name = model._input_layers[i].name
            input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
            input_layers.append(input_tensor)
            layer_map[x]._keras_history = (input_tensor, 0, 0)
            layer_map[x] = input_tensor
        else:
            input_layers.append(x)

    for x, y in zip(model.inputs, input_layers):
        tensor_map[x] = (y, None)

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

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments or {}
                computed_tensors, computed_masks = zip(*computed_data) if computed_data else ((), ())
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_layers, output_tensors, name=model.name)
```

With these corrections, the `_clone_functional_model` function should now properly handle the creation of input layers and mappings, allowing the cloned model to predict outputs correctly based on the provided input tensors.