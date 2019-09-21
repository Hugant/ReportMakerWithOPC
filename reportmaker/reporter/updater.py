from datetime import timedelta, datetime

import OpenOPC
import apscheduler
import pytz
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Report, Process

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def start():
	logging.info("Background scheduler on start")
	if scheduler.state == apscheduler.schedulers.base.STATE_RUNNING:
		scheduler.shutdown()

	scheduler.remove_all_jobs()
	reports = Report.objects.all()

	for report in reports:
		max_interval_time = datetime.now(tz=pytz.utc) - timedelta(minutes=report.interval_update)
		processes = Process.objects.all().filter(report=report.id)
		if (len(processes) == 0) or (processes.latest('date').date < max_interval_time):
			update(report.id)

		scheduler.add_job(update, 'interval', args=[report.id], minutes=report.interval_update, id=str(report.id))
		logging.info("Job will be created by id " + str(report.id))

	scheduler.start()
	logging.info("Background scheduler started")


def update(report_id):
	logging.info("Trying update report " + str(report_id))
	try:
		report = Report.objects.get(id=int(report_id))
		opc = OpenOPC.client()
		opc.connect('Matrikon.OPC.Simulation')
		logging.info("OPC connect completed")
		process = opc.read('Random.Int4')
		process_name = report.title_text + " - " + "process #" + str(Process.objects.all().filter(report=report.id).distinct().count())
		process = Process(
			report_id=report.id,
			name_text=process_name,
			state_text=process[1],
			ram_in_kb_int=process[0],
			date=timezone.now())
		process.save()
		report.process_set.add(process)
		logging.info("Process has been created by name " + process_name)
	except ObjectDoesNotExist:
		logging.info("Remove job from scheduler by id " + report_id)
		scheduler.remove_job(report_id)
