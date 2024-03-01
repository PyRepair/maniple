The bug in the provided function is due to the incorrect handling of input placeholders and the creation of new layers when cloning a functional model. The function fails to create the input layers correctly and handle the layer mapping and tensor mapping leading to errors in creating the cloned model.

To fix the bug, the following corrective steps should be taken:
1. Ensure correct creation and mapping of input placeholders.
2. Properly clone each layer when creating the new model.
3. Update the tensor mapping for output tensors.

Here is the corrected version of the _clone_functional_model function:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)
    
    layer_map = {}  
    tensor_map = {}
    
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
        for i, x in enumerate(input_tensors):
            name = model._input_layers[i].name
            input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
            input_tensors[i] = input_tensor
            layer_map[model._input_layers[i]] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

    for depth in range(len(model._nodes_by_depth)):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                
                computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                
                for x, y, mask in zip(reference_output_tensors, output_tensors, computed_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

By aligning the input placeholders creation, layer cloning, and tensor mapping, the corrected function should now successfully clone a functional model as intended.