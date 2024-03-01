### Analysis:
The function `_clone_functional_model` is designed to clone a functional `Model` instance by creating new layers and weights instead of sharing the existing layers' weights. The function iterates over the layers of the input `model`, creates new layers, and sets up connections between the layers based on the relationships defined in the input `model`.

The error message indicates an `AssertionError` caused by failing to compute the output tensors during the model cloning process. Specifically, the failing test asserts that it could not compute the output tensor of the model.

### Bug:
The bug appears to be related to how the model's outputs are handled during the cloning process in the `_clone_functional_model` function. The assertion error indicates that the function failed to compute the output tensor of a specific layer (`swap_layer_1`). This could be due to an incomplete implementation of handling multiple outputs while cloning the model.

### Strategy for Fixing the Bug:
To fix the bug, we need to ensure that all output tensors of the model are correctly computed during the cloning process. This involves correctly setting up the connections and mapping between input and output tensors of the layers as the cloning proceeds.

### Fix - Corrected Version of `_clone_functional_model`:
The corrected version of the `_clone_functional_model` function is provided below:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name)
                         for layer in model._input_layers]
    for x, y in zip(model.inputs, input_tensors):
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
            
            reference_input_tensors = node.input_tensors
            computed_inputs = [tensor_map[x][0] for x in reference_input_tensors if x in tensor_map]
            if len(computed_inputs) == len(reference_input_tensors):
                output_tensors = to_list(layer(computed_inputs))
                output_tensors = [x for x in output_tensors if x is not None]
                for x, y in zip(node.output_tensors, output_tensors):
                    tensor_map[x] = (y, None)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected version ensures that the output tensors are correctly computed during the model cloning process by correctly setting up the connections between layers and handling multiple outputs.