GitHub Bug Title:
Copying PeriodIndex levels on MultiIndex loses weakrefs

Description:
When creating a MultiIndex from a PeriodIndex and checking if the levels are monotonic, it raises an error. This is because the weakly referenced PeriodIndex is dropped before it should be, causing the PeriodEngine to receive a None instead of the PeriodIndex.

Expected Output:
The check for monotonic levels should return True.

Environment:
- Python: 3.7.3.final.0
- pandas: 1.0.1
- numpy: 1.18.1
- scipy: 1.3.0