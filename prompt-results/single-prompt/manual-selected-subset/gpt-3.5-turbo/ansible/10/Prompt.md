You need to fix a bug in a python code snippet.

The buggy source code is following:

    def remove(self, rule_type, rule_control, rule_path):
        current_line = self._head
        changed = 0

        while current_line is not None:
            if current_line.matches(rule_type, rule_control, rule_path):
                if current_line.prev is not None:
                    current_line.prev.next = current_line.next
                    current_line.next.prev = current_line.prev
                else:
                    self._head = current_line.next
                    current_line.next.prev = None
                changed += 1

            current_line = current_line.next
        return changed

Part of class definition for this function is:

    class PamdService(object):

        def __init__(self, content):
            self._head = None
            self._tail = None
            for line in content.splitlines():
                if line.lstrip().startswith('#'):
                    pamd_line = PamdComment(line)
                elif line.lstrip().startswith('@include'):
                    pamd_line = PamdInclude(line)
                elif line == '':
                    pamd_line = PamdLine(line)
                else:
                    pamd_line = PamdRule.rule_from_string(line)

                self.append(pamd_line)


And the raised issue description for this bug is 'pamd: Fix AttributeError when removing the first or last rule'.


You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.