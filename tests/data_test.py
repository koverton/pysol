from pysol import *

print "Testing msg_evt_type"
# test message event type
udata   = c_char_p('session user data')
msg     = c_char_p('whatever')
topic_p = c_char_p('topic/string/1')
queue_p = c_char_p('queue_one')
msg_evt = msg_evt_type(TOPIC, topic_p, 12345, 67890, cast(msg,c_void_p), 9, 321, 0, 0, cast(udata, c_void_p) )
print "Done"

# test error event type
print "Testing err_evt_type"
fnname  = c_char_p('whatever')
rcstr   = c_char_p('return code string')
scstr   = c_char_p('sub-code string')
errstr  = c_char_p('error string')
err_evt = err_evt_type(fnname, 1, rcstr, 2, scstr, 3, errstr, cast(udata, c_void_p))
print "Done"

# test publisher event type
print "Testing pub_evt_type"
corr    = c_char_p('correlation pointer 1')
pub_evt = pub_evt_type(REJECT, cast(corr, c_void_p), cast(udata, c_void_p))
print "Done"

# test connectivity event type
print "Testing conn_evt_type"
udata   = c_char_p('session user data')
conn_evt = conn_evt_type(UP, cast(udata, c_void_p))
print "Done"
