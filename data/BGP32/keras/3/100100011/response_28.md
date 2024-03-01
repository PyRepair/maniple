### Analysis:
1. The buggy function `_clone_functional_model` is used to clone a functional `Model` instance in Keras.
2. The buggy function iterates over the nodes in the model, tries to create new layers, and then creates a new model based on the inputs and outputs.
3. The failing test `test_clone_functional_model_with_multi_outputs` creates a model with multiple inputs and outputs, including a Lambda layer and a SwapLayer.
4. The failing test checks if the predictions from the original model and the cloned model are the same, but the bug in `_clone_functional_model` results in an error while computing the output tensors.
5. The GitHub issue points out a similar error that occurs when using `clone_model` with multi-output layers that do not support masks.

### Bug:
The bug occurs when the output masks are always `None` for layers that do not support masks, leading to the error "Could not compute output". This is due to the `to_list` function always expecting masks but not getting them from layers without mask support like Lambda.

### Fix:
To fix this bug, we need to modify the way output masks are handled for layers that do not support masks. We can update the logic in `_clone_functional_model` to handle layers without mask support appropriately.

### Corrected Version:
```python
def _clone_functional_model(model, input_tensors=None):
    # Existing implementation
    # ...

    if model.__class__ == Model:
        layer_map = {}  
        tensor_map = {}  

        # Existing implementation
        # ...

        for x, y in zip(model.inputs, input_tensors):
            tensor_map[x] = (y, None)  # tensor, mask

        # Iterated over every node in the reference model, in depth order
        depth_keys = list(model._nodes_by_depth.keys())
        depth_keys.sort(reverse=True)
        for depth in depth_keys:
            nodes = model._nodes_by_depth[depth]
            for node in nodes:
                # Get or create layer
                # ...

                computed_data = []  
                for x in reference_input_tensors:
                    if x in tensor_map:
                        computed_data.append(tensor_map[x])

                if len(computed_data) == len(reference_input_tensors):
                    # Call layer
                    # ...

                    computed_tensors = [x[0] for x in computed_data]
                    if has_arg(layer.call, 'mask'):
                        if 'mask' not in kwargs:
                            kwargs['mask'] = [None] * len(computed_tensors)

                    output_tensors = to_list(
                        layer(computed_tensors, **kwargs))
                    # Update tensor_map
                    for x, y in zip(reference_output_tensors, output_tensors):
                        tensor_map[x] = (y, None)

        # Check that we did compute the model outputs
        output_tensors = []
        for x in model.outputs:
            assert x in tensor_map, 'Could not compute output ' + str(x)
            tensor, _ = tensor_map[x]
            output_tensors.append(tensor)

        return Model(input_tensors, output_tensors, name=model.name)
    else:
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
```

By updating the logic to handle layers without mask support in the `clone_functional_model` function, we can address the issue reported in the failing test and the GitHub issue. This correction should now allow the function to successfully clone functional models with multiple outputs.