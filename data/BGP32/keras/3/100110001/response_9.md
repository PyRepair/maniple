### Analysis
The `_clone_functional_model` function is intended to clone a functional model instance by creating new layers and new weights instead of sharing the existing ones. The error occurs when trying to clone a model that is not a functional model (i.e., a Sequential model). The function should only work with instances of the `Model` class, not with `Sequential` instances.

### Bug Location
The bug is located in the error checking part where the function mistakenly raises an error if the model is an instance of `Sequential`.

### Bug Description
The bug occurs because the function does not properly handle the case when the model provided is an instance of `Sequential`, which should not be cloned using this function since it is not a functional model.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the error checking logic to handle the case when the model is an instance of `Sequential`. Instead of raising an error, we should gracefully handle the situation and provide a message indicating that a `Sequential` model cannot be cloned through this function.

### Corrected Function
Based on the analysis and bug description, the corrected function is provided below:

```python
def _clone_functional_model(model, input_tensors=None):
    if not isinstance(model, Model):
        raise ValueError('Expected `model` argument to be a `Model` instance, got ', model)
    
    if isinstance(model, Sequential):
        raise ValueError('Expected `model` argument to be a functional `Model` instance, got a `Sequential` instance instead:', model)
    
    # Rest of the function remains the same
    # No changes required after the error checking
```

By adding this check, the function will now properly handle the case when a `Sequential` model is provided as an input and will raise an appropriate error message. This correction should ensure that the function behaves as intended.