# GitHub Bug Issue Title
BUG/API: pivot_table with multi-index columns causing AttributeError

## Description
The output is asymmetrical between rows/columns and single/multi case. The error is caused by an AttributeError, resulting in no error for a symmetrical output between rows/columns and single/multi case.

## Additional Information
- Output of pd.show_versions(): pandas 0.20.2