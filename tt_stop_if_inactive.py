#!/usr/bin/env python3

import subprocess

try:
	secs = int(subprocess.check_output(['xprintidle'])) / 1000
	print('idle for %ss' % secs)
	if secs > 8 * 60:
		if subprocess.call(['tt_is_on']) == 0:
			print('idle, turning tt off')
			subprocess.check_call(['tt', 'off', str(secs) + 'secs idle'])
except e:
	subprocess.check_call(['tt', 'error', str(e)])
	raise e
