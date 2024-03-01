### Analysis
1. The `clone_model` function is a critical part of the Keras library, responsible for cloning a functional model instance. The bug in the `_clone_functional_model` function is causing issues with multi-output models when utilizing `clone_model`.
2. The bug seems to be related to handling multiple output tensors without proper mask support, leading to a failure in computing output tensors.
3. The failing test case `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs and then clones that model using `clone_model`. The model is used to make predictions and compare them, which currently fails due to the underlying issue.
4. The GitHub issue indicates a similar problem occurring due to a specific setup using `clone_model` with `multi_gpu_model` and `cpu_relocation=True` resulting in an Assertion Error. The issue points to the same underlying problem of incorrect handling with output masks.
5. To fix the bug, we need to address the handling of multiple output tensors and masks, ensuring proper computation during cloning of functional models.

### Bug Fix Strategy
1. Update the code to handle multiple output tensors properly, considering cases where masks may be `None`.
2. Ensure that all output tensors are computed correctly while iterating over the nodes in the model.
3. Check for the presence of masks and handle them appropriately for different scenarios.

### Corrected Version of the Function

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
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    else:
        input_tensors = to_list(input_tensors)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in model._nodes_by_depth:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]

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

                for x, y, mask in zip(reference_output_tensors, output_tensors, computed_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

By revising how the output tensors and masks are handled during the cloning process, the corrected function should now be able to successfully clone functional models with multiple outputs, resolving the issue raised in the test case and GitHub.