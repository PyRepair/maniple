The bug in the `table_exists` function is that it checks for the exact string match of the table name in the output of the `run_hive_cmd` function. This causes an issue when the table name appears in a line with other information such as in Case 2, where the output is `'OK\nmytable'`.

To fix this bug, we need to modify the condition to check if the table name appears as a separate word in the output. We can use regular expressions to accomplish this.

Here is the corrected version of the `table_exists` function:

```python
import re

def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and re.search(r'\b{}\b'.format(table), stdout)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

With this correction, the function will now correctly check if the table name appears as a separate word in the output, passing the failing test cases provided.