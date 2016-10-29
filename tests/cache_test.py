from time import sleep
import os.path
from sys import *
from pysol import *


def on_msg(instance, msg):
	print "msg on inst: "   , instance.name 
	print "\tDest: "	, msg.destination
	print "\tLength: "      , str(msg.buflen)
	print "\tredelivered: " , str(msg.redelivered_flag)
	print "\tdiscard: "     , str(msg.discard_flag)
	print "\treq-id: "      , str(msg.req_id)
	print "\tflow-id: "     , str(msg.flow)
	print "\tid: "          , str(msg.id)

def on_err(instance, err):
	print "err on inst: " , instance.name
	print "\tfn-name: "   , err.fn_name
	print "\trc-str: "    , err.rc_str
	print "\tsc-str: "    , err.sc_str
	print "\terr-str: "   , err.err_str


if len(argv) < 2:
	print "\n\tUSAGE: " + argv[0] + " <file.properties>\n"
	exit(0)
if not os.path.isfile(argv[1]):
	print "\n\tFile " + argv[1] + " could not be found.\n"
	exit(0)

# See the direct_test for info about the setup

solinst = Pysol( on_msg, on_error, None, None )

rc     = solinst.connect( argv[1] )

rc     = solinst.send_direct( "cache/topic/1", "hello",   5 )
rc     = solinst.send_direct( "cache/topic/2", "goodbye", 7 )
rc     = solinst.send_direct( "cache/topic/3", "hello",   5 )

sleep(1)

# Request top-level wildcard match against the cache
rc     = solinst.cache_req( "pysolcache", "cache/topic/>", 54321)
rc     = solinst.disconnect( )

print "DONE"

