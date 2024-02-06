Summary:
The bug occurs when using the pivot_table function with multi-index columns only, resulting in an AttributeError. This can be seen in the provided code samples where the pivot_table function returns an error when using it with a multi-index column structure. The expected output is to have no error and to maintain symmetry between rows/columns and single/multi cases.

Further investigation and debugging are required to address this issue, considering the specific version of the pandas library being used (pandas 0.20.2). The ultimate goal is to resolve the AttributeError and ensure that the pivot_table function operates as expected in all scenarios, including multi-index columns.

The bug description and code samples provide a clear illustration of the problem, allowing for detailed analysis and debugging efforts to rectify the issue.