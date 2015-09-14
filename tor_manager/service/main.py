#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-



import tornado.web
import json, logging, types, time, urllib2
from tor_manager.util.config import Config
from tor_manager.util.httpclient import HttpClient
from tor_manager.util.httpresponse import Response as Resp, ResponseCode as RespCode

class MainHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.Resp = Resp()
		
	def get(self):
		ori = self.get_argument("ori", None)
		if ori == None:
			self.render("index.html")
			return
			
		if ori == "book":
			self.render("bookmanage/addbook.html")
			return
			
		if ori == "reader":
			self.render("readermanage/addreader.html")
			return
			
	def post(self):
		data = self.request.body
		logging.info("receive data: %s", data)
		username = self.get_argument("username", None)
		password = self.get_argument("password", None)
		logging.info("user logging! username: %s, password: %s", username, password)
		
		self.render("tor_main.html", username = username)
