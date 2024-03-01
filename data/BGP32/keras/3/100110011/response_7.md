### Analysis:
1. The buggy function `_clone_functional_model` is intended to clone a functional `Model` instance, creating new layers and weights instead of sharing the existing ones.
2. The test function `test_clone_functional_model_with_multi_outputs` creates a model with multiple outputs and uses `keras.models.clone_model` to clone it.
3. The error message indicates that the model's output tensor is not found in the `tensor_map`, causing an assertion error.
4. The GitHub issue also mentions a similar scenario where the error occurs due to the lack of support for masks in certain layers like `Lambda`.

### Bug Cause:
The bug is caused because the code does not handle the case where the `output_tensors` for a specific layer are not computed and added to the `tensor_map`, leading to the missing tensor during the cloning process.

### Fix Strategy:
To fix the bug, we need to ensure that all the output tensors for each layer in the model are properly computed and added to the `tensor_map`.

### Corrected Function:
```python
from keras.engine.saving import model_from_config
import numpy as np

def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  
    tensor_map = {}  
    
    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype, sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
        if not model._input_layers or len(input_tensors) != len(model._input_layers):
            raise ValueError('Incorrect number of input layers')

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in range(len(model._nodes_by_depth) - 1, -1, -1):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer

            if layer not in layer_map:
                new_layer = model_from_config(layer.get_config())
                layer_map[layer] = new_layer
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
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                if has_arg(layer.call, 'mask') and 'mask' not in kwargs:
                    kwargs['mask'] = computed_masks

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))

                for x, y, mask in zip(node.output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
```

Now, the corrected function should handle the scenario where all output tensors are properly computed and added to the `tensor_map`, resolving the issue mentioned in the failing test and the GitHub report.