The bug in the `table_exists` function stems from the way the `run_hive_cmd` function is being used to execute the Hive command. The bug causes the `STDOUT` to be checked directly for the presence of the table name, which may not always work accurately.

To fix this bug:
1. We need to properly format the Hive command to check for the existence of the table in both cases when a partition is provided and when it is not.
2. After running the Hive command, we should check the output for the existence of the table name in a more robust way.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            table_list = stdout.split('\n')
            return table in table_list
        else:
            stdout = run_hive_cmd("""use {0}; show partitions {1} PARTITION ({2});""".format(database, table, self.partition_spec(partition)))
            table_list = stdout.split('\n')
            return table in table_list
```

In this corrected version, we split the STDOUT output by newline and check if the table name exists in the list of tables obtained from the Hive command output. This approach ensures a more reliable check for the existence of the table in Hive.