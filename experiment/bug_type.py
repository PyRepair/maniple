from typing import List, TypedDict


BugInfo = TypedDict('BugInfo', {
    'id': int,
    'fix_commit_link': str,
    'buggy_commit_link': str
})


ProjectInfo = TypedDict('ProjectInfo', {
    'project': str,
    'bugs': List[BugInfo]
})


Features = TypedDict('Features', {
    'class_definition': None,
    'variable_definitions': None,
    'error_message': str,
    'stack_trace': None,
    'test_code': str,
    'raised_issue_description': str
})


BuggySnippet = TypedDict('BuggySnippet', {
    'filename': str,
    'source_code': str
})


BugsData = TypedDict('BugsData', {
    'id': int,
    'buggy_code_blocks': List[BuggySnippet],
    'features': Features
})


ProjectData = TypedDict('ProjectData', {
    'project': str,
    'bugs': List[BugsData]
})