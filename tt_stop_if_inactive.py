#!/usr/bin/env python3

import subprocess

if int(subprocess.check_output(['xprintidle'])) > 10 * 60 * 1000:
	if subprocess.call(['tt_is_on']) == 0:
		print('idle, turning tt off')
		subprocess.check_call(['tt', 'off'])

