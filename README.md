# Daily summary Part

## 29/08/23
Add example demonstration in Daily summary, which focus on critical features to justify why and when they are 'important'. Develop tools that can automatically generate templates and pass them into LLM to generate patches. Currently it's still in a broken state and in developing, so I push an example input jason file for cookiecutter project to give a overview.

Example demonstration for test error:
For some simple bugs, they can be fixed by making some small changes following the language syntax, in this case even you don't use test error you can still get the correct fix patch. These bugs are quite similar to bugs in QuixBugs datasets, you can see an example there https://github.com/HuijieYan/LLM-prompt-data-for-APR/blob/master/PySnooper/3/prompt.md

For more bugs, test error can provide a general repair direction by value assertion and stack trace. Value assertion can provide input-output value pair to constrain return value. For example: https://github.com/HuijieYan/LLM-prompt-data-for-APR/blob/master/cookiecutter/2/Answer.md.

Stack Trace can be used to locate relevant code snippets, sometimes these snippets can provide definition to supplement variable or class definition. Although there is still not a succeed example fix patch rn, while doing the experiment i can see function definition or comment contains useful infomation 'occasionally'.

Example demonstration for raised issue description:
Raised issue description can be treated as alternative for bug report. Ideally, a mature project should have a bug report that gives you detailed information about each bug. 

Unfortunately, serveral projects in BugsInPy that i've checked so far have no bug report, everytime the developer fixed a bug they just closed a issue raised. Although issue description are very unclear and misleading 'occasionally', for example in httpie bug 4: https://github.com/httpie/cli/issues/235.

But in most time the 'title' summary is concise, and the 'content' gives a correct fix direction or a specific description when the bug happened or how to reproduce the bug.

Note that there are still some bugs (may be 20%) are found and fixed by the auther, so in the fix commit you can't find raised issue, and you also can't find a bug report as said before.

## 22/08/23
Mention: Instructions in the bugsinpy database are not available, and pyrepair support for bugsinpy is still under development. I'm trying to run tests manually direct from a specific project, so for some bugs i use manual test error, cause still need some time to set up the testing env.

Test error and raised issue description are crucial for LLM to understand how to correct bugs, yet the raised issue description of many bugs is very vague and misleading.

## 18/08/23

Update prompt for httpie 2,3,4.

Adding 'Apostrophe' to constrains word instructs LLM to focus on them, reduces the probability of generated fix patche that break already passed tests.

Again for short and isolated program, in most cases, bugs can be resolved simply by making changes that follow language syntax even you don't provide 'test error'.
Programs that are more difficult to fix often require an understanding of the author's needs. If the author already wrote fix description in fix commit while fixing the bug, the description can be passed to LLM as a repair requirement to increase the probability of successful repair. In addition, for such bugs, if the definition of the relevant parameters used in repair is avaiable, the probability of successful repair also increases, which implicitly provide a repair options for LLM.


## 17/08/23

Mention: Although BugsInPy has the 'record of fail test' for every bug, which indicate the test file name and the specific failed test in this file, but lots of test file are already deleted or modified by the author. Unlike the fix (buggy) commit which has a id to track the fixed (buggy) version, the deleted test files or original test files can't be found. Right now i still can't find a way to get exactly project version that BugsInPy, so current experiment only performed directly by cloning and running tests from project's repo.

Current prompt feature includes 'Bug location', 'test error and related info', 'variable or class definition', 'code comment', 'fix commit of the project author', and a description sentence forces the generated fixed patch to be drop-in replacement.

For short and isolated program, in most cases, bugs can be resolved simply by making changes that follow language syntax. However, in some cases, generating the correct patch needs to follow the author's idea or requirement, which is more common in non-isolated program.

Sometimes, buggy commit and fix commit can give a description of the bug and fix requirements, or code comment can gives the functionality for function, class, variable, snippet. Unfortunately in most time, these feature are absent or descriptions don't have a high correlation about fix requirement.

# LLM-prompt-data-for-APR Spreadsheet

[Result Spreadsheet (Google Sheet)](https://docs.google.com/spreadsheets/d/1XYWpsnhUVL7p8IS9K6jc1vadp2cirJ5O7VIA-F8hCH8/edit?usp=sharing)
