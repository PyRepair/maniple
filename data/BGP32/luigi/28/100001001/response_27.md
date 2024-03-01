### Bug analysis:
The function `table_exists` is designed to check if a table (or partition of a table) exists in a specified database by running a Hive command. The bug seems to be related to how the function handles the output (`stdout`) of the Hive commands.

In the first `if` block, the function checks if the table exists by searching for the table name in the output of the Hive command `show tables like "{table}"`. The bug here might be that it checks if `stdout` is not empty (`return stdout`) rather than checking if the table name is present in `stdout`.

In the else block, the function is trying to check if a table partition exists by running a Hive command `show partitions {table} partition ({partition_spec})`. The bug here could be related to how the function evaluates the presence of a partition in the output of this command.

### Bug fix strategy:
1. Update the logic in the first `if` block to check if the table name exists in the stdout rather than just checking if `stdout` is not empty.
2. In the else block, revise the logic to properly handle checking the presence of a table partition in the stdout.

### Corrected version of the function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout  # Corrected logic to check if table exists in the stdout
    else:
        partition_cmd = ' '.join(self.partition_spec(partition))
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".format(database, table, partition_cmd))

        return bool(stdout)  # Corrected logic to return True if stdout is not empty, False otherwise
```

This corrected version addresses the issues in both the `if` and `else` blocks to accurately check for the existence of tables and partitions in the specified database.