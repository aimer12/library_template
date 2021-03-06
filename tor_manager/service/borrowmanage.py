#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import tornado.web
import json,logging,types,time,urllib2
from tor_manager.util.config import Config
from tor_manager.util.httpclient import HttpClient
from tor_manager.util.httpresponse import Response as Resp, ResponseCode as RespCode
from tor_manager.util import tools

class BorrowHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.Resp = Resp()
		url = Config.VALUE['master_url'] + "/borrow"
		self.http_client = HttpClient(url)
		
	def get(self):
		_method = tools.strip_string(self.get_argument('_method', None))
		
		if _method == 'delete':
			self.delete()
			return
		
		if _method == 'put':
			self.put()
			return
			
	def post(self):
		logging.info("received post body: %s", self.request.body)
		
		bookid = tools.strip_string(self.get_argument("bookid", None))
		readerid = tools.strip_string(self.get_argument('readerid', None))
		
		borrow = {}
		borrow['bookid'] = bookid
		borrow['readerid'] = readerid
		
		resp = self.http_client.post(borrow)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS:
			failure_reason = resp.get('failure_reason', None)
			self.render("bookmanage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
			return

		success_type = resp.get('success_type', None)
		self.render('bookmanage/success.html',code=resp['response_code_string'],success_type=success_type)
        
	def put(self):
		logging.info("received renew book: %s", self.request.body)
		bookid = tools.strip_string(self.get_argument('bookid', None))
		borrow = {}
		borrow['bookid'] = bookid
		
		resp = self.http_client.put(borrow)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS:
			failure_reason = resp.get('failure_reason', None)
			self.render("bookmanage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
		return
		
		logging.info("renew success!")

		success_type = resp.get('success_type', None)
		self.render('bookmanage/success.html',code=resp['response_code_string'], success_type = success_type)
		
		return
		
		
	def delete(self):
		logging.info("received post body: %s", self.request.body)
	
		bookid = tools.strip_string(self.get_argument('bookid', None))
		borrow = {}
		borrow['bookid'] = bookid
		
		resp = self.http_client.delete(borrow)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS:
			failure_reason = resp.get('failure_reason', None)
			self.render("bookmanage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
			return

		success_type = resp.get('success_type', None)
		self.render('bookmanage/success.html',code=resp['response_code_string'],success_type=success_type)
		return
