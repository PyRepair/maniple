## Analysis:
- The `AssertionError` occurs in the `test_clone_functional_model_with_multi_outputs` test function.
- The error points to the `keras/models.py` file in the `clone_model` function `_clone_functional_model`.
- Specifically, the issue arises when trying to compute the output tensors for the model, and the error message indicates a failure in computing the output for a specific tensor.

## Identifying the Bug:
- The bug seems to be related to the handling of input tensors and their mapping in the `_clone_functional_model` function.
- The `assert x in tensor_map` indicates that the particular output tensor `x` is not found in the `tensor_map`, which leads to the assertion failure.

## Bug Cause:
- The cause of the bug is likely due to incorrect mapping of tensors in the `tensor_map` dictionary. The assertion is failing because the output tensor is missing from the `tensor_map`, meaning it was not computed properly during the cloning process.

## Bug Fix:
To fix the bug:
- We need to ensure that all output tensors are correctly mapped in the `tensor_map` dictionary while iterating over the nodes and layers in the model.
- Each output tensor should be added to the `tensor_map` after it is computed.

## Corrected Code:
Here is the corrected version of the `_clone_functional_model` function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {} 
    tensor_map = {}  

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]

        for original_input, cloned_input in zip(model._input_layers, input_tensors):
            layer_map[original_input] = cloned_input
    else:
        input_tensors = [Input(tensor=x, name='input_wrapper_for_' + model._input_layers[i].name) if not K.is_keras_tensor(x) else x for i, x in enumerate(input_tensors)]

        for original_input, new_input in zip(model._input_layers, input_tensors):
            layer_map[original_input] = new_input

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in reversed(sorted(model._nodes_by_depth.keys())):
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
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for output, output_tensor, output_mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[output] = (output_tensor, output_mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

With these corrections, the `_clone_functional_model` function should now correctly clone the model and compute the output tensors as expected.