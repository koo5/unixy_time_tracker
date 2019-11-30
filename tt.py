#!/usr/bin/env python3

import os
import sys
import psycopg2
from collections import defaultdict, namedtuple
import datetime
import subprocess

Rec = namedtuple('Rec', ['action', 'ts', 'desc'])

def print_rec_nice(r):
	print(str(r.ts), r.action, r.desc)

def make_conn():
	conn = psycopg2.connect("dbname=hours user=hours password=hours")
	return conn

def store(action, misc):
	sql = """INSERT INTO hours(ts,action,misc) VALUES(CURRENT_TIMESTAMP, %s, %s);"""
	with make_conn() as conn:
		with conn.cursor() as curs:
			curs.execute(sql, (action, misc))
	print('db updated.')

def report0():
	sql = """SELECT * FROM hours ORDER BY ts;"""
	with make_conn() as conn:
		with conn.cursor() as curs:
			curs.execute(sql)
			for r in curs.fetchall():
				yield Rec(*r)


def report1(verbose = False):
	runs = []
	on = False
	task = '???'
	last_start = None
	last_tick = None
	use_ticks = False

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

	def get_now():
		return datetime.datetime.now(datetime.timezone.utc)

	def fake_stop(at_time):
		stop(Rec('off', at_time, ''))

	def check_last_tick(at_time):
		nonlocal last_tick, on
		if use_ticks and on:
			if last_tick == None:
				raise('wtf')
			if at_time - last_tick > datetime.timedelta(minutes=5):
				if verbose:	print('lack of ticks, stopping')
				fake_stop(last_tick)

	for r in report0():
		if verbose: print_rec_nice(r)
		check_last_tick(r.ts)
		if r.action == 'on':
			start(r)
			last_tick = r.ts
		elif r.action == 'off':
			stop(r)
		elif r.action == 'desc':
			if on:
				stop(r)
				task = r.desc
				start(r)
				last_tick = r.ts
			else:
				task = r.desc
		elif r.action == 'tick':
			if not use_ticks:
				use_ticks = True
				if verbose: print('activating ticks processing')
			last_tick = r.ts
		else:
			raise(Exception('unexpected action:%s'%[r.action]))
	#print()
	was_on = on
	fake_stop(get_now())
	return runs, was_on

def report2():
	result = []
	runs, on = report1()
	for (task,durations) in runs:
		result.append((task, sum(durations, datetime.timedelta()))) #start=
	return result, on


def dump2():
	lines,on = report2()
	for (task,duration) in lines:
		print (str(duration), task)
	return on

def dump3(do_print=True):
	lines,on = report2()
	output = defaultdict(datetime.timedelta)
	aliases = {
		'depreciation':'depreciation_ui',
		'open_sourcing':'cleanup, open-sourcing reorg',
		'code cleanup':'cleanup, open-sourcing reorg',
		'cleanup':'cleanup, open-sourcing reorg',
		'that_was_testrunner':'tests_framework',
		'prolog_stuff':'prolog_rdf_stuff',
		'depreciation_new':'depreciation_ui',
		# todo move 3h from livestock to tests_framework
	}
	for (task,duration) in lines:
		if task in aliases:
			task = aliases[task]
		output[task] += duration
	if do_print:
		for task,duration in output.items():
			print (str(duration), task)
	return output,on

def csv():
	print('#hours\ttask')
	lines,on = dump3(False)
	for task,duration in lines.items():
		#import IPython; IPython.embed()
		print(task, '\t', round(duration.total_seconds()/60/60, 1))

def noncritical_call(args):
	try:
		subprocess.check_call(args, timeout=5)
	except Exception as err:
		print("error: {0}".format(err))

def notify(text):
	ico = os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/ufo_by_telepatx_d2ne2p4-fullview2.ico')
	noncritical_call(['notify-send', '-i', ico, 'unixy_time_tracker', text])

def notify_running_change(on, arg):
	print (arg)
	start = arg == 'on'
	stop = not start
	
	if start and not on:
		msg = 'start'
	elif start and on:
		msg = 'already on'
	elif stop and not on:
		msg = 'already off'
	elif stop and on:
		msg = 'stop'
	notify(msg)

arg = sys.argv[1]
if arg in ['on', 'off', 'desc']:
	misc = ''
	if arg == 'desc':
		misc = sys.argv[2]
	if arg == 'on' and len(sys.argv) > 2:
		store('desc', sys.argv[2])
	old = dump2()
	store(arg, misc)
	if arg in ('on','off'):
		notify_running_change(old, arg)
	if arg == 'on':
		noncritical_call(['/home/koom/unixy_time_tracker/tt_beep'])
elif arg == 'dump0':
	for r in report0():
		print(r)
elif arg == 'dump0b':
	for r in report1(verbose=True):
		pass
elif arg == 'dump1':
	for i in report1()[0]:
		print (i)
elif arg == 'dump2':
	dump2()
elif arg == 'dump3':
	if dump2():
		print('running.')
	else:
		print('stopped.')
elif arg == 'info':
	if dump3()[1]:
		print('running.')
	else:
		print('stopped.')
elif arg == 'csv':
	csv()
elif arg == 'is_on':
	if report2()[1]:
		print('yep')
		exit(0)
	else:
		print('no')
		exit(1)
elif arg == 'is_on':
	if report2()[1]:
		print('yep')
		exit(0)
	else:
		print('no')
		exit(1)
elif arg == 'tick':
	if report2()[1]:
		print('yep')
		store('tick', '')
#elif arg == 'rename':
#	store('rename', '')

else:
	raise('unknown command')
