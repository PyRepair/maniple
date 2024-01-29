# Prompt Github issue info based facts

Your task is to determine whether the provided fact would be useful and relevant to fixing the buggy function.
Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
```python
def _recache(self):
    if self._marker_function is None:
        return
    self._path = _empty_path
    self._transform = IdentityTransform()
    self._alt_path = None
    self._alt_transform = None
    self._snap_threshold = None
    self._joinstyle = 'round'
    self._capstyle = 'butt'
    self._filled = True
    self._marker_function()

```

The github issue message is:
# A GitHub issue title for this bug
```text
The markers are not hollow when I use ax.scatter() and set markers.MarkerStyle()'s fillstyle to 'none'. My usage is wrong?
```

## The associated detailed issue description
```text
I want to set markers hollow. So I make a costomed markers.MarkerStyle and set the paramter fillstyle='none'. But I don't get what I want.

Code for reproduction

from matplotlib import pyplot as plt
from matplotlib import markers
import numpy as np
xy = np.random.rand(10, 2)
fig, ax = plt.subplots()
style = markers.MarkerStyle(marker='o', fillstyle='none')
ax.scatter(xy[:, 0], xy[:, 1], marker=style)
plt.show()
```



Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No."


