You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

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

