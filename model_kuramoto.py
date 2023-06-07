import pygame, math, random, time, pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle

class person:
    def __init__(self, name, freq, phase):
        self.name = name
        self.freq = freq
        self.phase = phase

class Settings:
    K=0.25 
    dt = 1 
    focus=True
    def __init__(self,target_freq,noob_freq,pro_freq,focus):

        self.target_freq=target_freq
        self.noob=noob_freq
        self.pro_freq=pro_freq
        self.focus=focus

target_freq = 1/(4*math.pi)
Conductor = person("Conductor", target_freq,random.random()* 2*math.pi)
Noob = person("Noob", target_freq*(1.+0.1),random.random()* 2*math.pi) 
Pro = person("Pro", target_freq*(1.-0.1),random.random()* 2*math.pi)


def update():
    K = Settings.K
    dt = Settings.dt
    dPhase_Pro = Pro.freq + K*math.sin((Conductor.phase-Pro.phase))/3

    if Settings.focus:
        dPhase_Noob = Noob.freq + K*math.sin((Conductor.phase-Noob.phase))/3
    else:
        dPhase_Noob = Noob.freq + 0.33*K*math.sin((Pro.phase-Noob.phase))/3 + \
        K*math.sin((Conductor.phase-Noob.phase))/3

    Noob.phase = (Noob.phase + dPhase_Noob*dt)%(2*math.pi)
    Pro.phase = (Pro.phase + dPhase_Pro*dt)%(2*math.pi)
    Conductor.phase = (Conductor.phase + Conductor.freq*dt)%(2*math.pi)

def draw_circles():
    Noob_color = (255,255,0) # Yellow
    Pro_color = (0,0,255) #  Blue
    Conductor_color = (255,0,0) # Red
    screen.fill((255,255,255))

    
    

    pygame.draw.circle(screen, (0,0,0), (640,360), 200, width=5) #Draw a big circle
    
    pygame.draw.circle(screen, Noob_color, (-200*math.cos(Noob.phase)+640, 200*math.sin(Noob.phase)+360), 10) # Noob

    pygame.draw.circle(screen, Pro_color, (-200*math.cos(Pro.phase)+640, 200*math.sin(Pro.phase)+360), 10) # Pro

    pygame.draw.circle(screen, Conductor_color, (-200*math.cos(Conductor.phase)+640, 200*math.sin(Conductor.phase)+360), 10) # Conductor
    #time.sleep(0.05)

def change_noob_phase():
    Noob.phase = random.random()*2*math.pi

def change_pro_phase():
    Pro.phase = random.random()*2*math.pi


size = width, height = 1280, 720
pygame.init()
screen = pygame.display.set_mode(size)  

pygame.display.set_caption('Kuramoto')
Icon = pygame.image.load('giga.png')
pygame.display.set_icon(Icon)


k_slider = Slider(screen, 50, 50, 100, 20, min=0, max=1, step=0.1, initial=0.3,handleColour=(255,0,0))

K_output = TextBox(screen, 70, 80, 60, 30, fontSize=20)
K_output.disable()

dt_slider = Slider(screen, 1100, 50, 100, 20, min=0, max=1, step=0.1, initial=0.2, handleColour=(0,255,0))

dt_output = TextBox(screen, 1100, 80, 60, 30, fontSize=20)
dt_output.disable()

button_random_noob = Button(screen,50,600,100,100,text='Random Noob',fontSize=20,margin=20,inactiveColour=(255, 255, 0),
hoverColour=(150, 150, 0),pressedColour=(0, 200, 20),radius=20, onClick=lambda: change_noob_phase())

button_random_pro = Button(screen,1100,600,100,100,text='Random Pro',fontSize=20,margin=20,inactiveColour=(0, 0, 255),
hoverColour=(0, 0, 150),pressedColour=(0, 200, 20),radius=20, onClick=lambda: change_pro_phase())

toggle = Toggle(screen, 50, 360, 40, 20, startOn=False)
tg_output = TextBox(screen, 30, 390, 100, 30, fontSize=20)
tg_output.disable()

clock = pygame.time.Clock()
run=True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    update()
    draw_circles()

    K_output.setText("K = " + str(round(k_slider.getValue(),1)))
    Settings.K=round(k_slider.getValue(),1)

    dt_output.setText("dt = " + str(round(dt_slider.getValue(),1)))
    Settings.dt=round(dt_slider.getValue(),1)

    tg_output.setText("focus = " + str(toggle.getValue()))
    Settings.focus=toggle.getValue()

    pygame_widgets.update(pygame.event.get())
    
    pygame.display.flip()
pygame.display.quit() 

pygame.quit()
