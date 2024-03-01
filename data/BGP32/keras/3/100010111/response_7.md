### 1. Issue Analysis
- **Buggy Function**: `_clone_functional_model`
- **Error Message**: `Could not compute output Tensor("swap_layer_1/Identity:0", shape=(?, 4), dtype=float32)`
- **Expected Input/Output**:
  - `model._input_layers`: `[<keras.engine.input_layer.InputLayer object at 0x7f8257dbf710>]`
  - `model.inputs`: `[<tf.Tensor 'input_1:0' shape=(?, 4) dtype=float32>]`
  - `model._nodes_by_depth`: `{0: [<keras.engine.base_layer.Node object at 0x7f8257dbaf90>], 1: [<keras.engine.base_layer.Node object at 0x7f8258161910>], 2: [<keras.engine.base_layer.Node object at 0x7f8257dbab90>]}`
  - `model.outputs`: `[<tf.Tensor 'swap_layer_1/Identity:0' shape=(?, 4) dtype=float32>, <tf.Tensor 'swap_layer_1/Identity_1:0' shape=(?, 4) dtype=float32>]`
  - `model.name`: `'model_1'`
- **GitHub Issue**: Related to error when using `clone_model` with `multi_gpu_model` and `cpu_relocation=True`.

### 2. Error Location
The error appears to stem from the inconsistency in handling multiple output tensors without mask support in the cloning process.

### 3. Bug Cause
- The bug occurs when the cloned layer does not support masks, leading to `output_masks` being set to `[None]` instead of `[None, None]`.
- This issue arises due to the input layer tensors being set incorrectly, which results in the failure to compute the model outputs.

### 4. Bug Fix Strategy
- Ensure that the cloned functional model correctly handles layers with multiple output tensors that do not support masks.
- Verify that all input tensors are passed through the cloning process accurately to compute the model outputs successfully.

### 5. Corrected Function
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)
    
    layer_map = {}  # Cache for created layers
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}

    if input_tensors is None:
        input_tensors = [Input(batch_shape=layer.batch_input_shape, dtype=layer.dtype,
                                sparse=layer.sparse, name=layer.name) for layer in model._input_layers]
    
    for original_tensor, cloned_tensor in zip(model.inputs, input_tensors):
        tensor_map[original_tensor] = (cloned_tensor, None)  # tensor, mask
    
    nodes_by_depth = sorted(model._nodes_by_depth.items(), reverse=True)
    for _, nodes in nodes_by_depth:
        for node in nodes:
            layer = node.outbound_layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer
                layer = new_layer
            else:
                layer = layer_map[layer]

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = [tensor_map[x] for x in reference_input_tensors if x in tensor_map]
            
            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments if node.arguments else {}
                computed_tensors, computed_masks = zip(*computed_data)
                output_tensors = to_list(layer(computed_tensors, **kwargs))
                output_masks = to_list(layer.compute_mask(computed_tensors, computed_masks))
                
                for output_tensor, output_mask, reference_output_tensor in zip(output_tensors, output_masks, reference_output_tensors):
                    tensor_map[reference_output_tensor] = (output_tensor, output_mask)

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    
    return Model(input_tensors, output_tensors, name=model.name)
```

By fixing the handling of input tensors, computing outputs for layers without mask support, and ensuring accurate mapping of tensor relationships during cloning, the corrected function should address the error experienced with `clone_model`.