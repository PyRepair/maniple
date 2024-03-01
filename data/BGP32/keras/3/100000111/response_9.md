### Analysis:
The issue reported on GitHub describes a problem encountered when using `clone_model()` with `multi_gpu_model()` and `cpu_relocation=True`. The issue arises due to a bug in the `clone_model()` function that affects the computation of output tensors, specifically when a layer doesn't support masking. The error message received is `'Could not compute output Tensor'`.

### Bug Explanation:
1. In the provided function `_clone_functional_model`, the bug seems to originate from the handling of output masks for layers that do not support masking.
2. The function attempts to compute output masks for each layer, but for layers without mask support (like `Lambda` layers mentioned in the GitHub issue), the `compute_mask` method returns `None`.
3. This leads to an inconsistency in the expected output masks causing the function to raise an error when checking for computed output tensors.

### Bug Fix Strategy:
To fix the bug, we need to modify the logic of the function to correctly handle layers that do not support masks. One possible approach is to add a condition to check if the layer supports masking before attempting to compute and assign masks to the output tensors.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    """Clone a functional `Model` instance.

    Model cloning is similar to calling a model on new inputs,
    except that it creates new layers (and thus new weights) instead
    of sharing the weights of the existing layers.

    # Arguments
        model: Instance of `Model`.
        input_tensors: optional list of input tensors
            to build the model upon. If not provided,
            placeholders will be created.

    # Returns
        An instance of `Model` reproducing the behavior
        of the original model, on top of new inputs tensors,
        using newly instantiated weights.

    # Raises
        ValueError: in case of invalid `model` argument value.
    """
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    # Rest of the function remains unchanged from the original

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Rest of the function remains unchanged from the original

    computed_data = []  # List of tuples (input, mask)
    for x in reference_input_tensors:
        if x in tensor_map:
            computed_data.append(tensor_map[x])

    # Rest of the function remains unchanged from the original

    # Add a check to only compute masks if the layer supports masking
    if has_arg(layer.call, 'mask'):
        if len(computed_data) == 1:
            computed_tensor, computed_mask = computed_data[0]
            output_tensors = to_list(layer(computed_tensor, **kwargs))
            output_masks = to_list(layer.compute_mask(computed_tensor, computed_mask))
            computed_tensors = [computed_tensor]
            computed_masks = [computed_mask]
        else:
            computed_tensors = [x[0] for x in computed_data]
            computed_masks = [x[1] for x in computed_data]
            output_tensors = to_list(layer(computed_tensors, **kwargs))
            output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
    else:
        # Skip mask computation if the layer doesn't support masking
        if len(computed_data) == 1:
            computed_tensor, _ = computed_data[0]
            output_tensors = to_list(layer(computed_tensor, **kwargs))
            computed_tensors = [computed_tensor]
        else:
            computed_tensors = [x[0] for x in computed_data]
            output_tensors = to_list(layer(computed_tensors, **kwargs))

    # Rest of the function remains unchanged from the original

    return Model(input_tensors, output_tensors, name=model.name)
```

By adding a check to only compute masks if the layer supports masking, we ensure that the function handles layers without mask support correctly, resolving the issue reported in the GitHub bug.