### Bug Explanation
The bug in the `table_exists` function is likely due to how the function checks the presence of the table in the output from the `run_hive_cmd` command. In the first branch of the `if` statement, the function checks if the table name is present in the output, but in the second branch, it only checks if the output is not None. This inconsistency leads to incorrect results and failing tests.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function checks for the exact table name in the output in both branches of the `if` statement. We should also consider trimming any extra spaces or newlines in the output to accurately match the table name provided.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.strip()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout and table in stdout.strip()
``` 

By modifying the function to check for the presence of the exact table name in the trimmed output in both branches, we ensure consistent behavior and accurate table existence checks.