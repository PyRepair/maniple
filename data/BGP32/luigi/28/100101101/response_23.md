### Bug Explanation:
The bug in the `table_exists` function lies in the condition for checking whether the table exists. The function checks if the table name is present in the output obtained from the `run_hive_cmd` function. However, the current implementation does not handle cases where the table name might be a substring of another table name present in the output. This leads to incorrect results, as shown in the failing test cases.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the function correctly identifies the table name in the output and does not mistake it for a substring of another table name. One approach is to split the output by newline characters and loop through each line to check if the table name is an exact match. This way, we avoid matching partial table names.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        tables = stdout.split('\n')
        return any(t.strip() == table for t in tables)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

### Summary:
The corrected version of the function now splits the output into lines and checks for an exact match of the table name in each line, avoiding issues with substring matching. This modification ensures that the function behaves as expected and passes the failing test cases.