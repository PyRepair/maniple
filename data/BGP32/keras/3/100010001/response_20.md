The bug in the `_clone_functional_model` function is causing an assertion error because it fails to correctly compute the output tensors when cloning a functional Keras model with multiple outputs. The issue arises from how the function handles multiple input and output tensors attached to a Layer and the usage of input_tensors for referencing these tensors.

To fix this bug, we need to ensure that the `layer_map` and `tensor_map` dictionaries are updated correctly to handle multiple outputs and inputs. Specifically, we should create new lists to store the cloned layers and input tensors during the cloning process, and we need to correctly match the input tensors to the corresponding output tensors when updating the `tensor_map`.

Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    input_layers = []
    input_tensors = [] if input_tensors is None else to_list(input_tensors)

    for layer in model._input_layers:
        input_tensor = Input(batch_shape=layer.batch_input_shape,
                             dtype=layer.dtype,
                             sparse=layer.sparse,
                             name=layer.name)
        input_layers.append(input_tensor)
        input_tensors.append(input_tensor)
        layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in range(len(model._nodes_by_depth)):
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
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_layers, output_tensors, name=model.name)
```

This corrected version of the function should now be able to handle multiple inputs and outputs correctly when cloning a functional Keras model. It addresses the issue of properly matching input tensors to output tensors during the cloning process, ensuring that the cloned model is created accurately.