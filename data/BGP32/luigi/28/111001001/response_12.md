### Bug Explanation
The bug in the `table_exists` function lies in the condition to check if the given table exists. In the else part of the function, when a `partition` is provided, the query to check for the existence of the table is incorrect. The query includes both the table name and a partition specification, which may not correctly determine if the table exists.

### Bug Fix Strategy
To fix the bug, we need to modify the query when a partition is provided. The query should only check for the existence of the table without considering partition specifications.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
``` 

In the fixed version, when a partition is provided, we update the query in the else block to only check for the basic presence of the table without considering partition specifications. This modification ensures that the function correctly identifies the existence of the table regardless of the partition status.