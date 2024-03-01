## Analysis:
1. The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance.
2. The function involves creating new layers, input tensors, and mapping existing tensors to new ones.
3. The bug seems to be related to the incorrect handling of the `input_layers` and `input_tensors` in the function, leading to wrong computations of output tensors.
4. The failing test `test_clone_functional_model_with_multi_outputs` expects the cloned model to produce the same outputs as the original model.
5. The GitHub issue mentions a similar problem related to cloning models with multi outputs and missing masks support for certain layers.

## Bug Explanation:
The bug in the function `_clone_functional_model` causes incorrect handling of input tensors when processing the layers of the model. This incorrect handling leads to the failure to compute output tensors correctly, resulting in an error similar to the one mentioned in the GitHub issue. Specifically, the issue is related to the way input tensors are processed, mapped, and utilized during the computation of output tensors.

## Bug Fix Strategy:
To fix the bug, we need to ensure that the input tensors are correctly mapped to their corresponding tensors throughout the cloning process. Additionally, we need to account for cases where layers do not support masks to prevent errors during the computation of output tensors.

## Corrected Function:
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
        input_tensors = to_list(input_tensors)

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
            else:
                new_layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            computed_data = [(tensor_map[x][0], None) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]

                if has_arg(new_layer.call, 'mask'):
                    kwargs['mask'] = [x[1] for x in computed_data if x[1] is not None]

                output_tensors = to_list(new_layer(computed_tensors, **kwargs))

                for i, x in enumerate(reference_input_tensors):
                    tensor_map[x] = (output_tensors[i], None)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

The corrected function modifies the handling of input tensors, ensures correct mapping of tensors throughout the process, and accounts for layers that do not support masks. This correction should address the issue and enable the function to clone functional models successfully, passing the failing test and aligning with the expected input/output values.