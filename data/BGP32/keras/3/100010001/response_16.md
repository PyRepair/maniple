### Analysis:
1. The error message is raised from the `clone_model` function in the `keras/models.py` file.
2. The error occurs when trying to clone a model that has multiple outputs and complex layers like Lambda and custom SwapLayer.
3. The error message suggests that the model cloning process failed to compute the output tensor for a specific layer `Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`.
4. The issue likely stems from the complexity of the model structure and the handling of multiple inputs and outputs during the cloning process.

### Bug Cause:
- The error is triggered because the `for x in model.outputs` loop in the `_clone_functional_model` function fails to find the output tensor in the `tensor_map`.
- The `assert` statement expects the output tensor (`x`) to be present in the `tensor_map`, but due to the complex structure of the model and potentially missing mapping during the cloning process, the specific output tensor cannot be found.

### Bug Fix Strategy:
1. Ensure that all layers and input/output tensors are correctly mapped during the model cloning process.
2. Update the tensor mapping logic to handle multiple inputs/outputs especially in scenarios involving Lambda layers or custom layers.
3. Check for cases where the cloning process might not be fully completing the mapping of all input/output tensors.

### Bug Fix in the Function:
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
        input_tensors = [Input(batch_shape=input_layer._batch_input_shape, name=input_layer.name)
                         for input_layer in model._input_layers]

    for original_input, cloned_input in zip(model._input_layers, input_tensors):
        tensor_map[original_input] = (cloned_input, None)

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            outbound_layer = node.outbound_layer

            if outbound_layer not in layer_map:
                new_layer = outbound_layer.__class__.from_config(outbound_layer.get_config())
                layer_map[outbound_layer] = new_layer
            else:
                new_layer = layer_map[outbound_layer]

            reference_input_tensors = node.input_tensors
            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                input_tensors, masks = zip(*computed_data)
                output_tensors = new_layer(input_tensors)
                for original_output, cloned_output in zip(node.output_tensors, output_tensors):
                    tensor_map[original_output] = (cloned_output, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
``` 

This corrected function addresses the issue by correctly mapping input/output tensors during the cloning process, especially when dealing with models that have multiple outputs and complex layer structures.