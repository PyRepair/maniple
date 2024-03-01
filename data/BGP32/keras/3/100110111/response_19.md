### Analysis:
1. The `clone_model` function is calling the `_clone_functional_model` function with the model object as input.
2. The error occurs in the `_clone_functional_model` function when checking for the model's type and input tensors.
3. The `test_clone_functional_model_with_multi_outputs` test function creates a model with multiple outputs and then tries to clone this model using `clone_model`.
4. The error message indicates that there is an issue with computing the output tensor during the cloning process, specifically related to the `swap_layer_1/Identity` tensor.
5. The expected values and types of variables provide insights into how the variables should be managed within the `_clone_functional_model` function.

### Bug Cause:
The bug is caused by not handling the specific case of layers like `SwapLayer()` that produce multiple outputs. When looping through the model's outputs in the `output_tensors` check, the `SwapLayer` node's output tensor does not get computed properly due to incorrect handling.

### Strategy for Fixing the Bug:
1. Modify the code to correctly handle the case of layers that generate multiple outputs when cloning the model.
2. Ensure that all the output tensors are correctly computed during the cloning process.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
  
    input_tensors = input_tensors or [Input(batch_shape=layer.output_shape[1:]) for layer in model._input_layers]

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    for original_layer, input_tensor in zip(model._input_layers, input_tensors):
        layer_map[original_layer] = input_tensor

    for node in model._nodes_by_depth:
        inbound_tensors = [tensor_map[x][0] for x in node.input_tensors if x in tensor_map]
        # Compute output_tensors based on the inbound_tensors and the node properties
        output_tensors = node.outbound_layer(inbound_tensors)

        for x, y in zip(node.output_tensors, output_tensors):
            tensor_map[x] = (y, None)

    # Collect computed output tensors
    output_tensors = []
    for x in model.outputs:
        if x not in tensor_map:
            raise ValueError('Could not compute output ', x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
```

Now, the corrected function should handle the case of multiple outputs from layers like `SwapLayer` properly, ensuring that all output tensors are computed and mapped correctly during the cloning process.