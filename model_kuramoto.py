import pygame, math, random, pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
import time

class person:
    def __init__(self, name, freq, phase):
        self.name = name
        self.freq = freq
        self.phase = phase

class Settings:
    K=0.1 
    dt = 0.1
    focus=True
    istimed=False
    curr_time = time.time()
    timed="Не синхронизировалось"
    def __init__(self,target_freq,noob_freq,pro_freq,focus):

        self.target_freq=target_freq
        self.noob=noob_freq
        self.pro_freq=pro_freq
        self.focus=focus

#frequency to go around a circle in 8 seconds
target_freq = 1/(16*math.pi)

Conductor = person("Conductor", target_freq,random.random()* 2*math.pi)
Noob = person("Noob", target_freq*(1.1),random.random()* 2*math.pi)     
Pro = person("Pro", target_freq*(0.9),random.random()* 2*math.pi)


def update():
    K = Settings.K
    dt = Settings.dt
    
    dPhase_Pro = Pro.freq + K*math.sin((Conductor.phase-Pro.phase))/3

    if Settings.focus:
        dPhase_Noob = Noob.freq + K*math.sin((Conductor.phase-Noob.phase))/3
    else:
        dPhase_Noob = Noob.freq + K*math.sin((Pro.phase-Noob.phase))/9  + \
        K*math.sin((Conductor.phase-Noob.phase))/3

    Noob.phase = (Noob.phase + dPhase_Noob*dt)%(2*math.pi)
    Pro.phase = (Pro.phase + dPhase_Pro*dt)%(2*math.pi)
    Conductor.phase = (Conductor.phase + Conductor.freq*dt)%(2*math.pi)

def draw_circles():
    Noob_color = (213, 242, 46) # Yellow
    Pro_color = (56, 169, 255) #  Blue
    Conductor_color = (204, 0, 0) # Red
    screen.fill((200,200,200))

    pygame.draw.circle(screen, (0,0,0), (640,360), 250, width=5) #Draw a big circle
    
    pygame.draw.circle(screen, Noob_color, (-250*math.cos(Noob.phase)+640, 250*math.sin(Noob.phase)+360), 20) # Noob

    pygame.draw.circle(screen, Pro_color, (-250*math.cos(Pro.phase)+640, 250*math.sin(Pro.phase)+360), 20) # Pro

    pygame.draw.circle(screen, Conductor_color, (-250*math.cos(Conductor.phase)+640, 250*math.sin(Conductor.phase)+360), 20) # Conductor



    pygame.draw.circle(screen, Noob_color, (1100,200), 20) 

    label_noob = myfont.render((" - Новичок"), 1, (0,0,0))
    screen.blit(label_noob, (1130, 190))

    pygame.draw.circle(screen, Pro_color, (1100,300), 20) 
    label_pro = myfont.render((" - Опытный"), 1, (0,0,0))
    screen.blit(label_pro, (1130, 290))

    pygame.draw.circle(screen, Conductor_color, (1100,400), 20) 
    label_conductor = myfont.render((" - Дирижёр"), 1, (0,0,0))
    screen.blit(label_conductor, (1130, 390))

def change_noob_phase():
    Settings.curr_time = time.time()
    Noob.phase = random.random()*2*math.pi
    Settings.istimed=False


def change_pro_phase():
    Settings.curr_time = time.time()
    Pro.phase = random.random()*2*math.pi
    Settings.istimed=False


size = width, height = 1280, 720
pygame.init()

pygame.font.init()

screen = pygame.display.set_mode(size)  

pygame.display.set_caption('Kuramoto')

myfont = pygame.font.SysFont("monospace", 24)



k_slider = Slider(screen, 50, 50, 100, 20, min=0, max=0.2, step=0.005, initial=0.1,handleColour=(144, 127, 240), colour=(255,255,255))
dt_slider = Slider(screen, 1100, 50, 100, 20, min=0, max=2, step=0.1, initial=1, handleColour=(57, 227, 128), colour=(255,255,255))
toggle = Toggle(screen, 50, 360, 40, 20, startOn=False, offColour=(227, 73, 73), handleOffColour=(255,0,0))



button_random_noob = Button(screen,50,600,100,100,text='Random Noob',fontSize=20,margin=20,inactiveColour=(213, 242, 46),
hoverColour=(150, 150, 0),pressedColour=(0, 200, 20),radius=20, onClick=lambda: change_noob_phase())

button_random_pro = Button(screen,1130,600,100,100,text='Random Pro',fontSize=20,margin=20,inactiveColour=(56, 169, 255),
hoverColour=(0, 0, 150),pressedColour=(0, 200, 20),radius=20, onClick=lambda: change_pro_phase())



clock = pygame.time.Clock()
run=True



def sync_time(istimed):
    if (Pro.phase - Conductor.phase > -0.06) and \
    (Pro.phase - Conductor.phase < -0.059) and \
    (istimed==False):
        if Settings.focus==False:
            if (Noob.phase - Conductor.phase > 0.029) and \
               (Noob.phase - Conductor.phase < 0.03):
                Settings.istimed=True
                Settings.timed = str(round(time.time() - Settings.curr_time,3)*Settings.dt) + "с"
        else:
            if (Noob.phase - Conductor.phase > 0.059) and \
               (Noob.phase - Conductor.phase < 0.06):
                Settings.istimed=True
                Settings.timed = str(round(time.time() - Settings.curr_time,3)*Settings.dt) + "с"
        

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    update()
    draw_circles()
    sync_time(Settings.istimed)
    

    sync_label = myfont.render(("Время синхронизации = " + Settings.timed), 1, (0,0,0))
    screen.blit(sync_label, (360, 650))


    label_k = myfont.render(("K = " + str(round(k_slider.getValue(),3))), 1, (0,0,0))
    screen.blit(label_k, (60, 80))
    Settings.K=round(k_slider.getValue(),1)
    

    label_dt = myfont.render(("dt = " + str(round(dt_slider.getValue(),2))), 1, (0,0,0))
    screen.blit(label_dt, (1100, 80))
    Settings.dt=round(dt_slider.getValue(),1)

    label_tg = myfont.render(("focus=" + str(toggle.getValue())), 1, (0,0,0))
    screen.blit(label_tg, (30, 390))
    Settings.focus=toggle.getValue()

    pygame_widgets.update(pygame.event.get())
    
    pygame.display.flip()
pygame.display.quit() 

pygame.quit()
