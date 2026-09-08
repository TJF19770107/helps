import ctypes, sys
from ctypes import wintypes
winmm = ctypes.WinDLL("winmm")
v = wintypes.DWORD()
ret = winmm.waveOutGetVolume(ctypes.c_void_p(), ctypes.byref(v))
left = v.value & 0xFFFF
right = (v.value >> 16) & 0xFFFF
print("GET ret=%s L=%d%% R=%d%% raw=%d" % (ret, round(left/65535*100), round(right/65535*100), v.value))
# 设置到 80%
target = int(65535 * 0.8)
ret2 = winmm.waveOutSetVolume(ctypes.c_void_p(), target | (target << 16))
print("SET ret=%s -> 80%%" % ret2)
v2 = wintypes.DWORD()
winmm.waveOutGetVolume(ctypes.c_void_p(), ctypes.byref(v2))
print("AFTER L=%d%% R=%d%%" % (round((v2.value&0xFFFF)/65535*100), round(((v2.value>>16)&0xFFFF)/65535*100)))