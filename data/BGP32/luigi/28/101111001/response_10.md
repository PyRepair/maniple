### Bug Explanation
The buggy function `table_exists` is failing because it is not handling the case-insensitivity of the table names correctly. The function checks if the given table name exists in the output received from the `run_hive_cmd` function. However, the comparison between the table name and the stdout is case-sensitive, leading to the test failures when different cases are used for the table name.

### Bug Fix Strategy
To fix the bug, the comparison between the table name and the stdout should be made case-insensitive. This can be achieved by converting both strings to lowercase before comparing them.

### Corrected Version of the Function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.strip, stdout.lower().split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

The corrected version of the function converts both the table name and the stdout to lowercase before comparison using the `lower()` function. This way, the comparison will be case-insensitive, and the function should now pass the failing tests.