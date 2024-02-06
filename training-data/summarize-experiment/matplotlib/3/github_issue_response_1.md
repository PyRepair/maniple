## Summary
The GitHub issue details a bug where markers are not appearing as hollow when using `ax.scatter()` and customizing the MarkerStyle by setting `fillstyle` parameter to 'none'. The user's expectation is to have hollow markers, but the current implementation does not reflect that.

## Reproduction Steps
1. Import necessary libraries: 
   ```python
   from matplotlib import pyplot as plt
   from matplotlib import markers
   import numpy as np
   ```
2. Generate random data for scatter plot: 
   ```python
   xy = np.random.rand(10, 2)
   ```
3. Create a new figure and axis:
   ```python
   fig, ax = plt.subplots()
   ```
4. Customize MarkerStyle to set markers as hollow:
   ```python
   style = markers.MarkerStyle(marker='o', fillstyle='none')
   ```
5. Use `ax.scatter()` to plot the scatter plot with custom MarkerStyle:
   ```python
   ax.scatter(xy[:, 0], xy[:, 1], marker=style)
   ```
6. Display the plot:
   ```python
   plt.show()
   ```

## Expected Outcome
The expected outcome is to have a scatter plot with hollow markers based on the customized MarkerStyle with `fillstyle='none'`.

## Current Outcome
The current outcome does not match the expectation, as the markers are not appearing as hollow despite setting the `fillstyle` parameter to 'none'. This leads to the bug in the visualization.

## Additional Notes
The issue suggests a potential discrepancy between the intended usage of custom MarkerStyle with `fillstyle='none'` and the actual behavior observed in the scatter plot. Further investigation is required to identify the root cause and devise an appropriate solution for this bug.