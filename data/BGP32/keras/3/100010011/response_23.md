### Analysis:
The function `_clone_functional_model` is responsible for cloning a functional `Model` instance. The error message indicates that the function is unable to compute the output of a layer during the cloning process.

#### Potential error locations:
1. The creation of placeholders when `input_tensors` is not provided.
2. The iteration over nodes in the reference model.
3. The handling of multiple outputs from a layer.

### Cause of the bug:
The error occurs because when using a layer with multiple outputs that does not support masks (such as the `Lambda` layer in the provided example), the function fails to compute the output masks correctly. This leads to an assertion error when trying to retrieve the output tensors.

### Strategy for fixing the bug:
1. Check and ensure proper handling of layers with multiple outputs and no mask support.
2. Update the logic for computing the output masks when dealing with multiple outputs.

### Updated corrected version of the function:

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K
from tensorflow.keras.engine.input_layer import Input
from tensorflow.keras.engine.engine import Node
from typing import List


def _clone_functional_model(model: keras.Model, input_tensors: List[tf.Tensor] = None) -> keras.Model:
    if not isinstance(model, keras.Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_tensors = [Input(batch_shape=layer.batch_input_shape,
                                dtype=layer.dtype,
                                sparse=layer.sparse,
                                name=layer.name) for layer in model._input_layers]
        for original, cloned in zip(model._input_layers, input_tensors):
            layer_map[original] = cloned

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
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

            computed_data = [(tensor_map[x][0], tensor_map[x][1]) for x in reference_input_tensors if x in tensor_map]

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors = [x[0] for x in computed_data]
                if len(computed_data) == 1:
                    computed_tensors = computed_tensors[0]
                if has_arg(layer.call, 'mask'):
                    if 'mask' not in kwargs:
                        kwargs['mask'] = [x[1] for x in computed_data if x[1] is not None]

                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = [layer.compute_mask(computed_tensors, mask) if mask is not None else None
                                for computed_tensors, mask in zip(computed_tensors, [x[1] for x in computed_data])]
                
                for x, y, mask in zip(reference_output_tensors, output_tensors, output_masks):
                    tensor_map[x] = (y, mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return keras.Model(input_tensors, output_tensors, name=model.name)
```

By updating the logic for computing the output masks and ensuring correct handling of multiple outputs from layers, this version of the function should fix the bug and pass the failing test.