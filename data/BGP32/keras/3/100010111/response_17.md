### Analysis:
1. The buggy function `_clone_functional_model` is intended to clone a functional model with newly instantiated weights and newly created layers. 
2. The error occurs when the function is called with a multi-output model containing layers without mask support, leading to the AssertionError: "Could not compute output Tensor(...)".
3. The function fails to handle the case where the layer's `compute_mask` method returns `None` due to lack of mask support, leading to incorrect behavior.
4. To fix the bug, we need to modify the logic that handles the creation of output masks and adapt it to handle cases where the output mask is `None`.
5. By updating the logic for mask handling, we can ensure that the function correctly computes the model outputs without encountering the AssertionError.

### Plan for Fixing the Bug:
1. Modify the logic for handling output masks to account for cases where the computed mask is `None`.
2. Update the function to handle the absence of masks for layers that don't support masking.
3. Ensure that the function correctly computes the model outputs even when some layers have `None` as the output mask.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  

    # Input creation logic
    if input_tensors is None:
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_layer = Input(batch_shape=layer.batch_input_shape,
                                dtype=layer.dtype,
                                sparse=layer.sparse,
                                name=layer.name)
            input_tensors.append(input_layer)
            layer_map[layer] = input_layer
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        input_tensors = to_list(input_tensors)
        new_input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_layer = Input(tensor=x, name='input_wrapper_for_' + name)
                new_input_tensors.append(input_layer)
                layer_map[x] = input_layer
            else:
                new_input_tensors.append(x)
        input_tensors = new_input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    # Iterate over nodes in the model
    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
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
                if len(computed_data) == 1:
                    computed_tensor, computed_mask = computed_data[0]
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

By updating the logic for handling output masks and adapting to cases where layers return `None` masks, the corrected function should now successfully clone functional models without encountering the previous AssertionError issue.