### Analyzing the buggy function and GitHub issue
1. The buggy function `table_exists` in the `HiveCommandClient` class checks if a table exists in a Hive database by running a Hive command and examining the output. The issue arises when the table names are case-sensitive, leading to test failures.
2. The related function `run_hive_cmd` is used to execute Hive commands.
3. The GitHub issue #896 highlights the need to make `table_exists` case insensitive to handle situations where table names have different cases.
4. To fix the bug, we need to modify the comparison logic in the `table_exists` function to ensure case insensitivity.
5. A corrected version of the function is provided below to address the case sensitivity issue.

### Suggested Fix Strategy
To address the case sensitivity problem, we should convert both the table name and the output from Hive to lowercase before comparing them. This will ensure that the comparison is case insensitive.

### Corrected Version of the Buggy Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        return stdout and table.lower() in map(str.lower, stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

### Explanation of Correction
- In the corrected version, `table.lower()` is used to convert the table name to lowercase for case insensitivity.
- Similarly, by using `map(str.lower, stdout.split('\n'))`, we convert each table name in the stdout to lowercase.
- This approach ensures that both sides of the comparison are in lowercase, resolving the case sensitivity issue reported in the GitHub issue.

By making these modifications, the `table_exists` function now compares table names in a case-insensitive manner, addressing the test failures caused by case differences in table names.