import ode
import matplotlib.pyplot as plt

INSTANTES = 200
PASOS = 0.005

MASA = 0.05
L = 0.05
W = 0.05
H = W
ZINI = 0.2

POSICION_Z = H/2+ZINI

mundo = ode.World()
mundo.setGravity((0,0,-9.81))

caja = ode.Body(mundo)
caja.setPosition((0,0,POSICION_Z))

masa_caja = ode.Mass()
masa_caja.setBoxTotal(MASA, W, L, H)
caja.setMass(masa_caja)

pos_z = []
tiempo = []
for i in range(0,INSTANTES+1):
	mundo.step(PASOS)
	x,y,z = caja.getPosition()
	pos_z.append(z)
	tiempo.append(i)
	print("posición z: {:4.4f} tiempo: {:4.4f}".format(z,i))

position = caja.getPosition()

print(len(pos_z))
print(len(tiempo))

plt.style.use('dark_background')
plt.title('Caída libre Simple', color = '#17becf')
plt.xlabel('Tiempo [s]', color = '#ff7f0e')
plt.ylabel('Altura [m]', color = '#ff7f0e')

plt.axis([0,220,-5,1])
plt.plot(tiempo, pos_z, color='#17becf')
plt.show()



