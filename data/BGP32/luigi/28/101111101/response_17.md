## Bug Explanation
The bug in the `table_exists` function lies in the conditional check for the existence of the table. The function checks if the table string is present in the stdout returned by the `run_hive_cmd` function. However, in some cases, the table name might be a substring of another table name in the output causing false positives or false negatives in the check.

For example, if the `table` is `'mytable'` and the `stdout` is `'OK\nmytable1'`, the current implementation would incorrectly return `True`, although 'mytable' is not the exact match in the output.

## Bug Fix Strategy
To fix the bug, we need to modify the way we check the presence of the table name in the stdout. Instead of just checking for containment, we should validate that the table name is a full word in the output string. We can achieve this by adding word boundaries to the regex pattern for matching the table name.

## The Corrected Function
```python
import re

def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and re.search(r'\b'+re.escape(table)+r'\b', stdout)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

By using the regex pattern with word boundaries (`\b`) around the table name, we ensure that we are matching the exact table name in the output. This modification should fix the bug and make the function return the correct results based on the expected behavior.