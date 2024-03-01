The buggy function `table_exists` in the `HiveCommandClient` class of the `luigi.contrib.hive.py` file is not handling case sensitivity correctly when checking for table existence in Hive. The function needs to compare the table name in a case-insensitive manner.

### Bug Analysis:
The bug arises because the function is not converting the table name to lowercase before comparing it with the output from the Hive command, causing the tests to fail when the case of the table name does not match the case of the output.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the table name is converted to lowercase before comparing it with the output. This approach will make the table existence check case-insensitive.

### Corrected Version of the Function:
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition%s)""" % (database, table, self.partition_spec(partition)))

            return bool(stdout)
```

By converting both the table name and the stdout to lowercase, the function now performs a case-insensitive comparison. This corrected version should pass the failing tests and address the GitHub issue by making the `table_exists` function case insensitive.