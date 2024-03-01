### Analysis:
1. The function `_clone_functional_model` is responsible for cloning a functional model instance.
2. The function involves creating new layers and input placeholders to replicate the original model's behavior.
3. The function encounters an issue when trying to compute the output tensors due to a discrepancy in the expected and actual output mask values.
4. The root cause of the bug lies in the handling of masks for layers that do not support masking, such as Lambda layers.
5. To address the bug, we need to modify the logic for computing masks when calling layers that may not support masking.

### Bug Fix Strategy:
1. Modify the logic related to output mask computation to accommodate layers without masking support.
2. Handle the case where a layer does not support masks by setting the mask attribute to None or deal with masking differently when applying the layer.
3. Update the function to correctly handle the scenario where Lambda layers are involved and do not support masks.

### Bug Fix:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    # Existing code remains the same until the loop where output tensors are computed

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # Update to store mask as None initially

    # Iterating over nodes in the reference model and handle layers without masking support
    depth_keys = list(model._nodes_by_depth.keys())
    depth_keys.sort(reverse=True)
    for depth in depth_keys:
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
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                
                if len(computed_data) == 1:
                    computed_tensor, _ = computed_data[0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)  # Update to store mask as None

    # Validate the output computation and create a new model instance
    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
```

By updating the mask handling logic and ensuring that 'None' is used for layers without masking support, the function should now correctly clone a functional model without encountering the previous error related to output tensor computation.