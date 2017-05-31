#-*- coding:utf-8 -*-
#!/usr/bin/python

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
url_video_category = 'https://5uwrj54ff1.execute-api.us-east-1.amazonaws.com/dev/categories'
u2 = urllib.urlopen(url_video_category)
video = json.loads(u2.read())

pxbf_home = ""
pxbf_video= ""
pxbf_cam= ""
pxbf_face= ""
pxbf_gallary= ""
pxbf_setting= ""

ctldata = ""

flag_ok=False

flag_video=False
flag_category =False
flag_camera=False
flag_gallary=False
flag_show_video=False
flag_show_gallary=False
flag_facial=False 

file=""
font = Pango.FontDescription('Latha 50')

cam_thread=""

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
		cam.set_from_pixbuf(pxbf_cam)
		cam.show()
		frame2 = Gtk.Frame()
		frame2.show()
		frame2.add(cam)

		b_cam = Gtk.Button()
		b_cam.add(frame2)
		b_cam.show()

		b_cam.connect("clicked", self.on_button_show_backhead_background)
		buttonbox.add(b_cam)

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
		
		image_bg = Gtk.Image()		
		image_bg.set_from_file("/home/pi/button/black.png")
		image_bg.show()
		
		# a grid to attach the widget
 
		grid_bg = Gtk.Grid(row_homogeneous=True, 
						column_spacing=0, row_spacing=1)
		grid_bg.attach(image_bg, 0, 0, 7, 4)
		self.facial_window.add(grid_bg)
		self.facial_window.show_all()

		facial_thread = threading.Thread(target=self.facial_test)
		facial_thread.daemon = True
		facial_thread.start()


	def facial_test(self):
		subprocess.call('python facial_test.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1', shell=True)



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
					url_video_list = 'https://5uwrj54ff1.execute-api.us-east-1.amazonaws.com/dev/category?id=' + video['list'][i]['id']
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
			for i in range(len(video['list'])):																								
	
				if convert == video_list['list'][i]['name']:																	
					url_youtube = 'https://youtube.com/watch?v='+ video_list['list'][i]['video_id']																																		
					subprocess.call ("omxplayer --win '110, 0, 690, 386' `youtube-dl -g "+ url_youtube +"`", shell=True)																
	
			self.play_window.destroy()


	def on_button_show_backhead_background(self, widget):
		global flag_camera


		flag_camera= True

		self.backhead_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		self.backhead_window.fullscreen()  

		overlay = Gtk.Overlay()
		self.backhead_window.add(overlay)
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
		self.backhead_window.show_all()

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

	aws_access_key_id = 'AKIAJ37RQ65RC5XNSC6Q'
	aws_secret_access_key = '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'
	bucket = 'godori-image'
	key = 'origin/'+file.name

	try:
		size = os.fstat(file.fileno()).st_size
	except:
		# Not all file objects implement fileno(),
		# so we fall back on this
		file.seek(0, os.SEEK_END)
		size = file.tell()

	conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
	bucket = conn.get_bucket(bucket, validate=True)
	k = Key(bucket)
	k.key = key

	if content_type:
		k.set_metadata('Content-Type', content_type)
	sent = k.set_contents_from_file(file, cb=callback, md5=md5, reduced_redundancy=reduced_redundancy, rewind=True)
	k.set_acl('public-read')

	# Rewind for later use
	file.seek(0)
 

#video recording and stroe
def Camera():
	global flag
	global flag_photo
	global flag_camera
	global filename
	global file

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

				subprocess.call('mv '+filename+' /home/pi/syeon/', shell=True)
				flag_photo = False
			else : time.sleep(0.1)


		camera.stop_preview()
		print " outout"	
	


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
				ctldata = client_sock.recv(1024)

				device = uinput.Device([
					uinput.KEY_RIGHT,
					uinput.KEY_LEFT,
					uinput.KEY_UP,
					uinput.KEY_DOWN,
					uinput.KEY_ENTER,
					uinput.KEY_H
					])
				if len(ctldata) != 0: 
					#print ctldata
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
							win.play_window.destroy()
							flag_video= True
						elif flag_camera:
							#flag=True
							print "in ok"
							flag_camera =False
							flag_photo = False
							win.backhead_window.destroy()
							print "out ok"
						elif flag_gallary:
							flag_gallary=False
							win.gallary_window.destroy()
						elif flag_show_gallary:
							flag_show_gallary=False
							win.show_gallary_window.destroy()
							flag_gallary=True
						elif flag_facial:
							flag_facial =False
							device.emit_click(uinput.KEY_H)
							win.facial_window.destroy()
					elif ctldata =='PLAY\n':
						subprocess.call('/home/pi/omxplayer/dbuscontrol.sh pause', shell=True)
					elif ctldata == 'FF\n':
						subprocess.call('/home/pi/omxplayer/dbuscontrol.sh seek 5000000', shell=True)
					elif ctldata == 'RW\n':
						subprocess.call('/home/pi/omxplayer/dbuscontrol.sh seek -5000000', shell=True)
				
				else:	
					break
			
	# raise an exception if there was any error
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
		GtkListStore {
			border-color: #000000;
			background-color: #000000;
		}
		GtkListStore:focus{
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
