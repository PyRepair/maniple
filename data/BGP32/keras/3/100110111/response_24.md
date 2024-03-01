### Analysis:
The buggy function `_clone_functional_model` is not handling the case where the model is a `Model` instance but not a functional one. This leads to the raised error when trying to clone the model.

### Bug Cause:
1. The `_clone_functional_model` function does not check properly if the input model is a functional `Model` instance.
2. The error occurs at the assert statement where it fails to recognize the output tensor during the computation process, resulting in the assertion error.

### Strategy for Fixing the Bug:
1. Check if the model is a functional model instance.
2. Ensure that all the input tensors have a mapping in the tensor map during the computation process.
3. Verify that the output tensors are computed correctly and mapped back to the tensor map.

### The corrected version of the function:

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
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)
    
    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
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
        tensor_map[x] = (y, None)  # tensor, mask
    
    # Iterate over every node in the reference model, in depth order
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    
    for depth in depth_keys:
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            
            if layer not in layer_map:
                cloned_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = cloned_layer
            
            cloned_layer = layer_map[layer]
            
            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors
            
            computed_data = []  # List of tuples (input, mask)
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])
            
            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                
                computed_tensors = [x[0] for x in computed_data]
                computed_masks = [x[1] for x in computed_data]
                
                if has_arg(cloned_layer.call, 'mask'):
                    kwargs['mask'] = computed_masks
                
                output_tensors = to_list(cloned_layer(computed_tensors, **kwargs))
                output_masks = to_list(cloned_layer.compute_mask(computed_tensors, computed_masks))
                
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)
    
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

After replacing the buggy function with the corrected version, it should now handle the given test case successfully without raising any errors.