import ctypes
import os
import platform
import Queue
import threading
from pysol_data import *

def _loaddll():
	plsys = platform.system()
	if 'Windows' in plsys:
		return ctypes.cdll.LoadLibrary('sol_wrap.dll')
	elif 'Darwin' in plsys:
	    return ctypes.cdll.LoadLibrary('libsol_wrap.dylib')
	else:
	    return ctypes.cdll.LoadLibrary('libsol_wrap.so')

dll_ = _loaddll()

# message event callback function
# - = - = - = - = - = - = - = - = -
@msg_cb_type
def on_msg(solhdl, msg_p):
	msg = msg_p[0] # dereferences the pointer
	inst = ctypes.cast(msg.user_data, POINTER(ctypes.py_object)).contents.value
	if inst._msg_cb is not None:
		inst._msg_cb( inst, msg )
	else:
		inst._msg_q.put( msg )
		inst._q_evt.set()

# error event callback function
# - = - = - = - = - = - = - = - = -
@err_cb_type
def on_err(solhdl, err_p):
	err = err_p[0] # dereferences the pointer
	inst = ctypes.cast(err.user_data, POINTER(ctypes.py_object)).contents.value
	if inst._err_cb is not None:
		inst._err_cb( inst, err )

# publisher event callback function
# - = - = - = - = - = - = - = - = -
@pub_cb_type
def on_pub_evt(solhdl, pub_evt_p):
	pub_evt = pub_evt_p[0] # dereferences the pointer
	inst = ctypes.cast(pub_evt.user_data, POINTER(ctypes.py_object)).contents.value
	if inst._pub_cb is not None:
		inst._pub_cb( inst, pub_evt )

# connection event callback function
# - = - = - = - = - = - = - = - = -
@conn_cb_type
def on_conn_evt(solhdl, conn_evt_p):
	conn_evt = conn_evt_p[0] # dereferences the pointer
	inst = ctypes.cast(conn_evt.user_data, POINTER(ctypes.py_object)).contents.value
	if inst._conn_cb is not None:
		inst._conn_cb( inst, conn_evt )

class Pysol(object):
	"""
	A Python class for sending and receiving messages via a Solace Message Bus
	Attributes:
		Message Event Callback
		Error Event Callback
		Publisher Event Callback
		Connectivity Event Callback
	"""

	#                      SESSIONS
	# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -
	def __init__( self, msg_cb, err_cb, pub_cb, conn_cb ):
		self.name    = "Solace Messaging API for Python"
		self._msg_cb = msg_cb
		self._err_cb = err_cb
		self._pub_cb = pub_cb
		self._conn_cb= conn_cb
		self._msg_q  = Queue.Queue()
		self._q_evt  = threading.Event()
		self._q_evt.clear()
		c_user_data = ctypes.cast(pointer(ctypes.py_object(self)), c_void_p)
		self._solhdl =  dll_.sol_init( on_msg, on_err, on_pub_evt, on_conn_evt, cast(c_user_data, c_void_p) )

	def connect( self, props_file ):
		return dll_.sol_connect( self._solhdl, props_file )

	def disconnect( self ):
		return dll_.sol_disconnect( self._solhdl )


	#                      PUBLISHING
	# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -
	def send_direct(self, topicstr, databuf, buflen):
		return dll_.sol_send_direct( self._solhdl, topicstr, databuf, buflen )

	def send_persistent(self, destination, desttype, databuf, buflen, corr_data=c_void_p(), corrlen=0):
		return dll_.sol_send_persistent( self._solhdl, destination, desttype, databuf, buflen, corr_data, corrlen )

	#                      SUBSCRIBING
	# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -
	def subscribe_topic(self, topicstr):
		return dll_.sol_subscribe_topic( self._solhdl, topicstr )

	def unsubscribe_topic(self, topicstr):
		return dll_.sol_unsubscribe_topic(self._solhdl, topicstr)

	def bind_queue(self, queuename, fwdmode=STORE_FWD, ackmode=AUTO_ACK):
		return dll_.sol_bind_queue(self._solhdl, queuename, fwdmode, ackmode)

	def unbind_queue(self, queue):
		return dll_.sol_unbind_queue(self._solhdl, queue)

	def ack_msg(self, flowhandle, msgid):
		return dll_.sol_ack_msg(self._solhdl, flowhandle, msgid)

	#                      BLOCKING CONSUMER
	# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -
	def receive(self, timeout):
		if self._msg_q.empty():
			self._q_evt.wait( timeout )
			if self._msg_q.empty():
				self._q_evt.clear()
				return None
		self._q_evt.clear()
		return self._msg_q.get()

	#                      CACHE REQUESTS
	# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -
	def cache_req(self, cachename, topicsub, reqid):
		return dll_.sol_cache_req(self._solhdl, cachename, topicsub, reqid)
