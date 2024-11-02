#!/usr/bin/env python3
import json
import locale
import os
import sys
import psycopg2
from collections import defaultdict, namedtuple
import datetime
import subprocess

host = os.uname().nodename
Rec = namedtuple('Rec', ['action', 'ts', 'desc', 'xidle', 'host'])

DBG = os.environ.get('TT_DBG', False)

def print_rec_nice(r):
	print(str(r.ts), r.host, r.action, r.desc, r.xidle)

def make_conn():
	conn = psycopg2.connect("host=hours.internal dbname=hours user=hours password=hours")
	return conn

def store(action, desc=None, xidle=None):
	sql = """INSERT INTO hours(ts,action,host,"desc",xidle) VALUES(CURRENT_TIMESTAMP, %s, %s, %s, %s);"""
	with make_conn() as conn:
		with conn.cursor() as curs:
			curs.execute(sql, (action, host, desc, xidle))
	print('db updated.')

def report0():
	sql = """SELECT * FROM hours ORDER BY ts;"""
	with make_conn() as conn:
		with conn.cursor() as curs:
			curs.execute(sql)
			for r in curs.fetchall():
				#print('SELECT * r:', r)
				r = Rec(*r)
				#print('>>>:', r)
				yield r



def one(sql):
	with make_conn() as conn:
		with conn.cursor() as curs:
			curs.execute(sql)
			for r in curs.fetchall():
				return Rec(*r)


def report_current_desc():
	r = one("""SELECT * FROM hours WHERE action='desc' ORDER BY ts DESC LIMIT 1;""")
	if r:
		return r.desc
	return '?????'



def last_on():
	return one("""SELECT * FROM hours WHERE action='on' ORDER BY ts DESC LIMIT 1;""")



def get_now():
	return datetime.datetime.now(datetime.timezone.utc)



def report1(verbose = False):
	"""

replay all records and produce list of tuples (task, [durations])
we have to take into account that there are ticks coming from different machines, with different xidle values.
a run is an uninterrupted stream of activity, testified by ticks with some minimal xidle value.


	"""

	runs = []
	on = False
	task = '???'
	last_start = None
	last_activity = None


	def add_task_time(task, delta):
		if len(runs) and runs[-1][0] == task:
			runs[-1] = (task, runs[-1][1] + [delta])
		else:
			runs.append((task, [delta]))

	def start(r):
		nonlocal on, last_start
		if not on:
			on = True
			last_start = r.ts

	def stop(at_time):
		nonlocal on
		if on:
			if DBG:
				print('stop at %s'%at_time)
			on = False
			add_task_time(task, at_time - last_start)

	def check_activity():
		if on:
			if at_time - last_activity > datetime.timedelta(minutes=5):
				if DBG:
					print('idle, stopping at %s'%last_activity)
				stop(at_time)

	records = list(report0())

	#print('got records:')
	#for record in records:
		#print('record:', record)


	if len(records) == 0:
		return [], False, '??'

	if DBG:
		print('starting loop over minutes')

	at_time = records[0].ts
	at_record_index = 0

	was_on = False

	while True:
		#if DBG:
		#	print('last_activity:', last_activity)
		check_activity()

		if at_record_index >= len(records):
			print('end of records.')
			was_on = on
			stop(at_time)
			break

		# find all records that happened in the same minute
		records_in_minute = []
		while at_record_index < len(records) and records[at_record_index].ts < at_time + datetime.timedelta(minutes=1):
			records_in_minute.append(records[at_record_index])
			at_record_index += 1

		if len(records_in_minute) == 0:
			if DBG:
				print('no records in minute', at_time)
		else:
			if DBG:
				print('records_in_minute:')

			# process all records in the minute
			for r in records_in_minute:
				print_rec_nice(r)
				if r.action == 'on':
					last_activity = r.ts
					start(r)
				elif r.action == 'off':
					stop(at_time)
				elif r.action == 'desc':
					last_activity = r.ts
					task = r.desc
				elif r.action == 'tick':
					if not on:
						continue
					tick_last_activity = r.ts - datetime.timedelta(seconds=int(r.xidle))
					if last_activity is None or last_activity < tick_last_activity:
						last_activity = tick_last_activity
						if DBG:
							print('update last_activity to:', last_activity)
				elif r.action == 'error':
					print(r)
				elif r.action == 'add_hours':
					add_task_time(task, datetime.timedelta(hours=float(r.desc)))
				else:
					raise(Exception('unexpected action:%s'%[r.action]))

			check_activity()

		at_time += datetime.timedelta(minutes=1)

	return runs, was_on, task



def report2():
	result = []
	runs, on, _ = report1()
	#print(runs)
	#print(on)
	for (task,durations) in runs:
		result.append((task, sum(durations, datetime.timedelta()))) #start=
	#print(result)
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



def dump_csv(custom_locale=None):
	print('#task;hours')
	lines,_on = dump3(False)
	if custom_locale:
		locale.setlocale(locale.LC_ALL, custom_locale)
	for task,duration in lines.items():
		hours = duration.total_seconds()/60/60
		print(str(task)+';'+locale._format('%.1f', hours))



def noncritical_tt_script(script, args):
	return noncritical_call([tt_file(script)] + args)



def noncritical_call(args):
	try:
		subprocess.check_call(args, timeout=5)
	except Exception as err:
		print("error: {0}".format(err))



def tt_file(x):
	return os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/'+x)



def notify(text):
	ico = tt_file('ufo_by_telepatx_d2ne2p4-fullview2.ico')
	noncritical_tt_script('notify.sh', ['-i', ico, text])



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
		l = last_on()
		if l:
			d = datetime.timedelta(seconds=
			int((get_now() - l.ts).total_seconds()))
			#d.millis = 0
			runtime = str(d)
		else:
			runtime = '???'
		msg = 'stop after %s'%runtime
	msg += ', ' + report_current_desc()
	notify(msg)



def tick():
	try:
		xidle = int(subprocess.check_output([os.path.abspath(os.path.dirname(os.path.realpath(__file__))+'/tt_xprintidle')])) / 1000
		store('tick',  None, xidle)
		# if secs > 15 * 60:
		# 	print('idle, stopping')
		# 	do_stop('idle:%ss'%secs)
	except Exception as e:
		store('error', str(e))
		raise e



last_start = None



def do_start():
	arg = 'on'
	if len(sys.argv) > 2:
		store('desc', sys.argv[2])
	old = dump2()
	store(arg)
	notify_running_change(old, arg)
	noncritical_call(['/home/koom/unixy_time_tracker/tt_beep'])

def do_stop(note):
	arg = 'off'
	old = dump2()
	store(arg, note)
	notify_running_change(old, arg)

def do_desc():
	arg = 'desc'
	misc = sys.argv[2]
	store(arg, misc)

arg = sys.argv[1]
if arg == 'on':
	do_start()
elif arg == 'off':
	if len(sys.argv) > 2:
		note = sys.argv[2]
	else:
		note = ''
	do_stop(note)
elif arg == 'desc':
	do_desc()
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
	dump_csv()
elif arg == 'csv2':
	dump_csv('cs_CZ')
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
	# if report2()[1]:
	# 	print('yep')
		tick()
elif arg == 'add_hours':
	float(sys.argv[2])
	store('add_hours', sys.argv[2])
#elif arg == 'rename':
#	store('rename', '')

else:
	raise('unknown command')

# delete from hours where ts < '2020-05-01 00:00:14.05933+01';
# update hours set misc = 'documentation' where misc = 'docs';
