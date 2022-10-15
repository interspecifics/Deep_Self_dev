#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
deepself_dataserver
------------------------------------------------------------------------------------
 ___________
|▒▒▒▒▒▒▒▒▒▒▒|
|===========|
|-----------|
|___________|


Usa el botón en la parte inferior derecha para cambiar entre el modo SEQUENCE y el modo LOOP

[SEQUENCE]:
    Recorre cada segmento en orden secuencial, cuando llega al ultimo, reinicia

[LOOP]:
    Recorre unicamente la lista de segmentos listado bajo el botón
    + Añade nuevos segmentos haciendo clic sobre ellos
    - Remueve los segmentos de la lista haciendo clic con el BOTON SECUNDARIO del mouse

"""

from locale import normalize
from operator import truediv
import queue
from random import randint, random
import pygame
import json, time
from oscpy.client import OSCClient
import numpy as np
from glob import glob


# -     ----------------------- ----------------------- -----------------------



# -[osc] 
osc_host = "127.0.0.1"
osc_port = 8000
OSC_CLIENT = OSCClient(osc_host, osc_port)

# - select data file  ---- | HERE |
DATA_I = 29



# -[data]
DATA_DIR = "./tracks/"
dfs = glob(DATA_DIR+"*.json")
print("{} archivos encontrados: ".format(len(dfs)))
for i,df in enumerate(dfs):
    print("{}: {}".format(i, df))
#
DATA_PATH = dfs[DATA_I]


# -     ----------------------- ----------------------- -----------------------
# - | 0B  | -visualize the track



emo = ["BoredSleepy",   "Contempt", "Sadness",  "Joy",
        "RelaxNeutral", "Love",     "Anger",    "TenseStress",
        "Fear",         "Surprise"]

emocolors = [[2, 3, 226],   [0, 191, 254],  [25, 167, 0],   [8, 255, 8],
            [207, 255, 0],  [255, 0, 204],  [254, 0, 2],    [252, 100, 45],
            [202, 1, 71],   [255, 4, 144]
            ]



# -     ----------------------- ----------------------- -----------------------


class MiniTrack():
    def __init__(self, _chunk, _nt):
        self.vad = _chunk['vad']
        self.emo = _chunk['emo']
        self.ss = _chunk['samples']
        self.nt = _nt
        self.ssa = np.array(self.ss)
        self.ss_max =  self.ssa.max(0).tolist()
        self.ss_min =  self.ssa.min(0).tolist()
        self.ss_mean =  self.ssa.mean(0).tolist()
        #print("{} - {}".format(self.ss_max, self.ss_min))
        self.i = 0
        self.current = self.ss[self.i]
        self.current_norm = self.ss[self.i]
        self.pxx = 0
        return

    def update(self):
        #self.i = self.i + 1 if self.i<len(self.ss)-1 else 0
        self.i = self.i + 1
        self.current = self.ss[self.i]
        self.current_norm = [pmap(self.current[c], self.ss_min[c], self.ss_max[c], 0, 1) for c in range(len(self.current))]
        return

    def draw(self, _surface, _x, _y):
        #pygame.draw.rect(surface, (0,0,32), pygame.Rect(posit[0], posit[1], shape[0], shape[1]), 0)
        # big surface for emotion
        s = pygame.Surface((64,16), pygame.SRCALPHA)
        alp = pmap(self.emo[2], 0 , 1, 0, 255)
        s.fill(tuple(emocolors[self.emo[1]] + [alp]))       # set the alpa
        _surface.blit(s, (_x, _y))
        # lines across x
        color_pix = [(224, 176, 255), (181, 110, 220), (143, 0, 241)]
        #print ("{},{}".format(self.nt, len(self.ss)))
        for i in range(int(len(self.ss)/4)+1):
            for j in range(len(self.ss[i])):
                # 5 elek [df_pro.AF3[s], df_pro.T7[s], df_pro.Pz[s], df_pro.T8[s], df_pro.AF4[s]]
                # 4 icas [df_pro.ICA_1[s], df_pro.ICA_2[s], df_pro.ICA_3[s], df_pro.ICA_4[s]]
                # 6 freq [df_pro.alpha_ICA_1[s], df_pro.beta_l_ICA_1[s], df_pro.beta_h_ICA_1[s], df_pro.gamma_ICA_1[s], df_pro.delta_ICA_1[s], df_pro.theta_ICA_1[s]]
                color = color_pix[0] if j < 5 else color_pix[1] if j < 9 else color_pix[2]
                pix = pygame.Surface((2,1), pygame.SRCALPHA)
                iii = i*4 if (i*4)<127 else 127
                #print ("{}".format(i))
                alp = pmap(self.ss[iii][j], self.ss_min[j], self.ss_max[j], 0, 255)
                pix.fill(tuple(color + tuple([alp])))
                _surface.blit(pix, (_x + 2*i, _y + 17 + j))
        return

    def draw_big(self, _surface, _x, _y, _szx = 8, _szy=5):
        # big line for emotion
        s = pygame.Surface((128*_szx,16), pygame.SRCALPHA)
        alp = pmap(self.emo[2], 0 , 1, 0, 255)
        s.fill(tuple(emocolors[self.emo[1]] + [alp]))       # set the alpa
        _surface.blit(s, (_x, _y))
        # the 127 steps
        color_pix = [(224, 176, 255), (181, 110, 220), (143, 0, 241)]
        #print ("{},{}".format(self.nt, len(self.ss)))
        for i in range(len(self.ss)+1):
            iii = i if i<127 else 126
            for j in range(len(self.ss[iii])):
                color = color_pix[0] if j < 5 else color_pix[1] if j < 9 else color_pix[2]
                pix = pygame.Surface((_szx,_szy), pygame.SRCALPHA)
                alp = pmap(self.ss[iii][j], self.ss_min[j], self.ss_max[j], 0, 255)
                pix.fill(tuple(color + tuple([alp])))
                _surface.blit(pix, (_x + _szx*i, _y + 18 + _szy*j))
        # draw the cursor!
        self.pxx = lerp(self.pxx, _x + _szx*self.i, 0.1);
        #pygame.draw.line(_surface, (255, 255, 255), (_x + _szx*self.i, _y + 18 + _szy*0), (_x + _szx*self.i, _y + 18 + _szy*16), 2)
        pygame.draw.line(_surface, (255, 255, 255), (self.pxx, _y + 18 + _szy*0), (self.pxx, _y + 18 + _szy*16), 2)
        return




class Tracktor():
    def __init__(self, _data, _wi, _he, _font_file):
        self.W = _wi
        self.H = _he
        # datas
        self.data = _data
        # normalize meta
        self.meta = []
        for d in self.data:
            self.meta.append(d['vad'])
        self.meta_a = np.array(self.meta)
        """
        print("len_meta: {}".format(self.meta_a.shape))
        print("len_meta_0: {}".format(self.meta_a[0]))
        self.meta_max =  self.meta_a.max(0).tolist()
        print("len_meta_max: {}".format(self.meta_max))
        self.meta_min =  self.meta_a.min(0).tolist()
        self.meta_mean =  self.meta_a.mean(0).tolist()
        self.meta_norm = []
        for me in self.meta_a:
            ml = [pmap(m, self.meta_min[k], self.meta_max[k], 0, 1) for k,m in enumerate(me)]
            self.meta_norm.append(ml)
        """
        # tracks
        self.n_tracks = len(self.data)
        self.tracks = [MiniTrack(self.data[_c], _c) for _c in range(len(self.data)) if len(self.data[_c]['samples'])>64]
        self.a_track = 0
        self.ttrr = self.tracks[self.a_track]
        # fonts
        self.channels = ["AF3", "T7", "PZ", "T8", "AF4", 
                        "ic_1", "ic_2", "ic_3", "ic_4",
                        "a", "bl", "bh", "g", "d", "t"]
        self.meta_ch = ["val","ars","dom",
                    "emo-n","emo-i","emo-c",]
        
        self.font_big = pygame.font.Font(_font_file, 20)
        self.font_med = pygame.font.Font(_font_file, 16)
        self.font_sml = pygame.font.Font(_font_file, 10)
        self.fonts = [self.font_sml, self.font_med, self.font_big]
        # drawing and gui layer
        self.DRAW_SCREEN = pygame.Surface((self.W, self.H),pygame.SRCALPHA, 32)
        self.DRAW_SCREEN.fill((0,0,0))
        self.GUI_SCREEN = pygame.Surface((self.W, self.H),pygame.SRCALPHA, 32)
        #self.GUI_SCREEN.fill((0,0,0,255))
        self.offset_x = 80
        self.offset_y = 40
        self.sz_x = 66
        self.sz_y = 34
        self.nx = 20
        self.ny = 20
        # modes
        self.loop = False
        self.queue = [self.a_track]
        self.qi = 0
        # buttons
        self.buttons = []
        r1_ = [1200, 680, 66*3,90]
        b1_loop = pygame.draw.rect(self.GUI_SCREEN, (255, 255, 255), pygame.Rect(r1_), 1)
        self.buttons.append(b1_loop)
        return

    def update(self):
        self.ttrr = self.tracks[self.a_track]
        # normally update current track ttrr
        if self.ttrr.i < len(self.ttrr.ss)-1:
            self.ttrr.update()
            # send_osc for track here
            self.send_osc_track(OSC_CLIENT)
        # when current track is over
        else:
            if (not self.loop):
                self.a_track = (self.a_track + 1) if (self.a_track + 2)<self.n_tracks else 0
                self.ttrr = self.tracks[self.a_track]
                self.ttrr.i = -1
                self.ttrr.pxx = self.offset_x
                self.ttrr.update()
            elif(self.loop):
                # iterate over queue
                self.qi = self.qi + 1 if (self.qi + 1) < len(self.queue) else 0
                self.a_track = self.queue[self.qi]
                self.ttrr = self.tracks[self.a_track]
                self.ttrr.i = -1
                self.ttrr.pxx = self.offset_x
                self.ttrr.update()
            # send osc for meta here
            self.send_osc_meta(OSC_CLIENT)
        return

    def draw(self):
        """        """
        self.DRAW_SCREEN.fill((0,0,0))
        for k,tr in enumerate(self.tracks):
            tr.draw(
                    self.DRAW_SCREEN, 
                    self.offset_x + (k%self.nx) * self.sz_x, 
                    self.offset_y + int(k/self.ny) * self.sz_y
                    )
        return

    def draw_mini(self):
        # make a mask on DRAW_SCREEN
        self.DRAW_SCREEN.fill((0,0,0),(0, 680, self.W, 200))
        # select actual track
        a_track = self.tracks[self.a_track]
        # draw actual track
        a_track.draw_big(self.DRAW_SCREEN, self.offset_x, self.offset_y + 640)
        return
    
    def draw_gui(self):
        # fill with transparency
        self.GUI_SCREEN.fill((255,255,255,0))
        # labels
        color_pix = [(224, 176, 255), (181, 110, 220), (143, 0, 241)]
        for i,ch in enumerate(self.ttrr.current_norm):
            color = color_pix[0] if i < 5 else color_pix[1] if i < 9 else color_pix[2]
            labl = self.fonts[1].render("[{}]:{:0.3f}".format(self.channels[i], ch), 1, color)
            if i < 5:
                rou = 0
                self.GUI_SCREEN.blit(labl, (self.offset_x + 120 * (i), self.offset_y + 740 + rou * 20))
            elif i < 9:
                rou = 1
                self.GUI_SCREEN.blit(labl, (self.offset_x + 120 * (i-5), self.offset_y + 740 + rou * 20))
            else:
                rou = 2
                self.GUI_SCREEN.blit(labl, (self.offset_x + 120 * (i-9), self.offset_y + 740 + rou * 20))
        for j,me in enumerate(self.ttrr.vad):
            #labels for the meta
            color = emocolors[self.ttrr.emo[1]]
            rou = 0
            labm = self.fonts[1].render("[{}]:{:0.3f}".format(self.meta_ch[j], me), 1, color)
            self.GUI_SCREEN.blit(labm, (self.offset_x + 600 + 120 * (j), self.offset_y + 740 + rou * 20))
        for j,me in enumerate(self.ttrr.emo):
            #labels for the meta
            color = emocolors[self.ttrr.emo[1]]
            if not j==0:
                rou = 1
                labm = self.fonts[1].render("[{}]:{:0.3f}".format(self.meta_ch[j+3], float(me)), 1, color)
                self.GUI_SCREEN.blit(labm, (self.offset_x + 600 + 120 * (j), self.offset_y + 740 + rou * 20))
            else:
                rou = 2
                labm = self.fonts[1].render("[{}]:{}".format(self.meta_ch[j+3], me), 1, color)
                self.GUI_SCREEN.blit(labm, (self.offset_x + 600 + 120 * (j+1), self.offset_y + 740 + rou * 20))
        # buttons
        for bt in self.buttons:
            if self.loop:
                pygame.draw.rect(self.GUI_SCREEN, color_pix[0], pygame.Rect(bt), 4)
                lab_nq = self.fonts[2].render("[-- LOOP --]", 1, color_pix[0])
                self.GUI_SCREEN.blit(lab_nq, (bt[0]+40, bt[1]+40))
            else:
                pygame.draw.rect(self.GUI_SCREEN, color_pix[1], pygame.Rect(bt), 2)
                lab_nq = self.fonts[2].render("[SEQUENCE]", 1, color_pix[1])
                self.GUI_SCREEN.blit(lab_nq, (bt[0]+40, bt[1]+40))
        # the queue
        if (self.loop):
            for i,q in enumerate(self.queue):
                psx =self.offset_x + (q%self.nx) * self.sz_x 
                psy = self.offset_y + int(q/self.ny) * self.sz_y
                pygame.draw.rect(self.GUI_SCREEN, (255,255,255), pygame.Rect(psx, psy, self.sz_x, self.sz_y), 4)
                if (i>0):
                    apsx =self.offset_x + (self.queue[i-1]%self.nx) * self.sz_x 
                    apsy = self.offset_y + int(self.queue[i-1]/self.ny) * self.sz_y
                    pygame.draw.line(self.GUI_SCREEN, (255, 255,255), (apsx, apsy), (psx, psy), 3)

            if (len(self.queue)<7):
                str_q = "-".join(["[{}]".format(k) for k in self.queue])
                lab_q = self.fonts[1].render(str_q, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q, (self.offset_x + 1050, self.offset_y + 740))
            elif(len(self.queue)<13):
                str_q = "-".join(["[{}]".format(k) for k in self.queue[:6]])
                lab_q = self.fonts[1].render(str_q, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q, (self.offset_x + 1050, self.offset_y + 740))
                str_q2 = "-".join(["[{}]".format(k) for k in self.queue[6:]])
                lab_q2 = self.fonts[1].render(str_q2, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q2, (self.offset_x + 1050, self.offset_y + 760))
            elif(len(self.queue)<19):
                str_q = "-".join(["[{}]".format(k) for k in self.queue[:6]])
                lab_q = self.fonts[1].render(str_q, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q, (self.offset_x + 1050, self.offset_y + 740))
                str_q2 = "-".join(["[{}]".format(k) for k in self.queue[6:12]])
                lab_q2 = self.fonts[1].render(str_q2, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q2, (self.offset_x + 1050, self.offset_y + 760))
                str_q3 = "-".join(["[{}]".format(k) for k in self.queue[12:]])
                lab_q3 = self.fonts[1].render(str_q3, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q3, (self.offset_x + 1050, self.offset_y + 780))
            else:
                str_q = "-".join(["[{}]".format(k) for k in self.queue[:6]])
                lab_q = self.fonts[1].render(str_q, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q, (self.offset_x + 1050, self.offset_y + 740))
                str_q2 = "-".join(["[{}]".format(k) for k in self.queue[6:12]])
                lab_q2 = self.fonts[1].render(str_q2, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q2, (self.offset_x + 1050, self.offset_y + 760))
                str_q3 = "-".join(["[{}]".format(k) for k in self.queue[12:18]])
                lab_q3 = self.fonts[1].render(str_q3, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q3, (self.offset_x + 1050, self.offset_y + 780))
                str_q4 = "-".join(["[{}]".format(k) for k in self.queue[18:]])
                lab_q4 = self.fonts[1].render(str_q4, 1, (255, 255, 255))
                self.GUI_SCREEN.blit(lab_q4, (self.offset_x + 1050, self.offset_y + 800))          

        # rect for current minitrack
        ccc = emocolors[randint(0,9)]
        psx =self.offset_x + (self.a_track%self.nx) * self.sz_x 
        psy = self.offset_y + int(self.a_track/self.ny) * self.sz_y
        pygame.draw.rect(self.GUI_SCREEN, ccc, pygame.Rect(psx, psy, self.sz_x, self.sz_y), 4)
        pygame.draw.rect(self.GUI_SCREEN, ccc, pygame.Rect(psx-4, psy-4, self.sz_x+8, self.sz_y+8), 1)

        return



    def send_osc_track(self, _osc_client):
        for i,ch in enumerate(self.channels):
            ruta = "/ds/"+ch
            _osc_client.send_message(ruta.encode(), [self.ttrr.current_norm[i]])
    def send_osc_meta(self, _osc_client):
        meta = self.ttrr.vad + self.ttrr.emo
        for i,ch in enumerate(self.meta_ch):
            ruta = "/ds/"+ch
            if (i==3):
                _osc_client.send_message(ruta.encode(), [meta[i].encode()])
            else:
                _osc_client.send_message(ruta.encode(), [meta[i]])
        return

    def check_collisions(self, _pos, _mp):
        # for buttons
        #print (_pos[0], _pos[1])
        #print (_mp)
        for i,bt in enumerate(self.buttons):
            if (bt.collidepoint(_pos)):
                if i==0:
                    self.loop = not self.loop
                    if self.loop: self.queue = [self.a_track]
                    print('queue: {}'.format(self.queue))
                #if j==4:
                #    tr.state['on'] = not tr.state['on']
                print("[bt|{}] ".format(i))
        # for minitracks
        if self.loop:
            ik = -1
            for k in range(len(self.tracks)):
                _px = self.offset_x + (k%self.nx) * self.sz_x 
                _py = self.offset_y + int(k/self.ny) * self.sz_y
                if (_pos[0] > _px) and (_pos[0] < _px+64) and (_pos[1] > _py) and (_pos[1] < _py+32):
                    ik = k
                    break
            if not ik == -1:
                if _mp[0]:
                    self.queue.append(ik)
                    print("[Q]: {}".format(self.queue))
                elif _mp[2] and len(self.queue)>1:
                    self.queue.pop(0)
                    print("[Q]: {}".format(self.queue))
        return




# -utils----------------------- ----------------------- -----------------------
def parse_data_old(_fn = DATA_PATH):
    # get data and keys       
    raw_data = json.load(open(_fn, 'r'))
    keys = list(raw_data.keys())
    # then get the lists
    center_x = [c[0] for c in raw_data[keys[0]]]
    center_y = [c[1] for c in raw_data[keys[0]]]
    area_total =  raw_data[keys[1]]
    radius_max = raw_data[keys[2]]
    n_segments = raw_data[keys[4]]
    s0_cx = [c[0][0] if len(c)>0 else 0 for c in raw_data[keys[5]]]
    s0_cy = [c[0][1] if len(c)>0 else 0 for c in raw_data[keys[5]]]
    s0_area = [a[0] if len(a)>0 else 0 for a in raw_data[keys[6]]]
    # make the big list and return
    data = [center_x, center_y, area_total, radius_max, n_segments,s0_cx,s0_cy,s0_area]
    return data

def parse_data(_fn = DATA_PATH):
    return json.load(open(_fn, 'r'))
    

# ------ ----------------------- ----------------------- -----------------------
# -mapping function
def pmap(value, inMin, inMax, outMin, outMax, clamp=True):
    """ like processing's map """
    inSpan = inMax - inMin
    outSpan = outMax - outMin
    if (clamp):
        if (value<inMin): value = inMin
        if (value>inMax): value = inMax
    try:
        transVal = float(value - inMin) / float(inSpan)
        return outMin + (transVal * outSpan)
    except:
        return 0

# https://gist.github.com/laundmo/b224b1f4c8ef6ca5fe47e132c8deab56
def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b

def inv_lerp(a: float, b: float, v: float) -> float:
    """Inverse Linar Interpolation, get the fraction between a and b on which v resides.
    Examples
    --------
        0.5 == inv_lerp(0, 100, 50)
        0.8 == inv_lerp(1, 5, 4.2)
    """
    return (v - a) / (b - a)

def remap(i_min: float, i_max: float, o_min: float, o_max: float, v: float) -> float:
    """Remap values from one linear scale to another, a combination of lerp and inv_lerp.
    i_min and i_max are the scale on which the original value resides,
    o_min and o_max are the scale to which it should be mapped.
    Examples
    --------
        45 == remap(0, 100, 40, 50, 50)
        6.2 == remap(1, 5, 3, 7, 4.2)
    """
    return lerp(o_min, o_max, inv_lerp(i_min, i_max, v))





    
# ------ ----------------------- ----------------------- -----------------------
# START HERE

# -
TIC_TIMER = 60 # 12 fps
TIC_TIMER = 120

# -init
pygame.init()
FONT_PATH = "RevMiniPixel.ttf"

# -screen
WIDTH = 1480
HEIGHT = 880
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


#-useful colors
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (223, 223, 223)
BLACK = (0,0,0)
ORANGE = (232,111,97)
BACKGROUND_COLOR = '#02033e'


# main screen for drawing buttons

#- channels
canales = ['cx','cy', 'area', 'radius', 'nparts', 'ncentrds','c0x','c0y', 'a0', 'b0x', 'b0y']
n_ch = len(canales)

# timer events
TIC_EVENT = pygame.USEREVENT + 1

#states and counters
clock = pygame.time.Clock()

running = True
ii=0
iid = 0




# .tracker.init ---------------------------------------------------------------
#TR = Tracker(parse_data(), FONT_PATH)
TR = Tracktor(parse_data(), WIDTH, HEIGHT, FONT_PATH)


# ------ ----------------------- ----------------------- -----------------------


# tic for the timer
def tic():
    global ii, iid
    #update_data_send(ii)

    ii = ii+1
    TR.update()
    return

# handle keys pressed
def handle_keys(event):
	global running
	if (event.key == pygame.K_q):
		running = False

# handlear eventos con un diccionario
def handle_events():
	event_dict = {
		pygame.QUIT: exit,
		pygame.KEYDOWN: handle_keys,
		TIC_EVENT: tic,
        pygame.MOUSEBUTTONDOWN: handle_mouse_clicks
        #pygame.MOUSEBUTTONDOWN: handle_mouse_where
		}

	for event in pygame.event.get():
		if event.type in event_dict:
			if (event.type==pygame.KEYDOWN):
				event_dict[event.type](event)
			else:
				event_dict[event.type]()
	return

# handlear clicks del mouse
def handle_mouse_clicks():
    # check for mouse pos and click
    pos = pygame.mouse.get_pos()
    mp = pygame.mouse.get_pressed()
    # collitions in Trackxr
    TR.check_collisions(pos, mp)
    # other collitions
    check_other_collisions(pos, mp)
    return


# handlear clicks del mouse
def check_other_collisions(pos, mp):
    global sws_canales, contadoress
    # check for mouse pos and click
    pos = pygame.mouse.get_pos()
    mp = pygame.mouse.get_pressed()
    print (pos, mp)
    #TR.check_collisions(pos, mp)
    return



# the loop from outside
def game_loop():
    TR.draw()
    WINDOW.blit(TR.DRAW_SCREEN, (0, 0))
    #WINDOW.blit(TR.GUI_SCREEN, (0, 0))
    #TR.draw_labels(WINDOW)
    pygame.display.flip()
    while running:
        handle_events()
        TR.draw_mini()
        TR.draw_gui()
        WINDOW.blit(TR.DRAW_SCREEN, (0, 0))
        WINDOW.blit(TR.GUI_SCREEN, (0, 0))
        pygame.display.flip()
        #handle_mouse_clicks()
        # .drawing routine
        #DRAW_SCREEN.fill(BACKGROUND_COLOR)
        clock.tick(300)

# the main (init+loop)
def main():
    pygame.display.set_caption('[DEEPSELF :: emotionstream]')
    #init_osc()
    #load_data()
    pygame.time.set_timer(TIC_EVENT, TIC_TIMER)
    game_loop()
    print("---- [transmission's over]")


if __name__=="__main__":
    main()