from random import randint

import numpy as np 
import pygame

from datetime import date
from datetime import datetime
import time

pygame.init()

#pygame.mouse.set_visible(False)

ancho = 1200
alto = 600
size=(ancho,alto)

centro = (ancho/2, alto/2)

screen = pygame.display.set_mode(size)


pygame.display.set_caption("SENSOR VS TIEMPO")
#icon = pygame.image.load("osciloscopio.png")
#pygame.display.set_icon(icon) 
 
# 
clock = pygame.time.Clock()


# COLORES 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY=(128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE =  (0, 0, 255)




class PUNTO:
	
	def __init__(self, y):
			
		self.x = ancho/2
		self.y = y
		self.tamano = 10
	


def CARTEL(texto, posicion, tamano, color):
	fuente = pygame.font.Font(None, tamano)
	fuente2 = pygame.font.Font(None, tamano)
	
	mensaje = fuente2.render(str(texto), tamano, color)
	screen.blit(mensaje, posicion)



def PAUSA():
	
	pygame.mixer.pause()
	global TEXTOCARTEL
	#TEXTOCARTEL='PAUSADO'
	Done=False
	while not Done:
		Mouse= [Mx,My] =[pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
		
		CARTEL('PAUSADO', (850,50), 30, RED)
		#TEXTOCARTEL='PAUSADO'
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				time.sleep(0.2)
				Done=True
				
			
			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
					time.sleep(0.1)
					Done=True
		

def DIBUJOGRILLA():
	global T
	BORDE=pygame.draw.rect (screen, WHITE,[0, 0, ancho, alto],2)
	
	#pygame.draw.line(surface, color, start_pos, end_pos, width)
	pygame.draw.line(screen, GRAY, (ancho*8/10,0),(ancho*8/10,alto), 1)
	pygame.draw.line(screen, GRAY, (0, alto/2),(ancho,alto/2), 1)
	

	for i in range(50):
		pygame.draw.line(screen, GRAY, (ancho*8/10-10, alto/20*i),(ancho*8/10+10, alto/20*i), 1)
		if ancho/20*i-T%ancho<ancho*8/10:
			pygame.draw.line(screen, GRAY, (ancho/20*i-T%ancho, alto/2-10),(ancho/20*i-T%ancho, alto/2+10), 1)

	for i in range(50):
		pygame.draw.line(screen, GRAY, (0, alto/10*i),(ancho*8/10, alto/10*i), 1)
		if ancho/10*i<ancho*8/10:
			pygame.draw.line(screen, GRAY, (ancho/10*i, 0),(ancho/10*i, alto), 1)



class BOTON:

	def __init__(self, texto, color, posicion): 
			
		self.x = posicion[0]
		self.y = posicion[1]
		self.color=color
		self.texto=texto
		self.ancho=90
		self.alto=50
		pygame.draw.rect(screen, GRAY, (self.x,self.y,self.ancho,self.alto), 0)
		pygame.draw.rect(screen, WHITE, (self.x,self.y,self.ancho,self.alto), 1)
		
		CARTEL(self.texto, (self.x+15,self.y+20), 20, self.color)
		
		
	
	def estado(self):
		if (self.x < Mx < self.x + self.ancho) and  (self.y< My< self.y +self.alto) and (Mpress[0]==True):
			pygame.draw.rect(screen, RED, (self.x,self.y,self.ancho,self.alto), 0)
			return True
		else:
			return False
		
			


def GRABANDO():
	f.write(f'\n {centro[1]-SENSOR}')
	
	
	
def GRABARCONDICION():
	time.sleep(0.2)
	global record 
	global f
	if record ==True:
		time.sleep(0.2)
		f.close()
		TEXTOCARTEL=''
		record=False
	else:
		now = datetime.now()
		current_time = now.strftime('%H:%M:%S')
		f=open(f'RECORD-{current_time}.txt','a')
		record=True


def main():
	
	global Mx
	global My
	global Mpress
	global f
	global SENSOR
	global record
	record=False
	
# ---------- LOOP PRINCIPAL  -----------

	H=[1]
	
	global T
	T=0
	
	
	
	global pausaestado
	pausaestado=False
	
	global TEXTOCARTEL
	TEXTOCARTEL=''
	
		
	List=[]	
	tick=50
	while True:
		T+=1
		
		screen.fill(BLACK)
		#screen.blit(imagenfondo, (-160,0))
		
		keys = pygame.key.get_pressed()
		Mouse= [Mx,My] =[pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
		Mpress=pygame.mouse.get_pressed()
	
		
		
	# --- Drawing
		DIBUJOGRILLA()
				
		
	# ---- CARTELES 
		CARTEL(TEXTOCARTEL, (850,50), 30, RED)
		CARTEL(f' = {centro[1]-My}', (ancho*9/10,30), 30, YELLOW)
		
		
		
		if Mx<int(ancho*8/10):
			SENSOR = My       # toma entrada desde posicion Y del mouse
		pelotitablanca= pygame.draw.circle(screen, WHITE, [int(ancho*8/10), SENSOR], 3, 0)
	
# :::::::::::BOTONES::::::::::
	
	#BOTON EXIT 
		BOTONexit=BOTON('EXIT', WHITE, (ancho*9/10,alto*2/10))
		if BOTONexit.estado():
			exit()
		
	#BOTON RECORD 
		BOTONrecord=BOTON('RECORD', WHITE, (ancho*9/10,alto*3/10))
		if BOTONrecord.estado():
			GRABARCONDICION()
					
		
		if record == True:
			TEXTOCARTEL='GRABANDO'
			GRABANDO()
			
		
	#BOTONES VELOCIDAD MEDIDA
		BOTONtickmas=BOTON('+ RAPIDO', WHITE, (ancho*9/10,alto*6/10))
		if BOTONtickmas.estado():
			if tick<200:
				tick+=5
			
		BOTONtickmenos=BOTON('- RAPIDO', WHITE, (ancho*9/10,alto*7/10))
		if BOTONtickmenos.estado():
			if tick>10:
				tick+=-5
		
	#BOTON PAUSA
		BOTONpausa=BOTON('PAUSA', WHITE, (ancho*9/10,alto*8/10))
		if BOTONpausa.estado():
			PAUSA()
			
			
		
	#  AQUI TOMAR DATO DESDE SENSOR, Y AGREGARLO COMO DATO ENTRADA en reemplazo del My.
		H.append(SENSOR)         # AQUI INGRESA DATO DE SENSOR EN EL TIEMPO
		
	# QUITA DATO INICIO DE LISTA (FIFO)
		num=len(H)
		if len(H)>ancho*8/10:
			H.pop(0)
			
		
	# DIBUJA LINEA MEDIDA DEL SENSOR
		num=len(H)
		for i in range(num):
			pygame.draw.line(screen, WHITE, (ancho*8/10-i, H[num-1-i]), (ancho*8/10-i-1, H[num-1-i-1]), 1)
			
		
						   
		# --- EVENTOS 
				
		if keys[pygame.K_UP]:pass
		if keys[pygame.K_DOWN]:pass
		if keys[pygame.K_LEFT]:pass
		if keys[pygame.K_RIGHT]:pass
			
	
		
		
# _______________________________     
				
		for event in pygame.event.get():
			#print (event)
			if event.type == pygame.QUIT:exit()
									
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					PAUSA()
			
				if event.key == pygame.K_q:exit()	
		#if keys[pygame.K_q]:exit()         
				
		
		clock.tick(tick)  
		pygame.display.flip()      
		
		
	
	pygame.quit()  


if __name__ == '__main__':
    main()


