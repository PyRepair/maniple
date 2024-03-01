### Analysis:
1. The buggy function `_clone_functional_model` is meant to clone a functional `Model` instance by creating new layers and new weights instead of sharing existing ones.
2. Upon examination, the function encounters an issue when dealing with multi-output layers without mask support. This situation leads to the "Could not compute output Tensor" error.
3. The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multi-output layers and then attempts to clone it.
4. The cause of the bug lies in the handling of output masks for layers that do not support masking, resulting in the incorrect behavior when creating the cloned model.
5. To resolve the bug, the function needs to properly handle layers without mask support to align with the multi-output scenario outlined in the failing test.

### Solution:
To address the bug and align the function properly with the failing test, the handling of output masks needs to be adjusted. The modification involves considering layers that do not support masks and updating the `output_masks` accordingly.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                                sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
        
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned
    else:
        # Handle input tensors that do not originate from Keras layers
        input_tensors = to_list(input_tensors)
        
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

    for depth in reversed(sorted(model._nodes_by_depth.keys())):
        for node in model._nodes_by_depth[depth]:
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
                computed_masks = [x[1] for x in computed_data]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                if layer.supports_masking:
                    output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                else:
                    output_masks = [None] * len(output_tensors)

                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, mask = tensor_map[x]
        output_tensors.append(tensor)

    return Model(input_tensors, output_tensors, name=model.name)
``` 

This corrected function now properly handles the creation of multi-output models and resolves the error related to output masks when cloning a model with layers lacking mask support.