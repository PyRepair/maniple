### Summary of Discrepancy
The discrepancy in the failing test cases seems to be related to how the function handles the vmin and vmax values, as well as the calculation of the maxabsvalue.

In the third test case, the function fails to correctly handle the scenario where vmin is greater than vmax, resulting in the "swapped" variable not being set to True and the "maxabsvalue" not being calculated correctly.

This discrepancy suggests that the core logic of the function does not properly handle the scenario where the vmin and vmax values are swapped. This issue likely leads to incorrect results and failing test cases.