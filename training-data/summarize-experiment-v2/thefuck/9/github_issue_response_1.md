GitHub Bug Title:
Fix suggestions for git push -u origin

Description:
After the merge of #538, the suggestion for git push -u myfork is broken. The expected output should be git push --set-upstream josephfrazier tmp, but the current suggestion is hub push --set-upstream josephfrazier tmp -u josephfrazier. Need to fix this issue.