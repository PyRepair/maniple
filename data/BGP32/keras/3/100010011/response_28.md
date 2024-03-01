### Analysis:
1. The buggy function `_clone_functional_model` is meant to clone a functional model instance. The error message is indicating that it cannot compute the output tensor of the cloned model.
2. The issue on GitHub highlights a similar problem where `clone_model` method is failing due to the inability to compute the output tensor because of a layer without mask support.
3. The bug arises when a layer without mask support is used in a model with multiple outputs, causing the assertion error because the output mask is `None` instead of the expected list of masks.
4. The strategy for fixing the bug involves updating the logic to handle cases where layers don't support masks, specifically for models with multiple outputs.

### Proposed Fix:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    
    # Check if model is of type Sequential
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}
    
    # Rest of the function remains the same as the original

    # Iterate over every node in the reference model in depth order
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            
            # Code to recover the corresponding layer remains the same
            
            # Check if layer has 'compute_mask' and 'mask' arguments
            has_mask_arg = has_arg(layer.call, 'mask')
            has_comput_mask = hasattr(layer, 'compute_mask')

            # Gather inputs to call the new layer
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            computed_data = []  

            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                # Call layer
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}

                if has_comput_mask:
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                # Update tensor_map
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)
    
    # Check that we did compute the model outputs
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

By checking for the presence of `compute_mask` and handling the mask updates accordingly, the fixed function should now be able to handle models with multiple outputs and layers without mask support successfully.