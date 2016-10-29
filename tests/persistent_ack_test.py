import os.path
from time import sleep
from sys import *
from pysol import *


# message event callback function
# - = - = - = - = - = - = - = - = -
def on_msg(instance, msg):
	data = string_at(msg.buffer, msg.buflen)
	print "msg on instance: ", instance.name
	print "\tDestination: " , msg.destination
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



if len(argv) < 2:
	print "\n\tUSAGE: " + argv[0] + " <file.properties>\n"
	exit(0)
if not os.path.isfile(argv[1]):
	print "\n\tFile " + argv[1] + " could not be found.\n"
	exit(0)


solinst = Pysol( on_msg, on_err, None, None )
rc     = solinst.connect( argv[1] )
print "Connected!"


# Bind to a guaranteed queue via a specific named-queue
qname  = "q0"
print "Binding to " + qname
rc     = solinst.bind_queue( qname, STORE_FWD, MANUAL_ACK )
print "BOUND to " + qname

s = "hello"

# Simple persistent send without streaming correlation data
for x in range(0, 3):
	# Send to named queue
	rc = solinst.send_persistent( qname, QUEUE, s, len(s)+1 )
	# Send to mapped topic
	rc = solinst.send_persistent( "q0/mapped/1", TOPIC, s, len(s)+1 )

sleep(2)

rc     = solinst.unbind_queue( qname )

rc     = solinst.disconnect( )

print "DONE"

