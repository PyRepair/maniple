The bug in the `table_exists` function is related to case sensitivity when checking for table existence. The function currently compares the table name directly with the output from Hive, leading to inconsistencies due to case differences. To address this, we need to ensure a case-insensitive comparison between the table name and the output from Hive.

Here is the corrected version of the `table_exists` function:

```python
# The relative path of the corrected file: luigi/contrib/hive.py

class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd(
                """use {0}; show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))
    
            return bool(stdout)
```

In the corrected version, we convert both the table name and the stdout to lowercase before comparison, ensuring a case-insensitive check for table existence.

This correction will address the issue reported in GitHub (Issue #896) and ensure that the `table_exists` function behaves as expected in both case-sensitive and case-insensitive scenarios.