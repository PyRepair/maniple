### Bug Analysis:
1. The function `_clone_functional_model` is designed to clone a functional Model instance by creating new layers and weights instead of sharing existing ones.
2. The error message indicates an AssertionError occurred while computing one of the model outputs during the execution of the function.
3. The error message specifically mentions that the output tensor `'swap_layer_1/Identity:0'` could not be computed.
4. The function is intended to create placeholders for input tensors if not provided and then iterate over the nodes in the model to clone the layers and compute the output tensors.

### Bug in the Code:
1. The function incorrectly checks the type of the input model, and the error occurs during the computation of the model outputs.
2. The function misses the creation of `input_layers` which should contain the placeholder input layers created during model initialization.
3. The function incorrectly maps the input tensors to their corresponding newly created input layers.

### Fix Strategy:
1. Ensure that the input model is an instance of a Functional Model.
2. Create `input_layers` and associate them with the corresponding placeholder input tensors.
3. Correctly map the input tensors to their respective newly created input layers to ensure proper computations later.

### The Corrected Function:
```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)

    layer_map = {}  # Cache for created layers.
    tensor_map = {}  # Map {reference_tensor: (corresponding_tensor, mask)}
    if input_tensors is None:
        # Create placeholders to build the model on top of.
        input_layers = []
        input_tensors = []
        for layer in model._input_layers:
            input_tensor = Input(batch_shape=layer.batch_input_shape,
                                 dtype=layer.dtype,
                                 sparse=layer.sparse,
                                 name=layer.name)
            input_layers.append(input_tensor)
            input_tensors.append(input_tensor)
            layer_map[layer] = input_tensor
    else:
        input_tensors = to_list(input_tensors)
        # Map input tensors to input layers
        for i, x in enumerate(input_tensors):
            if not K.is_keras_tensor(x):
                name = getattr(x, 'name', 'input_' + str(i))
                input_tensor = Input(tensor=x, name='input_wrapper_for_' + name)
                layer_map[x] = input_tensor
            else:
                layer_map[x] = x

    for x, y in zip(model.inputs, input_tensors):
        tensor_map[x] = (y, None)  # tensor, mask

    for depth in reversed(range(len(model._nodes_by_depth))):
        nodes = model._nodes_by_depth[depth]
        for node in nodes:
            layer = node.outbound_layer
            # Get or create the layer
            if layer not in layer_map:
                new_layer = layer.__class__.from_config(layer.get_config())
                layer_map[layer] = new_layer

            # Gather inputs to call the new layer
            reference_input_tensors = node.input_tensors

            # Compute output if all input tensors are available
            if all(x in tensor_map for x in reference_input_tensors):
                computed_data = [tensor_map[x] for x in reference_input_tensors]
                kwargs = node.arguments if node.arguments else {}
                output_tensors = to_list(layer([data[0] for data in computed_data], **kwargs))
                output_masks = to_list(layer.compute_mask([data[0] for data in computed_data], [data[1] for data in computed_data]))

                for x, (y, mask) in zip(node.input_tensors, zip(output_tensors, output_masks)):
                    tensor_map[x] = (y, mask)

    # Check computed model outputs and create a new model
    if not all(x in tensor_map for x in model.outputs):
        raise ValueError('Could not compute all model outputs')

    output_tensors = [tensor_map[x][0] for x in model.outputs]
    return Model(input_tensors, output_tensors, name=model.name)
``` 

This corrected function ensures that the model outputs are correctly computed by handling placeholder input layers creation and correctly mapping input tensors to their respective placeholder layers.