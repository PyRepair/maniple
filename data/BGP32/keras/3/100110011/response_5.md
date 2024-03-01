### Analysis:
1. The buggy function `_clone_functional_model` is responsible for cloning a functional `Model`. It is meant to create a new model with newly instantiated weights by recreating the layers instead of sharing the weights of the original layers.
2. In the failing test `test_clone_functional_model_with_multi_outputs`, a model with multiple outputs is created, and then the `clone_model` function is called, which internally calls the `_clone_functional_model` function.
3. The specific error message observed is an `AssertionError` stating "Could not compute output Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)". This error occurs because the `assert` statement in the buggy function fails, indicating that the output tensor was not calculated during the model cloning process.
4. The GitHub issue further highlights a similar error where the `clone_model` function is causing issues when using a layer without mask support in conjunction with multi-gpu processing, leading to a "Could not compute output" error.
5. The root cause of the bug lies in the logic where the output tensors are calculated and stored in the `tensor_map` within the `_clone_functional_model` function. Since some layers do not support masks, the output masks are always `None`, leading to a mismatch in the expected output calculations.

### Fix Strategy:
1. Update the logic for handling output tensors and masks in layers that do not support masks.
2. Modify the `clone_model` or `_clone_functional_model` function to handle such cases and ensure that the output tensors are correctly computed and stored in the `tensor_map`.
3. Verify that the output tensors are correctly calculated for all layers, even when the masks are not applicable.
4. Ensure that the new model instantiated from the cloned layers produces the expected output tensors.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}
    tensor_map = {}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name)
                         for layer in model._input_layers]

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

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
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                    computed_tensors = [computed_tensor]
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
``` 

By updating the logic in the `_clone_functional_model` function to correctly handle output tensors for layers without mask support, the bug should be fixed. This corrected version should resolve the `AssertionError` and successfully clone the functional model as intended.