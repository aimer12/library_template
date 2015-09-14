#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import tornado.web
import json,logging,types,time,urllib2
from tor_manager.util.config import Config
from tor_manager.util.httpclient import HttpClient
from tor_manager.util.httpresponse import Response as Resp, ResponseCode as RespCode
from tor_manager.util import tools

class ReaderHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.Resp = Resp()
		url = Config.VALUE['master_url'] + "/reader"
		self.http_client = HttpClient(url)
		url2 = Config.VALUE['master_url'] + "/borrow"
		self.http_client2 = HttpClient(url2)
		
	def get(self):
		_method = tools.strip_string(self.get_argument("_method", None))
		
		if _method == "delete":
			self.delete()
			return
			
		if _method == 'put':
			reader_id = tools.strip_string(self.get_argument('reader_id'))
			self.render("readermanage/updatereader.html", reader_id = reader_id)
			return
			
		reader_id = tools.strip_string(self.get_argument('reader_id'))
		reader = {}
		breader = {}
		
		if reader_id != None:
			reader['reader_id'] = reader_id
			breader['readerid'] = reader_id
			resp = self.http_client.get(reader)
			(code, body) = self.http_client.resp_handler(resp)	
			if code != RespCode.SUCCESS and code != RespCode.NO_RECORD:
				failure_reason = resp.get('failure_reason', None)
				self.render("bookmanage/error.html", code = resp['response_code_string'], fail_reason = failure_reason)
				return
				
			for k,v in body.items():
				reader[k]=v
				
			resp = self.http_client2.get(breader)
			(code, body) = self.http_client2.resp_handler(resp)
			if code == RespCode.SUCCESS:
				reader['book'] = body
			else:
				reader['book'] = None
				
			self.render("readermanage/viewreader.html", reader = reader)
			return
			
			
	def post(self):
		logging.info("received post body: %s", self.request.body)
				
		reader_name = tools.strip_string(self.get_argument('reader_name', None))
		sex = tools.strip_string(self.get_argument('sex', None))
		age = tools.strip_string(self.get_argument('age', None))
		email = tools.strip_string(self.get_argument('email',None))
		type = tools.strip_string(self.get_argument('type', None))
		
		reader = {}
		reader['reader_name'] = reader_name
		reader['sex'] = sex
		reader['age'] = age
		reader['email'] = email
		reader['type'] = type
		
		resp = self.http_client.post(reader)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS:
			failure_reason = resp.get('failure_reason', None)
			self.render('readermanage/error.html', code = resp['response_code_string'], fail_reason =failure_reason)
			return
		
		success_type = resp.get('success_type', None)
		self.render('bookmanage/success.html',code=resp['response_code_string'],success_type=success_type)
		return
		
		
	def put(self):
		logging.info("received post body: %s", self.request.body)
		
		_method = tools.strip_string(self.get_argument('_method', None))
		if _method == 'delete':
			self.delete()
			return
			
		reader_id = tools.strip_string(self.get_argument('reader_id', None))
		reader_name = tools.strip_string(self.get_argument('reader_name', None))
		sex = tools.strip_string(self.get_argument('sex', None))
		age = tools.strip_string(self.get_argument('age', None))
		email = tools.strip_string(self.get_argument('email', None))
		type = tools.strip_string(self.get_argument('type', None))
		
		resp = self.http_client.put(reader)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS:
			failure_reason = resp.get('failure_reason', None)
			self.render('readermanage/error.html', code = resp['response_code_string'], fail_reason = failure_reason)
			return
			
		success_type = resp.get('success_type', None)
		self.render('bookmanage/success.html',code=resp['response_code_string'],success_type=success_type)
		return
		
	def delete(self):
	
		reader_id = tools.strip_string(self.get_argument('reader_id', None))
		reader = {}
		if reader_id != None:
			reader['reader_id'] = reader_id
		
		resp = self.http_client.delete(reader)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS:
			failure_reason = resp.get('failure_reason', None)
			self.render('readermanage/error.html', code = resp['response_code_string'], fail_reason = failure_reason)
			return
			
		success_type = resp.get('success_type', None)
		self.render('bookmanage/success.html',code=resp['response_code_string'],success_type=success_type)
		return
		
		
			
			
