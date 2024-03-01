### Bug Explanation
The bug in the `table_exists` function is related to how the function checks for the existence of a table in Hive. When the `table_exists` function is called with a table name that already exists in the database, it should return `True`, but the bug causes it to return `False`. This issue arises from the comparison logic in the function.

The function retrieves information about tables from Hive using the `run_hive_cmd` function. The bug occurs when the function checks if the table name is in the output received from `run_hive_cmd`. The comparison is incorrect, causing the function to return `False` even when the table exists.

### Bug Fix Strategy
To fix this bug, we need to correct the logic for comparing the received output with the table name to accurately determine if the table exists. The function should return `True` if the table name is found in the output and `False` otherwise.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))

        return bool(stdout)  # Corrected comparison to return True if stdout is not empty
``` 

By modifying the comparison to `return bool(stdout)`, we ensure that the function returns `True` when the table is found in the output from Hive. This correction aligns the function's behavior with the expected outcome, fixing the bug.