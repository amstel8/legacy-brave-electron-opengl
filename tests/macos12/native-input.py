import ctypes as c,sys,json,plistlib,time
cg=c.CDLL('/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics');cf=c.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
class Point(c.Structure):_fields_=[('x',c.c_double),('y',c.c_double)]
cg.CGEventCreateMouseEvent.argtypes=[c.c_void_p,c.c_uint32,Point,c.c_uint32];cg.CGEventCreateMouseEvent.restype=c.c_void_p
cg.CGEventPost.argtypes=[c.c_uint32,c.c_void_p]
cg.CGEventCreateKeyboardEvent.argtypes=[c.c_void_p,c.c_ushort,c.c_bool];cg.CGEventCreateKeyboardEvent.restype=c.c_void_p
cg.CGEventSetFlags.argtypes=[c.c_void_p,c.c_ulonglong]
cf.CFRelease.argtypes=[c.c_void_p]
def post(e):cg.CGEventPost(0,e);cf.CFRelease(e)
mode=sys.argv[1]
if mode in ('click','move','rightclick'):
 p=Point(float(sys.argv[2]),float(sys.argv[3]));post(cg.CGEventCreateMouseEvent(None,5,p,0));time.sleep(.12)
 if mode in ('click','rightclick'):
  button=1 if mode=='rightclick' else 0;down=3 if button else 1;up=4 if button else 2
  post(cg.CGEventCreateMouseEvent(None,down,p,button));time.sleep(.08);post(cg.CGEventCreateMouseEvent(None,up,p,button))
elif mode=='hover':
 x,y=map(float,sys.argv[2:4])
 for dx in (-3,3,0):
  post(cg.CGEventCreateMouseEvent(None,5,Point(x+dx,y),0));time.sleep(.1)
elif mode=='drag':
 x,y,tx,ty=map(float,sys.argv[2:6]);p=Point(x,y);post(cg.CGEventCreateMouseEvent(None,5,p,0));time.sleep(.1);post(cg.CGEventCreateMouseEvent(None,1,p,0))
 for i in range(1,16):
  post(cg.CGEventCreateMouseEvent(None,6,Point(x+(tx-x)*i/15,y+(ty-y)*i/15),0));time.sleep(.03)
 post(cg.CGEventCreateMouseEvent(None,2,Point(tx,ty),0))
elif mode=='key':
 for down in (True,False):
  e=cg.CGEventCreateKeyboardEvent(None,int(sys.argv[2]),down);cg.CGEventSetFlags(e,int(sys.argv[3]));post(e);time.sleep(.08)
elif mode=='windows':
 cg.CGWindowListCopyWindowInfo.argtypes=[c.c_uint32,c.c_uint32];cg.CGWindowListCopyWindowInfo.restype=c.c_void_p
 cf.CFPropertyListCreateData.argtypes=[c.c_void_p,c.c_void_p,c.c_long,c.c_ulong,c.c_void_p];cf.CFPropertyListCreateData.restype=c.c_void_p
 cf.CFDataGetLength.argtypes=[c.c_void_p];cf.CFDataGetLength.restype=c.c_long
 cf.CFDataGetBytePtr.argtypes=[c.c_void_p];cf.CFDataGetBytePtr.restype=c.c_void_p
 a=cg.CGWindowListCopyWindowInfo(1,0);d=cf.CFPropertyListCreateData(None,a,100,0,None)
 v=plistlib.loads(c.string_at(cf.CFDataGetBytePtr(d),cf.CFDataGetLength(d)))
 print(json.dumps([{k:x.get(k) for k in ('kCGWindowNumber','kCGWindowOwnerPID','kCGWindowBounds','kCGWindowLayer')} for x in v if x.get('kCGWindowOwnerPID')==int(sys.argv[2])]))
