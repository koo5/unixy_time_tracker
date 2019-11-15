#!/usr/bin/env python3


import sys
import psycopg2
from collections import defaultdict, namedtuple
import datetime
import subprocess

Rec = namedtuple('Rec', ['action', 'ts', 'desc'])

def make_conn():
	conn = psycopg2.connect("dbname=hours user=hours password=hours")
	return conn

def store(action, misc):
	sql = """INSERT INTO hours(ts,action,misc) VALUES(CURRENT_TIMESTAMP, %s, %s);"""
	with make_conn() as conn:
		with conn.cursor() as curs:
			curs.execute(sql, (action, misc))

def report0():
	sql = """SELECT * FROM hours ORDER BY ts;"""
	with make_conn() as conn:
		with conn.cursor() as curs:
			curs.execute(sql)
			for r in curs.fetchall():
				yield Rec(*r)


def report1():
	runs = []
	on = False
	task = '???'
	last_start = None

	def start(r):
		nonlocal on, last_start
		if not on:
			on = True
			last_start = r.ts

	def stop(r):
		nonlocal on
		if on:
			on = False
			last_run = r.ts - last_start
			if len(runs) and runs[-1][0] == task:
				runs[-1] = (task, runs[-1][1] + [last_run])
			else:
				runs.append((task, [last_run]))

	for r in report0():
		#print (r)
		if r.action == 'on':
			start(r)
		if r.action == 'off':
			stop(r)
		if r.action == 'desc':
			if on:
				stop(r)
				task = r.desc
				start(r)
			else:
				task = r.desc
	#print()
	was_on = on
	now = datetime.datetime.now(datetime.timezone.utc)
	stop(Rec('off', now, ''))
	return runs, was_on

def report2():
	result = []
	runs, on = report1()
	for (task,durations) in runs:
		result.append((task, sum(durations, datetime.timedelta())))
	return result, on


def dump2():
	lines,on = report2()
	for (task,duration) in lines:
		print (str(duration), task)
	return on

#def report3():
#	runs = defaultdict(list)

arg = sys.argv[1]
if arg in ['on', 'off', 'desc']:
	misc = ''
	if arg == 'desc':
		misc = sys.argv[2]
	if arg == 'on' and len(sys.argv) > 2:
		store('desc', sys.argv[2])
	store(arg, misc)
	if arg in ('on','off'):
		subprocess.check_call(['notify-send', 'unixy_time_tracker', arg])
	if arg == 'on':
		subprocess.check_call(['/home/koom/unixy_time_tracker/tt_beep'])
elif arg == 'dump0':
	for r in records():
		print(r)
elif arg == 'dump1':
	for i in report1()[0]:
		print (i)
elif arg == 'dump2':
	dump2()
elif arg == 'info':
	if dump2():
		print('running.')
	else:
		print('stopped.')
elif arg == 'is_on':
	if report2()[1]:
		print('yep')
		exit(0)
	else:
		print('no')
		exit(1)
else:
	raise('unknown command')
