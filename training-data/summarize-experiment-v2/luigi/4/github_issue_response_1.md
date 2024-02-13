GitHub Bug Title:
Redshift COPY fails in Luigi 2.7.1 when columns are not provided

Description:
When running Redshift COPY jobs with columns set to None to prevent table creation, it fails in Luigi 2.7.1 with a TypeError: object of type 'NoneType' has no len(). The issue appears to be related to a specific line in the code. A potential solution would be to make a change to that line.

Expected Output:
When using Redshift COPY jobs with columns set to None in Luigi 2.7.1, the operation should not fail with a TypeError related to the length of columns being None.

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0