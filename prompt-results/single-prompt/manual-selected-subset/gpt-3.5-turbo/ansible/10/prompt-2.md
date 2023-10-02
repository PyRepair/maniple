You need to fix a bug in a python code snippet.

The buggy source code is following, and you should follow all specifications in comment if there exists comment:

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



The raised issue description for this bug is: 'pamd: Fix AttributeError when removing the first or last rule'.



You need to provide a drop-in replacement, with 'minimum changes to source code' that 'pass failed test' while 'won't affect other already passed tests'. And the fixed patch can be directly used in original project.