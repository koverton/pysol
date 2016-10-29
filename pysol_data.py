from ctypes import *

#                      PRIMITIVE TYPES
# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -

solhandle_type = c_void_p
flowhandle_type= c_uint64


#                      ENUM VALUES
# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -

#fwd_mode
STORE_FWD   = 1
CUT_THRU    = 2

#ack_mode
AUTO_ACK    = 1
MANUAL_ACK  = 2

# destination type
TOPIC       = 1
QUEUE       = 2
NONE        = 3

# publisher event type
ACK         = 1
REJECT      = 2

# connectivity event type 
UP          = 1
RECONNECTING= 2
RECONNECTED = 3
DOWN        = 4

# return codes
SOLCLIENT_FAIL = -1
SOLCLIENT_OK = 0
SOLCLIENT_WOULD_BLOCK = 1
SOLCLIENT_IN_PROGRESS = 2
SOLCLIENT_NOT_READY = 3
SOLCLIENT_EOS  = 4
SOLCLIENT_NOT_FOUND = 5
SOLCLIENT_NOEVENT = 6
SOLCLIENT_INCOMPLETE = 7
SOLCLIENT_ROLLBACK = 8

#                      MESSAGE EVENT
# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -

class msg_evt_type (Structure):
	_fields_ = [
		('desttype',        c_int32),
		('destination',     c_char_p),
		('flow',            flowhandle_type),
		('id',              solhandle_type),
		('buffer',          c_void_p),
		('buflen',          c_uint32),
		('req_id',          c_int32 ),
		('redelivered_flag',c_int32 ),
		('discard_flag',    c_int32 ),
		('user_data',       c_void_p)
	]

msg_cb_type = CFUNCTYPE(c_void_p, solhandle_type, POINTER(msg_evt_type))


#                      ERROR EVENT
# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -

class err_evt_type (Structure): 
	_fields_ = [
		('fn_name',    c_char_p),
		('return_code',c_int32 ),
		('rc_str',     c_char_p),
		('sub_code',   c_int32 ),
		('sc_str',     c_char_p), 
		('resp_code',  c_int32 ),
		('err_str',    c_char_p),
		('user_data',  c_void_p)
	]

err_cb_type = CFUNCTYPE(c_void_p, solhandle_type, POINTER(err_evt_type))


#                      PUBLISHER EVENT
# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -

class pub_evt_type (Structure):
	_fields_ = [
		('type',     c_int32 ),
		('corr_data',c_void_p),
		('user_data',c_void_p)
	]

pub_cb_type = CFUNCTYPE(c_void_p, solhandle_type, POINTER(pub_evt_type))


#                      CONNECTIVITY EVENT
# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -

class conn_evt_type (Structure): 
	_fields_ = [
		('type',      c_int32 ),
		('user_data', c_void_p)
	]

conn_cb_type = CFUNCTYPE(c_void_p, solhandle_type, POINTER(conn_evt_type))


#                      CALLBACKS ARGUMENT TYPE
# - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = - = -

class cb_funcs_type (Structure): 
	_fields_ = [
		('msg_cb',    msg_cb_type ),
		('err_cb',    err_cb_type ),
		('pub_cb',    pub_cb_type ),
		('conn_cb',   conn_cb_type),
		('user_data', c_void_p    )
	]

