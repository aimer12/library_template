#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

import tornado.web
import json,logging,types,time,urllib2
from tor_manager.util.config import Config
from tor_manager.util.httpclient import HttpClient
from tor_manager.util.httpresponse import Response as Resp, ResponseCode as RespCode
from tor_manager.util import tools

class BookHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.Resp = Resp()
		url = Config.VALUE['master_url'] + "/book"
		self.http_client = HttpClient(url)
		url2 = Config.VALUE['master_url'] + "/borrow"
		self.http_client2 = HttpClient(url2)
		
	
	def get(self):
		_method = tools.strip_string(self.get_argument('_method', None))
		
		if _method == 'delete':
			self.delete()
			return
		
		if _method == 'put':
			book_id=tools.strip_string(self.get_argument('book_id', None))
			self.render("bookmanage/updatebook.html", book_id=book_id)
			return
			
		book_id = tools.strip_string(self.get_argument('book_id', None))
		book = {}
		bbook = {}
		if book_id != None:
			book['book_id'] = book_id
			bbook['bookid'] = book_id
			resp = self.http_client.get(book)
			(code, body) = self.http_client.resp_handler(resp)
			if code != RespCode.SUCCESS and code != RespCode.NO_RECORD:
				failure_reason = resp.get('failure_reason', None)
				self.render("bookmanage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
				return
			
			for k,v in body.items():
				book[k]=v
			
			resp = self.http_client2.get(bbook)
			(code, body) =self.http_client2.resp_handler(resp)		
			if code == RespCode.SUCCESS:
				book['sheet'] = 'no'
				book['returndate'] = body['returndate']
				book['borrowdate'] = body['borrowdate']
			else:
				book['sheet'] = "yes"
				book['returndate'] = None
				book['borrowdate'] = None
			
			self.render("bookmanage/viewbook.html", book = book)
			return
			
		se = self.get_argument('_se', None)
		if se == "title":  		
			book_title = tools.strip_string(self.get_argument('book', None))
			book['book_title'] = book_title
		elif se == "author":
			author = tools.strip_string(self.get_argument('book', None))
			book['author'] = author
		else:
			publisher = tools.strip_string(self.get_argument('book', None))
			book['publisher'] = publisher
		
#		if book_title != None:
#			
#		elif author != None:
#			
#		else:
#			
			
		resp = self.http_client.get(book)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS and code != RespCode.NO_RECORD:
			failure_reason = resp.get('failure_reason', None)
			self.render("bookmanage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
			return

		if code == RespCode.NO_RECORD:
			self.render("bookmanage/viewbooks.html",books = None)
			return

		self.render("bookmanage/viewbooks.html", books = body)
		return
           	
           
           	


	def post(self):
		logging.info("received post body: %s", self.request.body)
		book_title = tools.strip_string(self.get_argument('book_title', None))
		author = tools.strip_string(self.get_argument('author', None))
		publisher = tools.strip_string(self.get_argument('publisher', None))
		addr = tools.strip_string(self.get_argument('addr', None))
		description = tools.strip_string(self.get_argument('description', None))
		price = tools.strip_string(self.get_argument('price', None))
		
		book = {}
		book['book_title'] = book_title
		book['author'] = author
		book['publisher'] = publisher
		book['description'] = description
		book['addr'] = addr
		book['price'] = price

		resp = self.http_client.post(book)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS:
			failure_reason = resp.get('failure_reason', None)
			self.render("bookmanage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
			return
		
		success_type = resp.get('success_type', None)
		self.render('bookmanage/success.html',code=resp['response_code_string'],success_type=success_type)
		return




	def put(self):
		logging.info("received post body: %s", self.request.body)
		
		
		book_id = tools.strip_string(self.get_argument('book_id', None))    
		book_title = tools.strip_string(self.get_argument('book_title', None))
		author = tools.strip_string(self.get_argument('author', None))
		publisher = tools.strip_string(self.get_argument('publisher', None))
		description = tools.strip_string(self.get_argument('description', None))
		price = tools.strip_string(self.get_argument('price', None))

		book = {}
		book['book_id'] = book_id
		book['book_title'] = book_title
		book['author'] = author
		book['description'] = description
		
		resp = self.http_client.put(book)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS:
			failure_reason = resp.get('failure_reason', None)
			self.render("bookmanage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
			return
			
		success_type = resp.get('success_type', None)
		self.render('bookmanage/success.html',code=resp['response_code_string'],success_type=success_type)
		return 
		
	def delete(self):

		book_id = tools.strip_string(self.get_argument('book_id', None))

		book = {}
		if book_id != None:
			book['book_id'] = book_id 

		resp = self.http_client.delete(book)
		(code, body) = self.http_client.resp_handler(resp)
		if code != RespCode.SUCCESS:
			failure_reason = resp.get('failure_reason', None)
			self.render("bookmanage/error.html", code=resp['response_code_string'], fail_reason=failure_reason)
			return

		success_type = resp.get('success_type', None)
		self.render('bookmanage/success.html',code=resp['response_code_string'],success_type=success_type)
		return
        
