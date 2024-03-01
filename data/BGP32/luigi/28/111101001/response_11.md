The bug in the `table_exists` function lies in the condition checking for the presence of the table name in the output of the `run_hive_cmd` function. The current implementation checks if the table name is an exact match in the output, causing issues when there is additional content in the output after the table name.

To fix this bug, we need to modify the condition to check if the table name is present in the output, regardless of the exact match. Here's the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and any(table in line for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

This corrected version ensures that the function correctly detects the existence of the table by checking if the table name is present in each line of the output. This change will allow the function to pass the failing tests provided.