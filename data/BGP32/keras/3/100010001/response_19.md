The bug in the `_clone_functional_model` function is that it checks if the input `model` is an instance of `Model` but it should check if it is an instance of a functional `Model`, not a `Sequential` model. Additionally, there is an issue in how the input_layers are handled when `input_tensors` are provided.

1. Error:
The error message indicates that the function is failing to compute the output for a tensor created by a custom layer (`SwapLayer`). This results in the assertion error stating that it could not compute the output for that tensor.

2. Potential Error Locations:
The error could potentially be in how the input layers are handled when input_tensors are provided, as well as the check for the model type.

3. Cause of the Bug:
The bug occurs because the function incorrectly handles the input layers when input_tensors are provided. It also incorrectly checks if the input model is a functional `Model` instead of a `Sequential` model.

4. Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the input layers are correctly handled when input_tensors are provided. Additionally, we should check if the input model is a functional `Model` and not a `Sequential` model.

5. Corrected Version of the Function:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', type(model))

    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.output_shape[1:]) for layer in model.layers]
    else:
        input_tensors = [x._keras_history[0] if K.is_keras_tensor(x) else x for x in to_list(input_tensors)]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
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
            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                
                input_args = [x[0] for x in computed_data]
                if has_arg(layer.call, 'mask'):
                    kwargs['mask'] = [x[1] for x in computed_data]

                output_tensors = to_list(layer(input_args, **kwargs))

                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

In the corrected function:
- The handling of input layers has been corrected to ensure placeholder inputs are created correctly when `input_tensors` are not provided.
- The check for the model type has been revised to ensure that the input model is a functional `Model` and not a `Sequential` model.
- The loop for iterating over the nodes in the model and computing the output has been optimized for clarity and correctness.