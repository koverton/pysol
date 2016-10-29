import os.path
from time import sleep
from sys import *
from pysol import *


# message event callback function
# - = - = - = - = - = - = - = - = -
def on_msg(instance, msg):
	data = string_at(msg.buffer, msg.buflen)
	print "msg on inst: " , instance.name
	print "\tData: "	, data
	print "\tLength: "      , msg.buflen
	print "\tredelivered: " , msg.redelivered_flag
	print "\tdiscard: "     , msg.discard_flag
	print "\treq-id: "      , msg.req_id
	print "\tflow-id: "     , msg.flow
	print "\tid: "          , msg.id
	print "\nACKing the msg"
	instance.ack_msg( msg.flow, msg.id )

# error event callback function
# - = - = - = - = - = - = - = - = -
def on_err(instance, err):
	print "error on inst: " , instance.name
	print "\tfn-name: " , err.fn_name
	print "\trc-str: "  , err.rc_str
	print "\tsc-str: "  , err.sc_str
	print "\terr-str: " , err.err_str

# publisher event callback function
# - = - = - = - = - = - = - = - = -
def on_pub_evt(instance, pub_evt):
	print "pub-event on inst: " + instance.name
	if pub_evt.type == REJECT:
		print "\tRuh-roh, Rejected!"
	else:
		print "\tACK!"
		corid = cast(pub_evt.corr_data, POINTER(c_int))
		print "\tCorrelation: " , corid[0]

# connection event callback function
# - = - = - = - = - = - = - = - = -
def on_conn_evt(instance, conn_evt):
	print "conn-event on inst: " + instance.name



if len(argv) < 2:
	print "\n\tUSAGE: " + argv[0] + " <file.properties>\n"
	exit(0)
if not os.path.isfile(argv[1]):
	print "\n\tFile " + argv[1] + " could not be found.\n"
	exit(0)


solinst = Pysol( on_msg, on_err, on_pub_evt, on_conn_evt )
rc     = solinst.connect( argv[1] )
print "Connected!"


# Bind to a guaranteed queue via a specific named-queue
qname  = "q0"
print "Binding to " + qname
rc     = solinst.bind_queue( qname, STORE_FWD, MANUAL_ACK )
print "BOUND to " + qname

# Correlate publisher events back to each sent message via a correlation data-ptr 
# that is passed back in the publisher-events for each ack'd message
s = "hello"
cordata= []
for x in range(0, 3):
	cordata.append( c_int(100+x) )
	rc = solinst.send_persistent( qname, QUEUE, s, len(s)+1, byref(cordata[x]), getsizeof(x) )

sleep(2)

rc = solinst.unbind_queue( qname )

rc = solinst.disconnect( )

print "DONE"

