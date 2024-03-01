### Analysis
The buggy function is intended to clone a functional model instance by creating new layers and weights. It encounters an issue when dealing with multi-output layers and lambda layers without mask support, leading to incorrect output masks being generated and causing the final assertion in the failing test to fail.

### Error Locations
1. In the `input_layers` loop, the `input_layers` list is not populated correctly.
2. In the loop iterating over nodes, the conditions checking computed data and handling the layer call need improvement to consider multi-input cases properly.

### Bug Cause
The bug is caused by incorrect handling of multi-output layers and lambda layers without mask support. This leads to incorrect output masks being generated and results in failing the final assertion in the test case.

### Strategy for Fixing the Bug
To fix the bug, we need to properly initialize the `input_layers` list, adjust the conditions for handling computed data, and ensure correct handling when calling the layer in a multi-input scenario.

### Corrected Version
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
            input_layer = Input(batch_shape=layer.batch_input_shape,
                                dtype=layer.dtype,
                                sparse=layer.sparse,
                                name=layer.name)
            input_layers.append(input_layer)
            layer_map[layer] = input_layer
        input_tensors = input_layers
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)

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

            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                if node.arguments:
                    kwargs = node.arguments
                else:
                    kwargs = {}
                if len(computed_data) == 1:
                    computed_tensor = computed_data[0][0]
                    output_tensors = to_list(layer(computed_tensor, **kwargs))
                else:
                    computed_tensors = [x[0] for x in computed_data]
                    output_tensors = to_list(layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

After applying this correction, the `test_clone_functional_model_with_multi_outputs` test case should pass successfully without any assertions failing.