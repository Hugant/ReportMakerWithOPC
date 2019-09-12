import OpenOPC
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Report, Process


scheduler = BackgroundScheduler()


def start():
	pass
	# if scheduler.state == apscheduler.schedulers.base.STATE_RUNNING:
	# 	scheduler.shutdown()
	#
	# scheduler.remove_all_jobs()
	# reports = Report.objects.all()
	# for report in reports:
	# 	print("Job will be created by id " + str(report.id))
	# 	scheduler.add_job(update, 'interval', args=[report.id], minutes=report.interval_update, id=str(report.id))
	#
	# scheduler.start()


# def update(report_id):
# 	try:
# 		report = Report.objects.get(id=int(report_id))
# 		opc = OpenOPC.client()
# 		opc.connect('Matrikon.OPC.Simulation')
# 		process = opc.read('Random.Int4')
# 		process_name = report.title_text + " - " + "process #" + str(Process.objects.all().filter(report=report.id).distinct().count())
# 		print(timezone.now())
# 		process = Process(
# 			report_id=report.id,
# 			name_text=process_name,
# 			state_text=process[1],
# 			ram_in_kb_int=process[0],
# 			date=timezone.now())
# 		process.save()
# 		print(process)
# 		report.process_set.add(process)
# 		print("created")
# 	except ObjectDoesNotExist:
# 		scheduler.remove_job(report_id)
