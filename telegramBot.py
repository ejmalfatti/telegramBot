#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
###################################################################################
# Bot de Telgram que hace varias cosas, como informar la temperatura del Raspberry Pi y el clima (pronostico)
# Autor: Emanuel Malfatti 
# E-mail: ejmalfatti@outlook.com
# GitHub: https://ejmalfatti.github.io
# Licencia: GPLv3
###################################################################################

import telebot 
from telebot import types 
import time 
import random
import datetime
import token
import subprocess 
import os
import commands
import sys
from pyql.weather.forecast import Forecast
#import RPi.GPIO as GPIO


TOKEN = 'TOKEN' #Nuestro token del bot
 
bot = telebot.TeleBot(TOKEN)

#############################################
def listener(messages):
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text':
            print "[" + str(cid) + "]: " + m.text
 
bot.set_update_listener(listener)
#############################################


def mensaje(messages):
	for m in messages: 	
		uid = m.from_user.id
		if m.text == "Clima":
			cid = m.chat.id
			woeid = 91862968
			forecast = Forecast.get(woeid=woeid, u="c")
			ciudad = forecast.location.city
			region = forecast.location.region
			pais = forecast.location.country
			CIUDAD = ("Condiciones del clima en {0},{1}, {2}.\n".format(ciudad, region, pais))
			DATE = ("Fecha: {0}".format(forecast.item.condition.date))
			TEMP = ("Temperatura: {0}º {1}".format(forecast.item.condition.temp, forecast.units.temperature))
			CODE = ("Condición: {0} ({1})".format(forecast.item.condition.text, forecast.item.condition.code))
			CADENA = "{0}{1}\n{2}\n{3}".format(CIUDAD,DATE,TEMP,CODE)
			bot.send_message( cid, CADENA)

bot.set_update_listener(mensaje)


def mensaje(messages):
	for m in messages: 	
		uid = m.from_user.id
		if m.text == "Luz on":
			cid = m.chat.id
			bot.send_message( cid, "Luz encendida")

bot.set_update_listener(mensaje)


@bot.message_handler(commands=['luzon']) 
def command_ayuda(m): 
	uid = m.from_user.id
	cid = m.chat.id 
#	bot.send_message( cid, pedro)
	bot.send_message( cid, "Luz on")


@bot.message_handler(commands=['help']) 
def command_ayuda(m): 
	uid = m.from_user.id
	cid = m.chat.id 
#	bot.send_message( cid, pedro)
	bot.send_message( cid, "Comandos Disponibles: /help, /temp, /df, \"Clima\", \"Luz on\" ")


@bot.message_handler(commands=['temp'])
def command_temp(m):
	cid = m.chat.id
	#temp = os.system('sudo /opt/vc/bin/vcgencmd measure_temp')
	TEMP = commands.getoutput('sensors')	
	bot.send_message(cid, TEMP)
	

@bot.message_handler(commands=['df'])
def command_temp(m):
	cid = m.chat.id
	#temp = os.system('sudo /opt/vc/bin/vcgencmd measure_temp')
	SIZE = commands.getoutput('df -h')	
	bot.send_message(cid, SIZE)


#############################################
bot.polling(none_stop=True)
