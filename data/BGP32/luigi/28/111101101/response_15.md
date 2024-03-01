### Bug Explanation
The bug in the `table_exists` function arises from the way the function checks for the existence of tables in a Hive database. 

In the `table_exists` function:
- When `partition` is `None`, the function constructs a Hive command using the provided `table` and `database` variables, runs the command, and checks if the `table` exists in the output.
- When `partition` is not `None`, the function constructs a different Hive command using the `database`, `table`, and the partition specification from the `self.partition_spec(partition)` call, and checks the existence of the table based on the command output.

The bug occurs because the function relies solely on the existence of some output (not empty) to determine if a table exists or not. This approach is flawed because different outputs may not necessarily indicate the existence of the table.

### Bug Fix Strategy
To fix the bug, we should modify the function to explicitly check the output for the presence of the exact table name in both cases (with and without partitions). This change will ensure that the function accurately determines the existence of the table based on the output of the Hive commands.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        if stdout:
            return table in stdout.split('\n')
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        if stdout:
            return table in stdout.split('\n')
        else:
            return False
```

By splitting the `stdout` output on newlines and explicitly checking if the `table` is present in the list of tables or partitions, the function will accurately determine the existence of the table and pass the failing test cases.