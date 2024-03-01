The bug in the provided function `table_exists` lies in the formatting of the `stdout` variable assignment within the `else` block. The bug is caused due to the incorrect formatting of the Hive command which is needed to check the existence of a table with a specified partition.

In the buggy function, the formatting of the Hive command in the else block is incorrect. The `%s` placeholders are not correctly used with the variables `database`, `table`, and `self.partition_spec(partition)`. This causes a failure in executing the Hive command and hence leads to incorrect results being returned by the function.

To fix this bug, we need to ensure that the Hive command string is correctly formatted with the appropriate values of `database`, `table`, and `self.partition_spec(partition)`.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

With this correction, the Hive command string is formatted correctly using `.format()` method, ensuring that the values of `database`, `table`, and `self.partition_spec(partition)` are inserted into the command string appropriately, fixing the bug.