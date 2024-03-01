The bug in the function `_clone_functional_model` is related to the incorrect handling of input tensors and the corresponding node computation process. The error message indicates that the output tensor was not computed, leading to the assertion failure during the test.

### Bug Explanation:
1. The function incorrectly checks the type of the `model` argument. It should only raise an error if the input is not an instance of `Model`.
   
2. The creation of input layers and the handling of input tensors in the function are not synchronized, leading to issues in properly creating the model on top of new tensors.

3. In the node computation process, there are discrepancies in handling the input tensors, computing the outputs for each layer, and updating the tensor map.

### Fix Strategy:
1. Change the type checking to properly handle the `model` argument and remove the unnecessary check for `Sequential` instances.
   
2. Ensure that input layers and input tensors are correctly created and synchronized.

3. Fix the node computation process to accurately handle input tensors, compute outputs for each layer, and update the tensor map accordingly.

### Corrected Version of the Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got {}'.format(model))

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            # Cache newly created input layer.
            input_layers.append(input_tensor)
            layer_map[layer] = input_tensor
            
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                layer_map[model._input_layers[i]] = input_tensor
    
    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in reversed(range(len(model._nodes_by_depth))):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]
                if isinstance(new_layer, InputLayer):
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
                if has_arg(new_layer.call, 'mask') and 'mask' not in kwargs:
                    kwargs['mask'] = computed_masks
                output_tensors = to_list(new_layer(computed_tensors, **kwargs))
                output_masks = to_list(new_layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
``` 

With these corrections, the function should now correctly clone the functional model and pass the failing test case.