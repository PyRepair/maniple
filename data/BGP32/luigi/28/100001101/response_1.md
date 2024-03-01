## Bug Explanation
The bug in the provided function `table_exists` lies in the comparison of the `table` variable and the command output stored in `stdout`. The function checks if the `table` exists in the output string `stdout`, which can lead to false positives. For example, if the `table` name is a substring of another table name in the output, the function wrongly concludes that the table exists.

## Bug Fix Strategy
To fix the bug, we need to modify the comparison logic to ensure that the exact table name is being checked for existence in the output. We can achieve this by splitting the output string by newline characters and then checking if the `table` exists as a separate item in the resulting list.

## Corrected Version of the Function

```python
# The corrected version of the function
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return True if stdout else False
```

This corrected version splits the `stdout` string by newline characters, creating a list of tables. Then, it checks if the `table` exists in this list, ensuring an exact match for table existence. It also simplifies the logic for the `partition` case by directly returning the boolean evaluation of the `stdout` variable.