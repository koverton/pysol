import os.path
from time import sleep
from sys import *
from pysol import *


# message event callback function
# - = - = - = - = - = - = - = - = -
def on_msg(instance, msg):
	data = string_at(msg.buffer, msg.buflen)
	print "msg on inst: "   , instance.name
	print "\tDestination: " , msg.destination
	print "\tData: "	, data
	print "\tredelivered: " , msg.redelivered_flag
	print "\tdiscard: "     , msg.discard_flag
	print "\treq-id: "      , msg.req_id
	print "\tflow-id: "     , msg.flow
	print "\tid: "          , msg.id

# error event callback function
# - = - = - = - = - = - = - = - = -
def on_err(instance, err):
	print "err on inst: ", instance.name
	print "\tfn-name: "  , err.fn_name
	print "\trc-str: "   , err.rc_str
	print "\tsc-str: "   , err.sc_str
	print "\terr-str: "  , err.err_str


if len(argv) < 2:
	print "\n\tUSAGE: " + argv[0] + " <file.properties>\n"
	exit(0)
if not os.path.isfile(argv[1]):
	print "\n\tFile " + argv[1] + " could not be found.\n"
	exit(0)


solinst = Pysol( on_msg, on_err, None, None )
rc     = solinst.connect( argv[1] )
print "Connected!"


# Bind to a guaranteed queue via a specific named-queue with default modes store-and-fwd and auto-ack
qname  = "q0"
print "Binding to " + qname
rc     = solinst.bind_queue( qname )
print "BOUND to " + qname

# Correlate publisher events back to each sent message via a correlation data-ptr 
# that is passed back in the publisher-events for each ack'd message
s = "hello"
cordata= []
for x in range(0, 3):
	cordata.append( c_int(100+x) )
	rc = solinst.send_persistent( qname, QUEUE, s, len(s)+1 )

sleep(2)

rc     = solinst.unbind_queue( qname )

rc     = solinst.disconnect( )

print "DONE"

