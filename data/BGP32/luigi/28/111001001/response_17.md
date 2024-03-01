## Bug Explanation
The bug in the `table_exists` function lies in how the function is checking for the existence of a table in the Hive database. When `partition` is provided, the function is constructing a Hive command to check for partitions instead of directly checking for the table existence. This incorrect logic results in the function always returning `True` when a partition is specified, regardless of whether the table actually exists or not.

## Bug Fix
To fix the bug, we need to adjust the logic in the `table_exists` function to correctly check for the existence of the table based on the provided inputs. When `partition` is not None, we should only check for the table existence, and when `partition` is specified, we should check for the existence of the table partitions.

Here is the corrected version of the `table_exists` function:

```python
# this is the corrected version of the buggy function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return stdout is not None
```

With this correction, the function will now correctly determine the existence of a table based on the provided parameters.