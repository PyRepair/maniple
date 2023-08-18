# Daily summary Part

## 18/08/23

Update prompt for httpie 2,3,4.

Adding colon to constrains word instructs LLM to focus on them, reduces the probability of generated fix patche that break already passed tests.

Again for short and isolated program, in most cases, bugs can be resolved simply by making changes that follow language syntax even you don't provide 'test error'.
Programs that are more difficult to fix often require an understanding of the author's needs. If the author already wrote fix description in fix commit while fixing the bug, the description can be passed to LLM as a repair requirement to increase the probability of successful repair. In addition, for such bugs, if the definition of the relevant parameters used in repair is avaiable, the probability of successful repair also increases, which implicitly provide a repair options for LLM.


## 17/08/23

Mention: Although BugsInPy has the 'record of fail test' for every bug, which indicate the test file name and the specific failed test in this file, but lots of test file are already deleted or modified by the author. Unlike the fix (buggy) commit which has a id to track the fixed (buggy) version, the deleted test files or original test files can't be found. Right now i still can't find a way to get exactly project version that BugsInPy, so current experiment only performed directly by cloning and running tests from project's repo.

Current prompt feature includes 'Bug location', 'test error and related info', 'variable or class definition', 'code comment', 'fix commit of the project author', and a description sentence forces the generated fixed patch to be drop-in replacement.

For short and isolated program, in most cases, bugs can be resolved simply by making changes that follow language syntax. However, in some cases, generating the correct patch needs to follow the author's idea or requirement, which is more common in non-isolated program.

Sometimes, buggy commit and fix commit can give a description of the bug and fix requirements, or code comment can gives the functionality for function, class, variable, snippet. Unfortunately in most time, these feature are absent or descriptions don't have a high correlation about fix requirement.

# LLM-prompt-data-for-APR Spreadsheet

[Result Spreadsheet (Google Sheet)](https://docs.google.com/spreadsheets/d/1XYWpsnhUVL7p8IS9K6jc1vadp2cirJ5O7VIA-F8hCH8/edit?usp=sharing)
