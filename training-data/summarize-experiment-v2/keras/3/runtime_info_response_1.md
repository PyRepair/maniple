The `_clone_functional_model` function is intended to clone a functional model instance, which creates new layers and new weights instead of sharing the weights of the existing layers. However, there are several issues in the code that need to be addressed in order to fix the bug.

1. The function is not properly handling the input_layers and nodes of the model, leading to incorrect mapping and duplication of layers.

2. The function is not correctly computing the output tensors for the cloned model, leading to unexpected behavior and potentially incorrect model outputs.

3. There are inconsistencies in the usage of `input_layers`, `input_tensors`, and `input_layers`, leading to incorrect caching and reuse of input layers.

To fix the bug, the function needs to be refactored to properly handle input layers and nodes, compute output tensors, and handle input tensors consistently. Additionally, the layer mapping and caching should be carefully managed to avoid duplication and retain the intended behavior of the cloned model.