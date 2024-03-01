## Analysis:
1. The buggy function `_clone_functional_model` is meant to clone a functional `Model` instance by creating new layers and weights instead of sharing existing ones. The function goes through the model's input layers, nodes, and outputs to create a new model with the same behavior but different weights.
   
2. Upon analyzing the function, potential error locations include:
   - Incorrect handling of input tensors and their mapping.
   - Incorrect creation of input layers.
   - Issues related to node traversal and layer cloning.
   - Handling of computed data and model outputs.
   
3. The bug is evident in the failing test `test_clone_functional_model_with_multi_outputs` where `clone_model` fails to accurately reproduce the model's behavior due to issues in handling multiple outputs and layers without mask support. The expected values and types provide crucial insight into the problematic areas.

4. To fix the bug, the function needs adjustments in handling input tensors, creating new layers, ensuring correct layer cloning, managing computed data, and accurately mapping model outputs.

## Bug Fix:
Here is the corrected version of the `_clone_functional_model` function that addresses the identified issues and resolves the bug.

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
        for _original, _cloned in zip(model._input_layers, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        _input_tensors = []
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model._input_layers[i].name
                input_tensor = Input(tensor=x,
                                     name='input_wrapper_for_' + name)
                _input_tensors.append(input_tensor)
                layer_map[x] = input_tensor
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in range(len(model._nodes_by_depth)):
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
                computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(
                    layer(computed_tensors, **kwargs))
                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    return Model(input_tensors, output_tensors, name=model.name)
```

By incorporating the changes outlined, the corrected function should now pass the failing test and ensure proper handling of multiple outputs and layers without mask support.