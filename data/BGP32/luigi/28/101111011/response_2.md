### Bug Explanation:
The bug in the `table_exists` function is due to case sensitivity when checking if the table exists in the stdout returned from the `run_hive_cmd` function. The function needs to make the comparison case-insensitive to handle situations where the table name is defined differently in terms of case compared to what is returned by Hive.

### Bug Fix Strategy:
1. Modify the comparison to compare the lowercase version of the table name with the lowercase version of the stdout to ensure case insensitivity.
2. Update the function to handle the case where the table name is provided with mixed cases.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd(
            """use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By updating the `table_exists` function to compare the lowercase versions of the table name and the stdout, the function becomes case-insensitive when checking for the existence of tables. This modification addresses the issue reported in the GitHub bug reports.