### Analysis:
1. The `ValueError` is raised during the test run due to an `AssertionError: Could not compute output` within the `_clone_functional_model` function.
2. The function aims to clone a functional `Model` instance while creating new layers and weights without sharing existing ones.
3. The bug likely occurs due to the mismatch between the expected and actual output tensors during the cloning process. The error message mentions that the output tensor cannot be computed, indicating an issue in handling the layers during cloning.
4. To resolve the bug, ensure that the clone operation correctly maps the input and output tensors, especially in cases involving multiple outputs from a layer.
5. The corrected version must handle the layer cloning and input/output tensor mapping properly to avoid the error message.

### Bug Fix:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)

    layer_map = {}  
    tensor_map = {}  
    input_layers = []  # Updated
    if input_tensors is None:
        input_tensors = [] 
        input_layers = model._input_layers  # Fixed line
        for layer in input_layers:
            input_tensor = Input(batch_shape=layer.get_output_at(0).get_shape().as_list(),
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  

    for depth in sorted(model._nodes_by_depth.keys(), reverse=True):
        for node in model._nodes_by_depth[depth]:
            if node.outbound_layer not in layer_map:
                new_layer = node.outbound_layer.__class__.from_config(node.outbound_layer.get_config())
                layer_map[node.outbound_layer] = new_layer

            reference_input_tensors = node.input_tensors
            reference_output_tensors = node.output_tensors

            computed_data = []
            for x in reference_input_tensors:
                if x in tensor_map:
                    computed_data.append(tensor_map[x])

            if len(computed_data) == len(reference_input_tensors):
                kwargs = node.arguments or {}
                computed_tensors = [x[0] for x in computed_data]
                output_tensors = to_list(node.outbound_layer(computed_tensors, **kwargs))

                for x, y in zip(reference_output_tensors, output_tensors):
                    tensor_map[x] = (y, None)

    output_tensors = [tensor_map[t][0] for t in model.outputs]  # Updated

    return Model(inputs=[tensor_map[x][0] for x in model.inputs], outputs=output_tensors, name=model.name)
```

By updating the input layer handling, ensuring proper mapping of input/output tensors, and addressing the layer cloning process, the corrected function should resolve the `Could not compute output Tensor` error.