### Bug Explanation:
The bug in the `table_exists` function arises from the logic used to check if a table exists in the Hive database. In the `if partition is None` block, the function checks if the table exists based on whether the table name is present in the output received after running the hive command. However, this logic is flawed because the function only checks if the table name is present in the output, which can lead to false positives (as seen in the failing tests).

### Bug Fix Strategy:
To fix the bug, the function should parse the output from the `run_hive_cmd` function more accurately to ensure that the table name appears in a stand-alone line and is not part of another string. This will prevent false positives and accurately determine if the table exists in the Hive database.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = stdout.split()
        return table in tables
    else:
        stdout = run_hive_cmd('use {0}; show table {1} partition ({2});'.format(database, table, self.partition_spec(partition)))
        return stdout.strip() != ''
```

By splitting the output on whitespace in the `if partition is None` block and checking the presence of the table name in the list of tables, we ensure an exact match. In the `else` block, we utilize `strip()` to ensure that the output is not just whitespace, which helps to accurately determine if the table exists in the specified partition. This corrected logic should pass the failing tests.