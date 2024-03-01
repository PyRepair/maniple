### Analysis:
1. The `clone_model` function calls the `_clone_functional_model` function with the given model and input tensors.
2. The error occurs due to the failure of asserting that all model outputs have been computed in the `_clone_functional_model` function.
3. The output tensor `x` in the model is not found in the `tensor_map`, causing the assertion error.
4. The cause of the bug is that the input tensors are not properly processed and mapped in the `_clone_functional_model` function, leading to missing output tensors in the `tensor_map`.
   
### Bug Fix:
To fix the bug, ensure all input tensors are properly processed and mapped to their corresponding tensors in the `tensor_map` when cloning the functional model.

### Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  
    tensor_map = {}  

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                               dtype=layer.dtype,
                               sparse=layer.sparse,
                               name=layer.name) for layer in model._input_layers]
        for _original, _cloned in zip(model.inputs, input_tensors):
            layer_map[_original] = _cloned
    else:
        input_tensors = to_list(input_tensors)
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = model.inputs[i].name
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                input_tensors[i] = input_tensor
                original_input_layer = x._keras_history[0]
                newly_created_input_layer = input_tensor._keras_history[0]
                layer_map[original_input_layer] = newly_created_input_layer

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None) 

    for depth in reversed(range(len(model._nodes_by_depth))):
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

                computed_tensors = [computed_data[i][0] for i in range(len(computed_data))]
                computed_masks = [computed_data[i][1] for i in range(len(computed_data))]
                if has_arg(layer.call, 'mask'):
                    if 'mask' not in kwargs:
                        kwargs['mask'] = computed_masks

                output_tensors = to_list(layer(computed_tensors, **kwargs))

                for i, output_tensor in enumerate(output_tensors):
                    tensor_map[reference_output_tensors[i]] = (output_tensor, None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]

    return Model(input_tensors, output_tensors, name=model.name)
``` 

After fixing the `_clone_functional_model` function, the failing test should pass without any assertion errors.