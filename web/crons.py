#!/usr/bin/python3
# from django_cron import CronJobBase, Schedule
from . import views
from api import models
from datetime import datetime as dt
# class MyCronJob(CronJobBase):
# 	RUN_EVERY_MINS = 1 # every 2 hours

# 	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
# 	code = 'buscador.my_cron_job'    # a unique code

# 	def do(self):	
# 		views.updateAllItems(True)
# 		pass    # do your thing here

def my_scheduled_job():
	print("###CRON JOB###")	
	print(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
	lugares = models.Lugar.objects.filter(nuevo=False)
	for lugar in lugares:
		views.generar_cobranza(lugar.id)
	pass