from time import sleep
import os.path
from ctypes import *
from sys import *
from marshal import *
from pysol import *

if len(argv) < 2:
	print "\n\tUSAGE: " + argv[0] + " <file.properties>\n"
	exit(0)
if not os.path.isfile(argv[1]):
	print "\n\tFile " + argv[1] + " could not be found.\n"
	exit(0)

def on_msg(instance, msg):
	data = string_at(msg.buffer, msg.buflen)
	print "Msg on inst: "   , instance.name
	print "\tDestination: " , msg.destination
	print "\tData: "	, data
	print "\tLength: "      , msg.buflen
	print "\tredelivered: " , msg.redelivered_flag
	print "\tdiscard: "     , msg.discard_flag
	print "\tid: "          , msg.id

def on_err(instance, err):
	print "Err on inst:", instance.name
	print "\tfn-name: " , err.fn_name
	print "\trc-str: "  , err.rc_str
	print "\tsc-str: "  , err.sc_str
	print "\terr-str: " , err.err_str

def on_pub_evt(instance, pub_evt):
	print "PubEvent on inst: " , instance.name
	if pub_evt.type == REJECT:
		print "\tRuh-roh, Rejected!"
	else:
		print "\tACK!"
		corid = cast(pub_evt.corr_data, POINTER(c_int))
		print "\tCorrelation: " + str(corid[0])

def on_conn_evt(instance, conn_evt):
	print "ConnEvent on " , instance.name

solinst = Pysol( on_msg, on_err, on_pub_evt, on_conn_evt )

rc     = solinst.connect( argv[1] )

if rc == SOLCLIENT_OK:
    print "Connected!"

    # Subscribe to non-guaranteed messages via a topic-expression
    subscr = "direct/topic/>"
    print "Subscribing to " + subscr
    rc     = solinst.subscribe_topic( subscr )

    i      = "hello world" 
    rc     = solinst.send_direct( "direct/topic/1", i, len(i)+1 )

    rc     = solinst.unsubscribe_topic( subscr )

    sleep(2)

    rc     = solinst.disconnect( )
else:
    print "OH NOES! Failed to connect; return code is " + str(rc)

print "DONE"

