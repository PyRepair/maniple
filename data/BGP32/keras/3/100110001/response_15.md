### Analysis:
1. The error message indicates that the assertion in the `_clone_functional_model` function fails to compute an output tensor for a specific layer (`swap_layer_1/Identity:0`).
2. The function should create a new model based on the given `model` instance and input tensors, but it fails to properly compute the output tensors while iterating through the nodes of the model.
3. The cause of the bug seems to be related to the handling of input tensors and correctly mapping them to the output tensors during the node iteration process.

### Bug Cause:
The bug is caused by the incorrect mapping between the input and output tensors while processing the nodes of the model in the `_clone_functional_model` function. There is an issue with how the input tensors are being traced and passed through the layers, leading to the failure to compute the output tensor for the specific layer (`swap_layer_1/Identity:0`).

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that the input tensors are correctly mapped to the corresponding output tensors for each layer in the model. This involves properly updating the `tensor_map` and handling the computation of outputs based on the input tensors provided. We need to make sure that the relationship between input and output tensors is preserved during the node iteration process.

### Corrected Version of the Function:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        inputs = [Input(batch_shape=layer.output_shape[1:]) for layer in model.layers if isinstance(layer, InputLayer)]
        input_tensors = inputs

    for original_layer, input_layer in zip(model.input_layers, input_tensors):
        layer_map[original_layer] = input_layer

    for layer in model.layers:
        if layer not in layer_map:
            new_layer = layer.__class__.from_config(layer.get_config())
            layer_map[layer] = new_layer

    for layer in model.layers:
        if isinstance(layer, InputLayer):
            continue

        inbound_layers = [layer_map[node.inbound_layers[i]] for i in range(len(node.inbound_layers))]
        input_tensors = [tensor_map[x][0] for x in inbound_layers]

        kwargs = node.arguments if node.arguments else {}
        output_tensors = to_list(layer.call(computed_tensors, **kwargs))
        output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

        for x, y, mask in zip(layer.inbound_nodes, output_tensors, output_masks):
            tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version ensures that the input tensors are properly handled and mapped to the corresponding output tensors during the model cloning process. This should resolve the issue encountered in the failing test.