### Bug Explanation
The bug in the `table_exists` function arises from the condition checking for the presence of the table in the output of `run_hive_cmd`. Specifically, the bug occurs in the comparison of the table name with the entire stdout output, which causes incorrect results when the table name is a subset of the output.

### Bug Fix Strategy
To fix the bug, we need to make sure that the comparison of the table name with the stdout output is done correctly, considering the possibility of line-separated multiple tables in the output. We can split the stdout into lines and then check if the table name exists in any of those lines.

### Corrected Code
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and any(table in line for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` on the newline character and then checking if the `table` exists in any of those lines, we ensure that the function correctly determines the existence of the table in the Hive output. This correction should address the bug and make the `table_exists` function behave as expected in all provided test cases.