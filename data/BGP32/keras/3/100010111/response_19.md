### Analysis:
1. The function `_clone_functional_model` is tasked with cloning a functional model by creating new layers and weights instead of sharing existing ones.
2. The function checks if the input `model` is an instance of `Model` and not a `Sequential` model before proceeding.
3. The error occurs during the test case where the function fails due to an assertion error while computing the model outputs. This is related to a discrepancy in the expected and actual tensor values stored in the `tensor_map`.
4. The issue on GitHub highlights a similar problem where the `clone_model` function fails due to the inability to compute output tensors for a model containing layers that do not support masking.

### Potential Bug Location:
1. Incorrect handling of layer masks that results in `output_masks` being assigned `None` although multiple masks should be expected for the outputs.
2. The tensor mapping in the function may not be capturing the correct mappings for all tensors, leading to a missing match between reference and actual tensors.

### Bug Cause:
The issue arises from the discrepancy in the expected number of masks for the output tensors in the function. Due to the lack of support for masks in certain layers like Lambda, the function incorrectly returns `None` as the output masks instead of the expected list of masks.

### Bug Fix Strategy:
1. Ensure that the function correctly handles the case when the layer does not support masks.
2. Verify that the tensor mapping includes appropriate mappings between reference and actual tensors, accounting for layers without mask support.

### A Corrected Version of the Function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    # Create input tensors if not provided
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
        
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            else:
                layer = layer_map[layer]
                if isinstance(layer, InputLayer):
                    continue
            
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            
            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]
            
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                
                computed_tensors = [x[0] for x in computed_data]
    
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)
    
    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

With this corrected implementation, the function should now correctly handle the cloning of the functional model and resolve the issue encountered during the failing test.