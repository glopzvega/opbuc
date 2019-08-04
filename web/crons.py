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

def verificar_pago_cobranza():
	print("### CRON JOB VERIFICAR ###")	
	print(dt.now().strftime("%Y-%m-%d %H:%M:%S"))	
	views.verificar_pago_cobranza_method()	

def generar_cobranza():
	print("###CRON JOB GENERAR ###")	
	print(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
	views.generar_cobranza_method()	
	pass