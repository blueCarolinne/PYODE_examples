import sys, os, random, time
from math import *
import ode
import matplotlib.pyplot as plt

TICKS = 200
MASA = 0.05
L = 0.05
W = 0.05
H = W
ZINI = 0.2

MU = 0.2
MU2 = MU

GRAVEDAD = -9.81

PASOS = 0.005
CFM = 1e-5
ERP = 0.2
MAX_CORRECTING_VEL = 0.1
CAPA_SUPERFICIAL = 0.0001
REBOTE = 0.3
REBOTE_VEL = 0.1
SOFT_CFM = 0.01
MAX_CONTACTOS = 4



def nuevo_objeto (mundo, espacio, densidad, lx, ly, lz):
    cubo = ode.Body(mundo)
    cubo.setPosition((0.0, 0, H/2+ZINI))
    masa_cubo= ode.Mass()
    masa_cubo.setBoxTotal(densidad,lx,ly,lz)
    cubo.setMass(masa_cubo)

    cubo.sizebox = (lx,ly,lz)

    geometria = ode.GeomBox(espacio, lengths=cubo.sizebox)
    geometria.setBody(cubo)

    return cubo, geometria

def near_callback(args, geometria1,geometria2):
    contacto = ode.collide(geometria1,geometria2)

    mundo, grupo_contacto = args

    for c in contacto:
        c.setBounce(REBOTE)
        c.setMu(MU)
        c.setMu2(MU2)
        c.setBounceVel(REBOTE_VEL)
        c.setSoftCFM(SOFT_CFM)

        j = ode.ContactJoint(mundo,grupo_contacto,c)
        j.attach(geometria1.getBody(), geometria2.getBody())

#Simulacion

mundo = ode.World()
mundo.setGravity((0,0,GRAVEDAD))
mundo.setERP(ERP)
mundo.setCFM(CFM)
mundo.setContactMaxCorrectingVel(MAX_CORRECTING_VEL)
mundo.setContactSurfaceLayer(CAPA_SUPERFICIAL)
espacio = ode.Space()

suelo = ode.GeomPlane(espacio,(0,0,1),0)
grupo_contacto = ode.JointGroup()

cubo, geometria = nuevo_objeto(mundo,espacio,MASA,W,L,H)

pos_z = []
tiempo = []


for i in range(TICKS):

        espacio.collide((mundo,grupo_contacto), near_callback)

        mundo.step(PASOS)
        x,y,z = cubo.getPosition()
        pos_z.append(z)
        tiempo.append(i)
        print("altura: {:4.4f} tiempo:  {:4.2f}".format(z,i))
        
        

        grupo_contacto.empty()
position = cubo.getPosition()

print(len(pos_z)) 
print(len(tiempo))

plt.style.use('dark_background')
plt.title('Caída libre con rebote', color = '#17becf')
plt.xlabel('Tiempo [s]', color = '#ff7f0e')
plt.ylabel('Altura [m]', color = '#ff7f0e')

plt.axis([0,220,0,H/2+ZINI+0.05])
plt.plot(tiempo, pos_z, color='#17becf')
plt.show()

