# desktop_effects_v2_92_mega.py
import win32gui, win32con, win32api, random, time, math, threading, msvcrt

STAGES = 600
STOP_POLL_INTERVAL = 0.015

def get_desktop_dc():
    hwnd = win32gui.GetDesktopWindow()
    return win32gui.GetDC(hwnd)

def random_color():
    return win32api.RGB(random.randint(0,255),
                        random.randint(0,255),
                        random.randint(0,255))

# --- Mega Effects ---

def pixelate(hdc,w,h,stop_event=None):
    sw,sh=max(1,w//6),max(1,h//6)
    for _ in range(50):
        if stop_event and stop_event.is_set(): return
        win32gui.StretchBlt(hdc,0,0,sw,sh,hdc,0,0,w,h,win32con.SRCCOPY)
        win32gui.StretchBlt(hdc,0,0,w,h,hdc,0,0,sw,sh,win32con.SRCCOPY)
        time.sleep(0.02)

def bouncing_squares(hdc,w,h,stop_event=None):
    x,y,dx,dy=w//2,h//2,20,16
    size=60
    for _ in range(100):
        if stop_event and stop_event.is_set(): return
        x+=dx; y+=dy
        if x<0 or x>w-size: dx*=-1
        if y<0 or y>h-size: dy*=-1
        brush=win32gui.CreateSolidBrush(random_color())
        win32gui.FillRect(hdc,(x,y,x+size,y+size),brush)
        win32gui.DeleteObject(brush)
        time.sleep(0.008)

def swirling_triangles(hdc,w,h,stop_event=None):
    for _ in range(80):
        if stop_event and stop_event.is_set(): return
        pts=[(random.randint(0,w),random.randint(0,h)) for _ in range(3)]
        brush=win32gui.CreateSolidBrush(random_color())
        win32gui.Polygon(hdc,pts)
        win32gui.DeleteObject(brush)
        time.sleep(0.005)

def flashing_lines(hdc,w,h,stop_event=None):
    for _ in range(120):
        if stop_event and stop_event.is_set(): return
        x1,y1=random.randint(0,w),random.randint(0,h)
        x2,y2=random.randint(0,w),random.randint(0,h)
        pen=win32gui.CreatePen(win32con.PS_SOLID,2,random_color())
        old_pen=win32gui.SelectObject(hdc,pen)
        win32gui.MoveToEx(hdc,x1,y1)
        win32gui.LineTo(hdc,x2,y2)
        win32gui.SelectObject(hdc,old_pen)
        win32gui.DeleteObject(pen)
        time.sleep(0.004)

def crazy_blits(hdc,w,h,stop_event=None):
    for _ in range(80):
        if stop_event and stop_event.is_set(): return
        ox,oy=random.randint(-50,50),random.randint(-50,50)
        try: win32gui.BitBlt(hdc,ox,oy,max(0,w-abs(ox)),max(0,h-abs(oy)),hdc,0,0,win32con.SRCCOPY)
        except: pass
        time.sleep(0.003)

def spin_shift(hdc,w,h,stop_event=None):
    cx,cy=w//2,h//2
    for i in range(60):
        if stop_event and stop_event.is_set(): return
        angle=math.radians(i*6)
        dx=int(40*math.cos(angle))
        dy=int(40*math.sin(angle))
        try: win32gui.BitBlt(hdc,cx-dx,cy-dy,w-abs(dx),h-abs(dy),hdc,0,0,win32con.SRCCOPY)
        except: pass
        time.sleep(0.01)

def ripple_effect(hdc,w,h,stop_event=None):
    for i in range(50):
        if stop_event and stop_event.is_set(): return
        offset=random.randint(-30,30)
        try: win32gui.BitBlt(hdc,offset,offset,w-abs(offset),h-abs(offset),hdc,0,0,win32con.SRCCOPY)
        except: pass
        time.sleep(0.008)

def color_wave(hdc,w,h,stop_event=None):
    for _ in range(70):
        if stop_event and stop_event.is_set(): return
        brush=win32gui.CreateSolidBrush(random_color())
        x1=random.randint(0,w-100)
        y1=random.randint(0,h-100)
        win32gui.FillRect(hdc,(x1,y1,x1+100,y1+100),brush)
        win32gui.DeleteObject(brush)
        time.sleep(0.006)

# --- Ultimate Mix (multiple effects per stage) ---
def ultimate_mix(hdc,w,h,stop_event=None):
    effects=[pixelate,bouncing_squares,swirling_triangles,flashing_lines,crazy_blits,spin_shift,ripple_effect,color_wave]
    for _ in range(200):
        if stop_event and stop_event.is_set(): return
        choice=random.sample(effects, k=random.randint(2,4))
        threads=[]
        for effect in choice:
            t=threading.Thread(target=effect,args=(hdc,w,h,stop_event))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        time.sleep(0.005)

# --- Stage manager ---
def run_stage(stage,hdc,w,h,stop_event):
    if stop_event.is_set(): return
    if stage<=10: pixelate(hdc,w,h,stop_event=stop_event)
    elif stage<=20: bouncing_squares(hdc,w,h,stop_event=stop_event)
    elif stage<=30: swirling_triangles(hdc,w,h,stop_event=stop_event)
    elif stage<=40: flashing_lines(hdc,w,h,stop_event=stop_event)
    elif stage%15==0: spin_shift(hdc,w,h,stop_event=stop_event)
    else: ultimate_mix(hdc,w,h,stop_event=stop_event)

# --- Boss key ---
def boss_key_monitor(stop_event):
    try:
        while not stop_event.is_set():
            if msvcrt.kbhit() and msvcrt.getwch().lower()=='b':
                stop_event.set()
                return
            time.sleep(STOP_POLL_INTERVAL)
    except: stop_event.set()

# --- Main ---
def main():
    print("⚡ Mega Desktop Effects v2.92.332.44.990.33.21 ⚡")
    print("Ctrl+C or 'B' in this console to stop.")
    stop_event=threading.Event()
    hdc=get_desktop_dc()
    w,h=win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1)
    threading.Thread(target=boss_key_monitor,args=(stop_event,),daemon=True).start()
    
    try:
        for stage in range(1,STAGES+1):
            if stop_event.is_set(): break
            run_stage(stage,hdc,w,h,stop_event)
    except KeyboardInterrupt: stop_event.set()
    finally:
        try: win32gui.ReleaseDC(win32gui.GetDesktopWindow(),hdc)
        except: pass
        print("✅ Desktop restored. Effects stopped.")

if __name__=="__main__":
    main()
