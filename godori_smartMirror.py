#-*- coding:utf-8 -*-
#!/usr/bin/python

from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import sys 
from math import atan2

import os
from os import path
import gi 
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf, Gdk, Pango

import uinput

#picamera 
import time
import picamera

#thread
import threading

#nowtime
import datetime

#json
import json
import urllib
import urllib2


import sys
import subprocess

import dbus

from bluetooth import *

import boto
from boto.s3.key import Key

reload(sys)
sys.setdefaultencoding('utf-8')

video_list = ""

flag = False 
flag_photo =False

win = ""

local = 'Suwon'
# weather url 
url_weather = 'http://api.openweathermap.org/data/2.5/weather?q='+local+'&mode=json&APPID=5e212d73632d4e0b16fcddb0bc772978'
u1 = urllib.urlopen(url_weather)
weather= json.loads(u1.read())

# video category url 
url_video_category = 'https://4n54wpk7kd.execute-api.us-east-1.amazonaws.com/dev/categories'
u2 = urllib.urlopen(url_video_category)
video = json.loads(u2.read())

aws_access_key_id = ''
aws_secret_access_key = ''


shape = ""
degree=""

pxbf_home = ""
pxbf_video= ""
pxbf_cam= ""
pxbf_face= ""
pxbf_gallary= ""
pxbf_setting= ""

text = ""
ctldata = ""

flag_ok=False

flag=False
flag1=False 

flag_backhead = False 
flag_video=False
flag_category =False
flag_camera=False
flag_gallary=False
flag_show_video=False
flag_show_gallary=False
flag_facial=False 
flag_fcategory=False
flag_view =False 

file=""
font = Pango.FontDescription('Latha 50')

cam_thread=""
#############
percent = ""
rx="" 
lx="" 
ly=""
lw=""
rw = ""
rbx = ""
rby =""
lbx =""
lby =""
lbw =""

class MyWindow(Gtk.Window, threading.Thread):


  def __init__(self):

	global pxbf_home
	global pxbf_video
	global pxbf_cam
	global pxbf_face
	global pxbf_gallary
	global pxbf_setting
	global weather
	global string

	Gtk.Window.__init__(self, title="")


	self.set_border_width(0)
	#self.set_size_request(100,100)
	self.fullscreen()
	#self.notebook = Gtk.Notebook()
	#self.add(self.notebook)
  
	
	subprocess.call('sudo chmod 777 /var/run/sdp', shell=True)


	pics_list=[]
	pics_name=[]

	# get image
	for root, dirs, files in os.walk('/home/pi/image/'):
	  for fn in files:
		pics_name.append(fn)
		f= os.path.join(root, fn)
		pics_list.append(f)
	
	

	for name, pic in zip (pics_name,pics_list):
	  if name == "01.png":
		pxbf_video = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic,  110, 110, True)
	  elif name == "02.png":
		pxbf_cam = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic,  110, 110, True)
	  elif name == "03.png":
		pxbf_face= GdkPixbuf.Pixbuf.new_from_file_at_scale(pic, 110, 110, True)
	  elif name == "04.png":
		pxbf_gallary = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic, 110, 110, True)
	  elif name == "05.png":
		pxbf_backhead = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic, 110, 110, True)


	##################################### HOME #####################################

	self.timer = Gtk.Label()

	# buttonbox
	buttonbox = Gtk.HButtonBox(Gtk.Orientation.HORIZONTAL)
	buttonbox.set_layout(Gtk.ButtonBoxStyle.SPREAD)
	buttonbox.set_spacing(50)

	# video button
	video = Gtk.Image()
	video.set_from_pixbuf(pxbf_video)
	video.show()
	frame1 = Gtk.Frame()
	frame1.show()
	frame1.add(video)

	b_video = Gtk.Button()
	b_video.add(frame1)
	b_video.show()

	b_video.connect("clicked", self.on_button_video)
	buttonbox.add(b_video)

	# camera button
	cam = Gtk.Image()
	cam.set_from_pixbuf(pxbf_backhead)
	cam.show()
	frame2 = Gtk.Frame()
	frame2.show()
	frame2.add(cam)

	b_cam = Gtk.Button()
	b_cam.add(frame2)
	b_cam.show()

	b_cam.connect("clicked", self.on_button_show_backhead_background)
	buttonbox.add(b_cam)

	# camera button
	cam = Gtk.Image()
	cam.set_from_pixbuf(pxbf_cam)
	cam.show()
	frame2 = Gtk.Frame()
	frame2.show()
	frame2.add(cam)

	b_cam2 = Gtk.Button()
	b_cam2.add(frame2)
	b_cam2.show()

	b_cam2.connect("clicked", self.on_button_show_background)
	buttonbox.add(b_cam2)


	# face button
	face = Gtk.Image()
	face.set_from_pixbuf(pxbf_face)
	face.show()
	frame3 = Gtk.Frame()
	frame3.show()
	frame3.add(face)

	b_face = Gtk.Button()
	b_face.add(frame3)
	b_face.show()

	###############
	b_face.connect("clicked", self.on_button_facial_test)
	buttonbox.add(b_face)

	# gallary button
	gallary = Gtk.Image()
	gallary.set_from_pixbuf(pxbf_gallary)
	gallary.show()
	frame4 = Gtk.Frame()
	frame4.show()
	frame4.add(gallary)

	b_gallary = Gtk.Button()
	b_gallary.add(frame4)
	b_gallary.show()

	b_gallary.connect("clicked", self.on_button_gallary)
	buttonbox.add(b_gallary)


	grid = Gtk.Grid(row_homogeneous=True,
		  column_spacing=0, row_spacing=0)
	grid.attach(self.timer, 0,0,1,1)
	grid.attach(buttonbox, 0,2,2,1)

	self.add(grid)
	self.show_all()

	thread2()

  def on_button_facial_test(self, widget):
	global flag_facial
	flag_facial=True

	self.facial_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.facial_window.fullscreen()
	
	self.liststore6 = Gtk.ListStore (str)
	self.liststore6.append(["Eyebrow"])
	self.liststore6.append(["Glasses"])
	self.liststore6.append(["Hat"])
  
	#creating the treeview
	self.treeview6 = Gtk.TreeView(model=self.liststore6)
	
	# facial category
	facial_category = Gtk.CellRendererText(weight= 50)
	facial_category.set_property('font-desc', font)

	column_text = Gtk.TreeViewColumn("", facial_category, text=0)
	self.treeview6.append_column(column_text)

	self.scrolled_window6 = Gtk.ScrolledWindow() 
	self.scrolled_window6.set_vexpand(True) 
	self.scrolled_window6.set_hexpand(True)
	self.scrolled_window6.set_border_width(0)

	self.scrolled_window6.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
	self.scrolled_window6.add_with_viewport(self.treeview6)
	
	# a grid to attach the widget
		
	grid_bg = Gtk.Grid(row_homogeneous=True, 
			column_spacing=0, row_spacing=1)
	grid_bg.attach(self.scrolled_window6, 0, 0, 7, 4)
	self.facial_window.add(grid_bg)
	self.treeview6.connect('row-activated', self.fcategory)
	self.facial_window.show_all()	
	self.facial_test()


  def fcategory(self, aa, bb, cc):
	global text
	global flag_facial
	global flag_fcategory
	global flag_ok

	flag_facial = False
	flag_fcategory = True 

	flag_ok = False
	self.liststore7 = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
	
	select_fcategory = self.treeview6.get_selection()
	(model, treeiter) = select_fcategory.get_selected()
	  

	if (treeiter != None ) :
	  for i in range(3):
		if model[treeiter][0] == "Eyebrow":
			text = "eyebrow"
		elif model[treeiter][0] == "Glasses":
			text = "glasses"
		elif model[treeiter][0] == "Hat":
			text = "cap"

	pics_list=[]
	pics_name=[]

	# get image
	for root, dirs, files in os.walk('/home/pi/'+text+'/'):
		for fn in files:
			pics_name.append(fn)
			f= os.path.join(root, fn)
			pics_list.append(f)
	
	
	#add pixbuf  
	i=1
	for name, pic in zip (pics_name,pics_list):
		if text == "eyebrow":
			print len(name)
			if len(name) == 13:
				pxbf_photo = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic,200,100,True)
				string = text +' '+ str(i)
				self.liststore7.append([pxbf_photo, string, name])
				i = i+1		
		else : 
			pxbf_photo = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic,200,100,True)
			string = text +' '+ str(i)
			self.liststore7.append([pxbf_photo, string, name])
			i = i+1
	i=1
  
	self.iconview1= Gtk.IconView.new()
	self.iconview1.set_model(self.liststore7)
	self.iconview1.set_item_padding(0)
	self.iconview1.set_margin(0)
	self.iconview1.set_item_width(200)
	self.iconview1.set_pixbuf_column(0)
	self.iconview1.set_text_column(1)
	self.iconview1.set_columns(4)
	#self.iconview1.set_text_column(2)
  
	# the scrolledwindow 
	scrolled_window3 = Gtk.ScrolledWindow()
	scrolled_window3.set_border_width(0)
	scrolled_window3.set_vexpand(True)
	scrolled_window3.set_hexpand(False)

	# there is always the scrollbar (otherwise: AUTOMATIC - only if needed- or NEVER)
	scrolled_window3.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
	scrolled_window3.add_with_viewport(self.iconview1)

	# a grid to attach the widget
	grid = Gtk.Grid(row_homogeneous=True,
			column_spacing=0, row_spacing=2)
	grid.attach(scrolled_window3, 0, 0, 7, 4)
	#grid.attach(buttonbox, 3,6,1,1 )

	self.fcategory_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.fcategory_window.fullscreen()
	
	self.fcategory_window.add(grid)
	self.fcategory_window.show_all()
	
	self.iconview1.connect('item-activated', self.show_image)

	flag_ok = True 


  def show_image(self, widget, aa):
	global text
	global shape 
	global flag_fcategory
	global flag_view

	flag_fcategory = False
	flag_view = True 
 

	self.image_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.image_window.fullscreen()

	selected_path= self.iconview1.get_selected_items()[0]
	selected_iter = self.iconview1.get_model().get_iter(selected_path)
	# = select_image.get_selected_items()

	pics_list=[]
	pics_name=[]

	for root, dirs, files in os.walk('/home/pi/'+text+ '/'):
	  for fn in files:
		pics_name.append(fn)
		f= os.path.join(root, fn)
		pics_list.append(f)


	text11 = self.iconview1.get_model().get_value(selected_iter, 2)

	if  text11 != None:   
	  for name, pic in zip (pics_name,pics_list):
		if name == text11: 
			if text == "eyebrow": 
				text_img_l=cv2.imread('/home/pi/'+text+'/'+name, -1)
				name, name_split=name.split(".", 1)
				text_img_r=cv2.imread('/home/pi/'+text+'/'+name+'_r.png', -1)
			else:
				text_img=cv2.imread('/home/pi/'+text+'/'+name, -1)
	
	if text == "glasses":
		percent = 0.0025 * (lx+lw-rx)
		degree = 180- (atan2(ry-ly, rx - lx) * 180 )/ 3.141592
		
		rows,cols = text_img.shape[:2]   
		M = cv2.getRotationMatrix2D( (cols/2, rows/2), degree, 1 )  
		dst = cv2.warpAffine(text_img, M, (cols,rows))  
	
		text_imgDownscale = cv2.resize(dst, None , fx=percent, fy=percent, interpolation=cv2.INTER_AREA)
		x_offset =rx+rw+ ((lx-(rx+rw))/2)  -320*percent
		y_offset = ly - 107*percent

		person_image = cv2.imread ('/home/pi/facial_image/image.png', -1)
		person_image = imutils.resize(person_image, width=500)

		for c in range(0,3):
			person_image[y_offset:y_offset + text_imgDownscale.shape[0],x_offset:x_offset + text_imgDownscale.shape[1], c] = text_imgDownscale[:,:,c] * (text_imgDownscale[:,:,3]/255.0) + person_image[y_offset:y_offset + text_imgDownscale.shape[0], x_offset:x_offset + text_imgDownscale.shape[1], c]* (1.0 - text_imgDownscale[:,:,3]/255.0)
		
		cv2.imwrite('/home/pi/example.png', person_image)
		
		image_bg = Gtk.Image()    
		image_bg.set_from_file("/home/pi/example.png")
		image_bg.show()
	

	elif text == "eyebrow":
		percent = 0.00025 * (lbx+lbw-rbx)
		degree = 180- (atan2(rby-lby,rbx - lbx) * 180 )/ 3.141592
		
		rows_r,cols_r = text_img_r.shape[:2]   
		M_r = cv2.getRotationMatrix2D( (cols_r/2, rows_r/2), degree, 1 )  
		dst_r = cv2.warpAffine(text_img_r, M_r, (cols_r,rows_r))  
	
		text_img_rDownscale = cv2.resize(dst_r, None , fx=percent, fy=percent, interpolation=cv2.INTER_AREA)


		rows_l,cols_l = text_img_l.shape[:2]   
		M_l = cv2.getRotationMatrix2D( (cols_l/2, rows_l/2), degree, 1 )  
		dst_l = cv2.warpAffine(text_img_l, M_l, (cols_l,rows_l))  
	
		text_img_lDownscale = cv2.resize(dst_l, None , fx=percent, fy=percent, interpolation=cv2.INTER_AREA)


		x_offset_r = rbx 
		y_offset_r = rby-4

		x_offset_l = lbx
		y_offset_l = lby-4

		person_image = cv2.imread ('/home/pi/facial_image/image.png', -1)
		person_image = imutils.resize(person_image, width=500)

		for c in range(0,3):
			person_image[y_offset_l:y_offset_l + text_img_lDownscale.shape[0],x_offset_l:x_offset_l + text_img_lDownscale.shape[1], c] = text_img_lDownscale[:,:,c] * (text_img_lDownscale[:,:,3]/255.0) + person_image[y_offset_l:y_offset_l + text_img_lDownscale.shape[0], x_offset_l:x_offset_l + text_img_lDownscale.shape[1], c]* (1.0 - text_img_lDownscale[:,:,3]/255.0)
			person_image[y_offset_r:y_offset_r + text_img_rDownscale.shape[0],x_offset_r:x_offset_r + text_img_rDownscale.shape[1], c] = text_img_rDownscale[:,:,c] * (text_img_rDownscale[:,:,3]/255.0) + person_image[y_offset_r:y_offset_r + text_img_rDownscale.shape[0], x_offset_r:x_offset_r + text_img_rDownscale.shape[1], c]* (1.0 - text_img_rDownscale[:,:,3]/255.0)
		
		cv2.imwrite('/home/pi/example.png', person_image)
		
		image_bg = Gtk.Image()    
		image_bg.set_from_file("/home/pi/example.png")
		image_bg.show()

	elif text == "cap":
		percent = 0.0025 * (lx+lw-rx)
		degree = 180- (atan2(ry-ly,rx - lx) * 180 )/ 3.141592
		
		rows,cols = text_img.shape[:2]   
		(left_x, left_y) = shape[17]
		(right_x, right_y) = shape[26]
		face_x = right_x-left_x
		face_y = face_x *rows/cols

		ab_deg = degree
		if degree >180:
			ab_deg = 360-degree

		mul_num = 2.7*0.67*(89/float(face_x))
		per = (float(face_x)/cols) * mul_num

		face_x = face_x * mul_num
		face_y = face_y * mul_num

		center_x = ((left_x +right_x)/2)
		center_x = center_x-(face_x/2)

		M = cv2.getRotationMatrix2D( (cols/2, rows/2), degree, 1 )  
		dst = cv2.warpAffine(text_img, M, (cols,rows))  
	
		text_imgDownscale = cv2.resize(dst, None , fx=per, fy=per, interpolation=cv2.INTER_AREA)

		if degree < 180:
			x_offset = center_x - (face_x/20)
		else: x_offset = center_x + (face_x/20)

		y_offset = left_y -face_y

		if y_offset < 0:
			y_offset= 0.0


		person_image = cv2.imread ('/home/pi/facial_image/image.png', -1)
		person_image = imutils.resize(person_image, width=500)

		for c in range(0,3):
			person_image[y_offset:y_offset + text_imgDownscale.shape[0],x_offset:x_offset + text_imgDownscale.shape[1], c] = text_imgDownscale[:,:,c] * (text_imgDownscale[:,:,3]/255.0) + person_image[y_offset:y_offset + text_imgDownscale.shape[0], x_offset:x_offset + text_imgDownscale.shape[1], c]* (1.0 - text_imgDownscale[:,:,3]/255.0)
		
		cv2.imwrite('/home/pi/example.png', person_image)
		
		image_bg = Gtk.Image()    
		image_bg.set_from_file("/home/pi/example.png")
		image_bg.show()
	'''
	hbox = Gtk.Box(spacing=6)

	image_photo = Gtk.Image()
	image_photo.set_from_file("/home/pi/button/sendsend.png")
	image_photo.show()

	button = Gtk.ToggleButton()
	button.add(image_photo)
	button.connect("toggled", self.on_button_send, "1")
	hbox.pack_start(button, True, True, 0)

	grid_bg = Gtk.Grid(row_homogeneous=True, 
				column_spacing=0, row_spacing=1)
	grid_bg.attach(image_bg, 0, 0, 7, 4)
	grid_bg.attach_next_to(hbox, image_bg,
				 Gtk.PositionType.BOTTOM, 1, 1)
	'''

	buttonbox = Gtk.HButtonBox(Gtk.Orientation.HORIZONTAL)
	buttonbox.set_layout(Gtk.ButtonBoxStyle.SPREAD)
	buttonbox.set_spacing(120)

	image_photo = Gtk.Image()
	image_photo.set_from_file("/home/pi/button/sendsend.png")
	image_photo.show()
	b_photo = Gtk.Button()
	b_photo.add(image_photo)
	b_photo.connect("clicked", self.on_button_send)
  
	buttonbox.add(b_photo)

	grid_bg = Gtk.Grid(row_homogeneous=True, 
				column_spacing=0, row_spacing=1)
	grid_bg.attach(image_bg, 0, 0, 7, 4)
	grid_bg.attach_next_to(buttonbox, image_bg, Gtk.PositionType.BOTTOM, 1, 1)

	self.image_window.add(grid_bg)
	self.image_window.show_all()


  def on_button_send(self, widget): 
	global file 
	
	state = "on"
	now = datetime.datetime.now()
	file_name= now.strftime('%Y-%m-%d_%H:%M:%S')+'.png'

	subprocess.call('cp example.png '+file_name, shell=True)
	file = open(file_name, 'r+')
	upload_to_s3()
	subprocess.call('mv '+file_name+' /home/pi/syeon/'+file_name, shell=True)




  def facial_test(self):  	
	global rx
	global rw
	global ry 
	global ly
	global lx
	global lw 
	global rbx
	global rby
	global lbx
	global lby
	global lbw
	global shape

	person_image = cv2.imread ('/home/pi/facial_image/image.png', -1)
	#eyeglasses_img=cv2.imread('/home/pi/landmarks/glasses10.png', -1)
	#subprocess.call('python facial_test.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1', shell=True)

	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--shape-predictor", required=True,
		help="path to facial landmark predictor")
	args = vars(ap.parse_args())

	# initialize dlib's face detector (HOG-based) and then create
	# the facial landmark predictor
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(args["shape_predictor"])

	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
	(lbStart, lbEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
	(rbStart, rbEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]

	person_image = imutils.resize(person_image, width=500)
	gray = cv2.cvtColor(person_image, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 1)

	for (i, rect) in enumerate(rects):
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		(rx,ry,rw,rh) = cv2.boundingRect(np.array([shape[rStart:rEnd]]))
		(lx,ly,lw,lh) = cv2.boundingRect(np.array([shape[lStart:lEnd]]))
		(rbx,rby,rbw,rbh) = cv2.boundingRect(np.array([shape[rbStart:rbEnd]]))
		(lbx,lby,lbw,lbh) = cv2.boundingRect(np.array([shape[lbStart:lbEnd]]))
	
	
  def __on_dp_click(self, widget, aa, bb):
	global video_list
	global flag_video
	global flag_category

	flag_category=False
	flag_video=True


	select_video = self.treeview.get_selection()
	(model, treeiter) = select_video.get_selected()
	  
	if (treeiter != None ) :
	  for i in range(len(video['list'])):
		if model[treeiter][0] == video['list'][i]['name']:
		  url_video_list = 'https://4n54wpk7kd.execute-api.us-east-1.amazonaws.com/dev/category?id=' + video['list'][i]['id']
		  u3 = urllib.urlopen(url_video_list)
		  video_list= json.loads(u3.read())

	
	self.beauty_video_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.beauty_video_window.fullscreen()

	overlay = Gtk.Overlay()
	self.beauty_video_window.add(overlay)
	drawingarea = Gtk.DrawingArea()
	overlay.add(drawingarea)
	
  
	#creating the liststore 
	self.liststore1= Gtk.ListStore(GdkPixbuf.Pixbuf,str)
	#self.liststore1= Gtk.ListStore(str)
	  
	
	for i in range(len(video_list['list'])):
	  string = video_list['list'][i]['name']
	  
	  pics_list=[]
	  pics_name=[]

	  thumbnail_url = video_list['list'][i]['thumbnail_url']
	  file_name = "%d.jpg" %i

	  urllib.urlretrieve(thumbnail_url, file_name)    
	  subprocess.call('mv '+file_name+' ./photo/', shell=True)
		  # get image
	  for root, dirs, files in os.walk('./photo/'):
		for fn in files:
		  pics_name.append(fn)
		  f= os.path.join(root, fn)
		  pics_list.append(f)
	
	
	  #add pixbuf  
	  for name, pic in zip (pics_name,pics_list):
		if name == file_name:
		  pxbf_photo = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic,200,100,True)
		  self.liststore1.append([pxbf_photo, string])
		  subprocess.call('rm ./photo/'+file_name, shell=True)
  

	#creating the treeview
	self.treeview1 = Gtk.TreeView(model=self.liststore1)

	thumbnail_pixbuf = Gtk.CellRendererPixbuf()
	column1_pixbuf = Gtk.TreeViewColumn("", thumbnail_pixbuf, pixbuf=0)
	column1_pixbuf.set_alignment(0.5)
	self.treeview1.append_column(column1_pixbuf)

	# video category
	beauty_video_list = Gtk.CellRendererText(weight= 50)
	beauty_video_list.set_property('font-desc', font)
	column_text = Gtk.TreeViewColumn("", beauty_video_list, text=1)
	self.treeview1.append_column(column_text)


	self.scrolled_window1 = Gtk.ScrolledWindow() 
	self.scrolled_window1.set_vexpand(True) 
	self.scrolled_window1.set_hexpand(True)
	self.scrolled_window1.set_border_width(0)
	self.scrolled_window1.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
	self.scrolled_window1.add_with_viewport(self.treeview1)

	# a grid to attach the widget
	grid = Gtk.Grid(row_homogeneous=True, 
			column_spacing=0, row_spacing=2)
	grid.attach(self.scrolled_window1, 0, 0, 7, 4)
	#grid.attach(buttonbox, 2,6,1,1 )

	overlay.add_overlay(grid)
	overlay.show_all()
	self.beauty_video_window.show_all()

	self.treeview1.connect('row-activated', self.on_button_play_background)
  
  def on_button_video(self, widget):
	global flag_category

	flag_category=True

	self.video_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.video_window.fullscreen()          
	#creating the liststore 
	self.liststore = Gtk.ListStore (str)
	
	for i in range(len(video['list'])):
	  string = video['list'][i]['name']
	  self.liststore.append([string])
  

	#creating the treeview
	self.treeview = Gtk.TreeView(model=self.liststore)
	
	# video category
	video_category = Gtk.CellRendererText(weight= 50)
	video_category.set_property('font-desc', font)

	column_text = Gtk.TreeViewColumn("", video_category, text=0)
	self.treeview.append_column(column_text)

	self.scrolled_window = Gtk.ScrolledWindow() 
	self.scrolled_window.set_vexpand(True) 
	self.scrolled_window.set_hexpand(True)
	self.scrolled_window.set_border_width(0)

	self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
	self.scrolled_window.add_with_viewport(self.treeview)

	# a grid to attach the widget
	grid = Gtk.Grid(row_homogeneous=True,
			column_spacing=0, row_spacing=2)
	grid.attach(self.scrolled_window, 0, 0, 7, 4)
	#grid.attach(buttonbox, 3,6,1,1 )

	self.video_window.add(grid)
	self.video_window.show_all()
	
	self.treeview.connect('row-activated', self.__on_dp_click)
	
  def on_button_show_backhead_background(self, widget):
	global flag_backhead
	flag_backhead = True
	'''
	self.backhead_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.backhead_window.fullscreen()
	image_bg = Gtk.Image()    
	image_bg.set_from_file("/home/pi/button/black.png")
	image_bg.show()
	
	# a grid to attach the widget
 
	grid_bg = Gtk.Grid(row_homogeneous=True, 
			column_spacing=0, row_spacing=1)
	grid_bg.attach(image_bg, 0, 0, 7, 4)
	self.backhead_window.add(grid_bg)
	self.backhead_window.show_all()
	'''
	subprocess.call('cheese', shell=True)

  def on_button_gallary(self, widget):
	global flag_gallary

	flag_gallary = True

	self.gallary_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.gallary_window.fullscreen()

	self.liststore5 = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
	#self.liststore5 = Gtk.ListStore(GdkPixbuf.Pixbuf)
	pics_list=[]
	pics_name=[]

	# get image
	for root, dirs, files in os.walk('/home/pi/syeon/'):
	  for fn in files:
		pics_name.append(fn)
		f= os.path.join(root, fn)
		pics_list.append(f)
	

	i=1
	for name, pic in zip (pics_name,pics_list):     
	  pxbf_photo = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic,  300, 200, True)
	  #self.liststore5.append([pxbf_photo])
	  self.liststore5.append([pxbf_photo, "picture"+str(i), name])
	  i = i+1

	self.iconview= Gtk.IconView.new()
	self.iconview.set_model(self.liststore5)
	self.iconview.set_item_padding(0)
	self.iconview.set_margin(0)
	self.iconview.set_item_width(200)
	self.iconview.set_pixbuf_column(0)
	self.iconview.set_text_column(1)
	self.iconview.set_columns(4)

  
	# the scrolledwindow 
	scrolled_window3 = Gtk.ScrolledWindow()
	scrolled_window3.set_border_width(0)
	scrolled_window3.set_vexpand(True)
	scrolled_window3.set_hexpand(False)

	# there is always the scrollbar (otherwise: AUTOMATIC - only if needed- or NEVER)
	scrolled_window3.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) 
	scrolled_window3.add_with_viewport(self.iconview)

	# a grid to attach the widget
	grid = Gtk.Grid(row_homogeneous=True,
			column_spacing=0, row_spacing=2)
	grid.attach(scrolled_window3, 0, 0, 7, 4)
	#grid.attach(buttonbox, 3,6,1,1 )

	self.gallary_window.add(grid)
	self.gallary_window.show_all()
	
	self.iconview.connect('item-activated', self.show_gallary)

  def show_gallary(self, widget, aa):
	global flag_show_gallary
	global flag_gallary

	flag_gallary = False
	flag_show_gallary =True

	self.show_gallary_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.show_gallary_window.fullscreen()

	selected_path= self.iconview.get_selected_items()[0]
	selected_iter = self.iconview.get_model().get_iter(selected_path)
	# = select_image.get_selected_items()

	pics_list=[]
	pics_name=[]

	for root, dirs, files in os.walk('/home/pi/syeon/'):
	  for fn in files:
		pics_name.append(fn)
		f= os.path.join(root, fn)
		pics_list.append(f)


	text = self.iconview.get_model().get_value(selected_iter, 2)
	if  text != None:   
	  for name, pic in zip (pics_name,pics_list):
		if name == text:      
		  pxbf_photo = GdkPixbuf.Pixbuf.new_from_file_at_scale(pic,  900, 600, True)


	big_image = Gtk.Image()
	big_image.set_from_pixbuf(pxbf_photo)
	big_image.show()
	frame = Gtk.Frame()
	frame.show()
	frame.add(big_image)
	# a grid to attach the widget
	grid = Gtk.Grid(row_homogeneous=True,
			column_spacing=0, row_spacing=2)
	grid.attach(frame, 0, 0, 7, 4)
	#grid.attach(buttonbox, 3,6,1,1 )

	self.show_gallary_window.add(grid)
	self.show_gallary_window.show_all()


  # Video player
  def video_play(self):
  
	select_video = self.treeview1.get_selection()
	(model, treeiter) = select_video.get_selected()

	convert = str(unicode(model[treeiter][1]))


	if treeiter != None:
		for i in range(len(video_list['list'])):                                               
			if convert == video_list['list'][i]['name']:                                  
				url_youtube = 'https://youtube.com/watch?v='+ video_list['list'][i]['video_id']
				subprocess.call ("omxplayer --win '110, 0, 690, 386' `youtube-dl -g "+ url_youtube +"`", shell=True)                                
  
	
	self.play_window.destroy()


  def on_button_show_background(self, widget):
	global flag_camera
	flag_camera= True

	self.show_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.show_window.fullscreen()  

	overlay = Gtk.Overlay()
	self.show_window.add(overlay)
	drawingarea = Gtk.DrawingArea()
	overlay.add(drawingarea)

	
	buttonbox = Gtk.HButtonBox(Gtk.Orientation.HORIZONTAL)
	buttonbox.set_layout(Gtk.ButtonBoxStyle.SPREAD)
	buttonbox.set_spacing(120)


	image_photo = Gtk.Image()
	image_photo.set_from_file("/home/pi/button/send.png")
	image_photo.show()
	b_photo = Gtk.Button()
	b_photo.add(image_photo)
	b_photo.connect("clicked", self.on_button_photo)
  
	buttonbox.add(b_photo)

	image_bg = Gtk.Image()    
	image_bg.set_from_file("/home/pi/button/black.png")
	image_bg.show()
	
	# a grid to attach the widget
 
	grid_bg = Gtk.Grid(row_homogeneous=True, 
			column_spacing=0, row_spacing=1)
	grid_bg.attach(image_bg, 0, 0, 7, 4)
	grid_bg.attach_next_to(buttonbox, image_bg,
				 Gtk.PositionType.BOTTOM, 2, 1)

	overlay.add_overlay(grid_bg)
	overlay.show_all()
	self.show_window.show_all()

	thread()



	#######################################################################
  def on_button_photo(self, widget):
	global flag_photo
	flag_photo = True 


  def update(self):

	# weather url 
	temperature = float(weather['main']['temp']) - 273.15
	
	self.timer.set_markup("<span foreground='#FFFFFF' size='35000' font_family='arial' weight='heavy'><big>"
			+ 'Weather: '+ weather['weather'][0]['main']+'\nTemp: '+str(temperature)+"℃\nHumidity: "+ str(weather['main']['humidity'])+ '%\n\n'
			+ time.strftime('%Y년 %m월 %d일 \n     %H:%M:%S')+"</big></span>")

	return True  #needed to keep the update method in the schedule



  def on_button_play_background (self, widget, aa, bb):
	global flag_show_video
	global flag_video 

	flag_video = False
	flag_show_video =True

	self.play_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
	self.play_window.fullscreen()  
	#self.window.set_default_size(500, 400)
	overlay = Gtk.Overlay()
	self.play_window.add(overlay)
	drawingarea = Gtk.DrawingArea()
	overlay.add(drawingarea)

  
	image_bg = Gtk.Image()    
	image_bg.set_from_file("/home/pi/button/black.png")
	image_bg.show()

	grid_bg = Gtk.Grid(row_homogeneous=True, 
			column_spacing=0, row_spacing=0)
	grid_bg.attach(image_bg, 0, 0, 7, 4)

	overlay.add_overlay(grid_bg)
	overlay.show_all()
	
	self.play_window.show_all()

	play_thread = threading.Thread(target=self.video_play)
	play_thread.daemon = True
	play_thread.start()
	
def upload_to_s3(callback=None, md5=None, reduced_redundancy=False, content_type=None):
  global file
  global flag1

  flag1 = False

  key = 'origin/'+file.name

  try:
	size = os.fstat(file.fileno()).st_size
  except:
	# Not all file objects implement fileno(),
	# so we fall back on this
	file.seek(0, os.SEEK_END)
	size = file.tell()

  conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
  bucket = 'godori-img'
  bucket = conn.get_bucket(bucket, validate=True)
  k = Key(bucket)
  k.key = key

  if content_type:
	k.set_metadata('Content-Type', content_type)
  sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)
  k.set_acl('public-read')

  # Rewind for later use
  file.seek(0)

  flag1 = True
 

#video recording and stroe
def Camera():
  global flag
  global flag_photo
  global flag_camera
  global filename
  global file

  flag = False

  with picamera.PiCamera() as camera:
	camera.resolution = (720, 480)
	camera.framerate = 25
	camera.start_preview(fullscreen=False, window = (110, 0, 580, 386))

	#flag=False
	while flag_camera:
	  if flag_photo: #send button
		now = datetime.datetime.now()
		
		filename= now.strftime('%Y-%m-%d_%H:%M:%S')+'.png'
		camera.capture(filename)

		file = open(filename, 'r+')

		upload_thread = threading.Thread(target=upload_to_s3)
		upload_thread.daemon = True
		upload_thread.start()

		subprocess.call('cp '+filename+' /home/pi/syeon/'+filename, shell=True)
		subprocess.call('cp '+filename+' /home/pi/facial_image/image.png', shell=True)
		subprocess.call('rm '+filename, shell=True)
		flag_photo = False
	  else : time.sleep(0.1)

	camera.stop_preview()

  flag=True
  


def Control():
  global ctldata
  global win

  global flag
  global flag_category
  global flag_video
  global flag_camera
  global flag_gallary
  global flag_show_video
  global flag_show_gallary
  global flag_facial
  global flag_fcategory
  global flag_view
  global flag_backhead
  global flag_ok
  global flag1
  subprocess.call('sudo modprobe uinput', shell=True)

  while True:
	server_sock=BluetoothSocket( RFCOMM )
	server_sock.bind(("",PORT_ANY))
	server_sock.listen(1)

	port = server_sock.getsockname()[1]
	uuid = "00001101-0000-1000-8000-00805f9b34fb"
	advertise_service( server_sock, "SampleServer",

			  service_id = uuid,

			  service_classes = [ uuid, SERIAL_PORT_CLASS ],

			  profiles = [ SERIAL_PORT_PROFILE ])

	print "Waiting for connection on RFCOMM channel %d" % port

	client_sock, client_info = server_sock.accept()
	print "Accepted connection from ", client_info

	#this part will try to get something form the client
	# you are missing this part - please see it's an endlees loop!!


	try:
		while True:
			aa=""
			ctldata = client_sock.recv(1024)

			device = uinput.Device([
				uinput.KEY_RIGHT,
				uinput.KEY_LEFT,
				uinput.KEY_UP,
				uinput.KEY_DOWN,
				uinput.KEY_ENTER,
				uinput.KEY_LEFTALT,
				uinput.KEY_F4
			])


			if len(ctldata) != 0: 
				if ctldata == '1\n':
					device.emit_click(uinput.KEY_LEFT)
				elif ctldata =='2\n':
					device.emit_click(uinput.KEY_RIGHT)
				elif ctldata =='3\n':
					device.emit_click(uinput.KEY_UP)
				elif ctldata =='4\n':
					device.emit_click(uinput.KEY_DOWN)
				elif ctldata =='5\n':
					device.emit_click(uinput.KEY_ENTER)
				elif ctldata =='6\n' :
					if flag_category:
						flag_category =False
						win.video_window.destroy()
					elif flag_video:
						flag_video =False
						win.beauty_video_window.destroy()
						flag_category =True
					elif flag_show_video:
						flag_show_video=False
						subprocess.call('/home/pi/omxplayer/dbuscontrol.sh stop', shell=True)
						device.emit_combo([uinput.KEY_LEFTALT,uinput.KEY_F4])
						flag_video= True
					elif flag_camera:
						flag_camera =False
						device.emit_combo([uinput.KEY_LEFTALT,uinput.KEY_F4])
						flag_photo = False
						'''
						while True:
							if flag and flag1:
								flag_camera =False
								flag_photo = False
								win.show_window.destroy()
								break
							else: time.sleep(0.1)
						'''
					elif flag_gallary:
						flag_gallary=False
						device.emit_combo([uinput.KEY_LEFTALT,uinput.KEY_F4])
					elif flag_show_gallary:
						flag_show_gallary=False
						win.show_gallary_window.destroy()
						flag_gallary=True
					elif flag_facial:
						flag_facial =False
						win.facial_window.destroy()
					elif flag_backhead:
						flag_backhead =False
						device.emit_combo([uinput.KEY_LEFTALT,uinput.KEY_F4])
					elif flag_fcategory:
						while True:
							if flag_ok:
								flag_fcategory=False
								win.fcategory_window.destroy()
								flag_facial=True
								break
							else : time.sleep(0.1)
					elif flag_view:
						flag_view = False 
						device.emit_combo([uinput.KEY_LEFTALT,uinput.KEY_F4])
						flag_fcategory =True 
						'''
						flag_view =False
						win.image_window.destroy()
						flag_fcategory=True 
						'''
						'''
						while True:
							if flag1:
								flag_view =False
								flag_fcategory=True 
								win.image_window.destroy()
								break
							else: time.sleep(0.1)
						'''
				elif ctldata =='PLAY\n':
					subprocess.call('/home/pi/omxplayer/dbuscontrol.sh pause', shell=True)
				elif ctldata == 'FF\n':
					subprocess.call('/home/pi/omxplayer/dbuscontrol.sh seek 5000000', shell=True)
				elif ctldata == 'RW\n':
					subprocess.call('/home/pi/omxplayer/dbuscontrol.sh seek -5000000', shell=True)
			else :	break
	  	
  # rangeise an exception if there was any error
	except IOError:
		pass

	print "disconnected"
	client_sock.close()
	server_sock.close()



#camera thread

def thread():
  cam_thread = threading.Thread(target=Camera, args=())
  cam_thread.daemon = True
  cam_thread.start()

def thread2():
  control_thread = threading.Thread(target=Control, args=())
  control_thread.daemon = True
  control_thread.start() 



def main(argv):
  global win
  def gtk_style():
	css = """
	#MyWindow {
	  background-color: #000000;
	  border-color: #000000;
	  transition-property: color, background-color, border-color, background-image, padding, border-width;
	  transition-duration: 1s;  
	}
	GtkWindow {
	  background-color: #000000;
	  border-color: #000000;
	}
	GtkListStore {
	  border-color: #000000;
	  background-color: #000000;
	}
	GtkListStore:focus{
	  border:solid 10px;
	  border-color: #FBC112;      
	}

	GtkBox {
	  border:solid 10px;
	  border-color: #000000;
	  background-color: transparent;
	  -moz-border-radius: 40px;
	  -webkit-border-radius: 40px;
	  border-radius: 40px;
  
	}
	GtkBox:focus {
	  border:solid 10px;
	  border-color: #FBC112;
	}

	GtkScrolledWindow {
	  background-color: #000000;
	}
	GtkIconView {
	  margin: 0px;
	  padding: 0px;
	  color: #b41318;
	  background-color: #000000;
	  font-size: 20px;
	}
	GtkIconView:focus {
	  margin: 0px;
	  padding: 0px;
	  color: #FFFFFF;
	  background-color: #000000;
	}
	GtkTreeView {
	  color: #FBC112;
	  border-color: #000000;
	  background-color: #000000;
	}
	GtkTreeView:focus {
	  color: #FFFFFF;
	  background-color: #000000;
	}
	GtkButton {
	  border:solid 10px;
	  border-color: #000000;
	  background-color: transparent;
	  -moz-border-radius: 40px;
	  -webkit-border-radius: 40px;
	  border-radius: 40px;
  
	}
	GtkButton:focus {
	  border:solid 10px;
	  border-color: #FBC112;
	}
	GtkGrid {
	  border-color:#000000;
	  background-color: #000000;
	}
	GtkFrame{
	  border-color:#000000;
	  border-color: transparent;
	  border-width: 0;
	}
	"""   

	style_provider = Gtk.CssProvider()
	#style_provider.load_from_data(css)
	style_provider.load_from_data(bytes(css.encode()))

	Gtk.StyleContext.add_provider_for_screen(
	  Gdk.Screen.get_default(),
	  style_provider,
	  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION

	)


  gtk_style()

  win = MyWindow()
  win.connect("delete-event", Gtk.main_quit)
 
  win.show_all()
  GObject.timeout_add(200, win.update)
  Gtk.main()


if __name__ == "__main__":
  main(sys.argv)
