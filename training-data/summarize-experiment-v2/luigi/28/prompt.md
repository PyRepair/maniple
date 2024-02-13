Please fix the buggy function provided below and output a corrected version. When outputting the fix, output the entire function so that the output can be used as a drop-in replacement for the buggy version of the function.


# The source code of the buggy function
```python
# The relative path of the buggy file: luigi/contrib/hive.py



    # this is the buggy function you need to fix
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            if stdout:
                return True
            else:
                return False
    
```# The declaration of the class containing the buggy function
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """


# This function from the same file, but not the same class, is called by the buggy function
def run_hive_cmd(hivecmd, check_return_code=True):
    # Please ignore the body of this function

# This function from the same file, but not the same class, is called by the buggy function
def partition_spec(self, partition):
    # Please ignore the body of this function

# This function from the same file, but not the same class, is called by the buggy function
def partition_spec(self, partition):
    # Please ignore the body of this function

# This function from the same file, but not the same class, is called by the buggy function
def partition_spec(self, partition):
    # Please ignore the body of this function

    # This function from the same class is called by the buggy function
    def partition_spec(self, partition):
        # Please ignore the body of this function

# A failing test function for the buggy function
```python
# The relative path of the failing test file: test/contrib/hive_test.py

    @mock.patch("luigi.contrib.hive.run_hive_cmd")
    def test_table_exists(self, run_command):
        run_command.return_value = "OK"
        returned = self.client.table_exists("mytable")
        self.assertFalse(returned)

        run_command.return_value = "OK\n" \
                                   "mytable"
        returned = self.client.table_exists("mytable")
        self.assertTrue(returned)

        # Issue #896 test case insensitivity
        returned = self.client.table_exists("MyTable")
        self.assertTrue(returned)

        run_command.return_value = "day=2013-06-28/hour=3\n" \
                                   "day=2013-06-28/hour=4\n" \
                                   "day=2013-07-07/hour=2\n"
        self.client.partition_spec = mock.Mock(name="partition_spec")
        self.client.partition_spec.return_value = "somepart"
        returned = self.client.table_exists("mytable", partition={'a': 'b'})
        self.assertTrue(returned)

        run_command.return_value = ""
        returned = self.client.table_exists("mytable", partition={'a': 'b'})
        self.assertFalse(returned)
```


# A failing test function for the buggy function
```python
# The relative path of the failing test file: test/contrib/hive_test.py

    @mock.patch("luigi.contrib.hive.run_hive_cmd")
    def test_apacheclient_table_exists(self, run_command):
        run_command.return_value = "OK"
        returned = self.apacheclient.table_exists("mytable")
        self.assertFalse(returned)

        run_command.return_value = "OK\n" \
                                   "mytable"
        returned = self.apacheclient.table_exists("mytable")
        self.assertTrue(returned)

        # Issue #896 test case insensitivity
        returned = self.apacheclient.table_exists("MyTable")
        self.assertTrue(returned)

        run_command.return_value = "day=2013-06-28/hour=3\n" \
                                   "day=2013-06-28/hour=4\n" \
                                   "day=2013-07-07/hour=2\n"
        self.apacheclient.partition_spec = mock.Mock(name="partition_spec")
        self.apacheclient.partition_spec.return_value = "somepart"
        returned = self.apacheclient.table_exists("mytable", partition={'a': 'b'})
        self.assertTrue(returned)

        run_command.return_value = ""
        returned = self.apacheclient.table_exists("mytable", partition={'a': 'b'})
        self.assertFalse(returned)
```


Here is a summary of the test cases and error messages:

Based on the provided error messages, the assertion fails thereby causing the pytest to fail. The failing tests are intended to check the behavior of the 'table_exists' method. The error messages specify that after accessing the 'table_exists' method, the expected result is True, but instead, the result is False. Also, the initial mock command for 'run_hive_cmd' method is incorrect, which can infer to failing test as well. 

The refactored error message that skips the irrelevant parts would be as follows:
- The tests failed because a call to the 'table_exists' method returned an unexpected result: a False when it was expected to return True.

It leads to the conclusion that the code path taken corresponds to an else branch in the 'table_exists' method in the buggy file. Therefore, the conditional check seems to be faulty. The first troubleshooting step would be to investigate the 'table_exists' method in the buggy file and its else block to identify the root cause of the error.


## Summary of Runtime Variables and Types in the Buggy Function

The `table_exists` function is intended to check whether a table or partition exists in a Hive database. However, there are multiple bugs in the function that need to be fixed.

1. In the `if partition is None` block, the condition `stdout and table in stdout` is incorrect. If `stdout` is non-empty, it will always evaluate to `True`, but we need to check if the `table` is present in `stdout`. The correct condition should be `table in stdout`.

2. In the `else` block, the condition `if stdout` is also incorrect. The function should return `True` if the partition exists, which means `stdout` should not be empty. The condition should be `if stdout and table in stdout`.

3. In the `show partitions` command, the function should check if the specified partition exists, but it's currently just checking if the `stdout` is non-empty.

4. Because the case of the table name can vary, the function should be case-insensitive when checking for the existence of a table or partition. We can convert both the `table` and `stdout` to lowercase before performing the check.

To fix these bugs, the correct implementation for the `table_exists` function should be as follows:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return stdout and table.lower() in stdout.lower()
```


## Summary of Expected Parameters and Return Values in the Buggy Function

Based on the expected value and type of variables during the failing test execution, the buggy function is expected to query the hive database and return the result based on the input parameters. In the first case, the function should return `stdout` and check if the table exists in the database. In the second case, the function should return `stdout` and check if the table exists in the database. The buggy function is expected to correctly query the hive database and return the appropriate result based on the input parameters.


## Summary of the GitHub Issue Related to the Bug

GitHub Bug Title:
Hive table_exists should be case insensitive?

Description:
The table_exists function should be case insensitive when checking if a table exists in a hive database. The current implementation does not handle this and can cause tests to fail if the table names are defined as capitalized. This issue arises because hive is case insensitive and will return table names as lower case, causing the tests to fail. A fix is proposed to check the stdout against the table name in lower case to avoid case issues.

Expected Output:
The table_exists function should check for the existence of a table in a hive database in a case-insensitive manner.

Environment:
- luigi: 2.8.12
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0


1. Analyze the buggy function and it's relationship with the buggy class, related functions, test code, corresponding error message, the actual input/output variable information, the expected input/output variable information, the github issue.
2. Identify the potential error location within the problematic function.
3. Elucidate the bug's cause using:
   (a). The buggy function
   (b). The buggy class docs
   (c). The related functions
   (d). The failing test
   (e). The corresponding error message
   (f). Discrepancies between actual input/output variable value
   (g). Discrepancies between expected input/output variable value
   (h). The GitHub Issue information

4. Suggest possible approaches for fixing the bug.
5. Present the corrected code for the problematic function such that it satisfied the following:
   (a). Passes the failing test
   (b). Satisfies the expected input/output variable information provided
   (c). Successfully resolves the issue posted in GitHub

