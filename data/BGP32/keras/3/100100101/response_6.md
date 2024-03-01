The bug in the `_clone_functional_model` function arises from incorrect handling of input tensors when creating a new model by cloning a functional model instance. The incorrect parts include not adding input tensors to `input_layers` and skipping the creation of placeholders. 

Here is a corrected version of the `_clone_functional_model` function:

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
            input_layers.append(input_tensor)
            layer_map[layer] = input_tensor
        
    for original_input, cloned_input in zip(model._input_layers, input_layers):
        layer_map[original_input] = cloned_input

    for input_tensor, new_input in zip(model.inputs, input_tensors):
        tensor_map[input_tensor] = (new_input, None)

    for depth in model._nodes_by_depth:
        for node in model._nodes_by_depth[depth]:
            inbound_layer = node.outbound_layer
            if inbound_layer not in layer_map:
                layer_config = inbound_layer.get_config()
                new_layer = inbound_layer.__class__.from_config(layer_config)
                layer_map[inbound_layer] = new_layer
            else:
                new_layer = layer_map[inbound_layer]

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
                
                output_tensors = new_layer([data[0] for data in computed_data], **kwargs)

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

This corrected function makes sure to add input tensors to `input_layers` properly and fixes the placeholder creation when input tensors are not provided. Additionally, it correctly maps input tensors and processes the model's nodes to create a new model.

By using this corrected version of the function, the failing test `test_clone_functional_model_with_multi_outputs` should now pass with the expected input/output values.