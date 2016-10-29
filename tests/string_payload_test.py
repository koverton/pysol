from time import sleep
import os.path
from ctypes import *
from sys import *
from marshal import *
from pysol import *


# message event callback function
# - = - = - = - = - = - = - = - = -
def on_msg(instance, msg):
	data = string_at(msg.buffer, msg.buflen)
	print "msg on inst: " , instance.name
	print "\tDestination: " , msg.destination
	print "\tData: "	, data
	print "\tLength: "      , msg.buflen
	print "\tredelivered: " , msg.redelivered_flag
	print "\tdiscard: "     , msg.discard_flag
	print "\tid: "          , msg.id

# error event callback function
# - = - = - = - = - = - = - = - = -
def on_err(instance, err):
	print "error on inst: " + instance.name
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

if rc == SOLCLIENT_OK:
    print "Connected!"

    # Subscribe to non-guaranteed messages via a topic-expression
    subscr = "direct/topic/>"
    print  "Subscribing to " + subscr
    rc     = solinst.subscribe_topic( subscr )

    s      = "hello world" 
    rc     = solinst.send_direct( "direct/topic/1", s, len(s)+1 )
    rc     = solinst.unsubscribe_topic( subscr )

    sleep(2)

    rc     = solinst.disconnect( )
else:
    print "OH NOES! Failed to connect; return code is " + str(rc)

print "DONE"

