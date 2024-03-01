The bug in the provided function `table_exists` lies in the construction of the query in the else block. The query being formed is incorrect due to a missing comma after `show partitions %s`. This is causing the query to be syntactically incorrect when executed.

To fix this bug, we need to modify the query in the else block to include the missing comma after `show partitions %s`.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s, partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

Now the query in the else block is correctly formatted with the comma after `show partitions %s`, fixing the bug that caused the query to be syntactically incorrect.