## Analyzing the buggy function:

The `_clone_functional_model` function is intended to clone a functional model by creating new layers and weights instead of sharing the weights of the original model. The function iterates over nodes in the original model and creates new layers based on the configuration of the original layers.

## Bug Identification:

1. The function incorrectly checks the type of `model` with the isinstance function. It should check for the sequential model before checking for the functional model.
2. The function does not properly create input_layers when `input_tensors` are None.
3. The function does not correctly handle the creation and mapping of input layers.
4. There is an issue with the indexes and mapping of input tensors and input layers in the for loop.

## Bug Explanation:

The major bug in the function lies in the logic used to create and map input layers when `input_tensors` is None. Additionally, the error-handling for input tensors that are not Keras layers is not properly implemented.

## Bug Fix Strategy:

1. Fix the isinstance check to first check for Sequential before checking for Model.
2. Correctly create input layers and input tensors when `input_tensors` is None.
3. Ensure proper mapping between original input layers and newly created input layers.

## Corrected Version of the Function:

```python
def _clone_functional_model(model, input_tensors=None):
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument '
                         'to be a functional `Model` instance, '
                         'got a `Sequential` instance instead:', model)
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument '
                         'to be a `Model` instance, got ', model)
    
    layer_map = {}  # Cache for created layers.
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
                original_input_layer = x._keras_history[0]
                layer_map[original_input_layer] = input_tensor
            else:
                _input_tensors.append(x)
        input_tensors = _input_tensors

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

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
                
                if has_arg(layer.call, 'mask'):
                    if 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks
                    
                output_tensors = to_list(
                    layer(computed_tensors, **kwargs))
                output_masks = to_list(
                    layer.compute_mask(computed_tensors,
                                       computed_masks))
                
                for x, y, mask in zip(node.output_tensors,
                                      output_tensors,
                                      output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = []
    for x in model.outputs:
        assert x in tensor_map, 'Could not compute output ' + str(x)
        tensor, _ = tensor_map[x]
        output_tensors.append(tensor)
    
    return Model(input_tensors, output_tensors, name=model.name)
``` 

This corrected version of the function addresses the identified bugs and should now work as intended.