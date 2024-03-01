The issue with the `table_exists` function is that it is not correctly handling the return value from the `run_hive_cmd` function. The function is expecting a specific format for the output string in order to determine if the table exists or not. However, the parsing logic inside the function is incorrect, leading to incorrect results in the test cases.

### Bug Cause:
1. In the `table_exists` function, when no partition is provided, the function is trying to check if the table exists by searching for it in the output string. The check `return stdout and table in stdout` is not sufficient. It is only checking if `table in stdout`, but should also check for the presence of the database name in the output string.
2. When a partition is provided, the function constructs a command to show the partitions based on the database, table, and partition spec. The issue lies in the condition check after running the command. The function simply checks if `stdout` has any value but does not check for the specific output that indicates the existence of the partition.

### Fix Strategy:
1. Update the function to properly parse the output string returned by `run_hive_cmd` to check for the existence of the table in the specified database.
2. Modify the function to check for the presence of the partition spec in the output string when a partition is provided.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and '{0}.{1}'.format(database, table) in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            %s""" % (database, table, self.partition_spec(partition)))

        return stdout.strip() != ""
```

By making these modifications, the `table_exists` function should now correctly check for the existence of tables and partitions within the specified database, and the corrected version should pass the failing tests.