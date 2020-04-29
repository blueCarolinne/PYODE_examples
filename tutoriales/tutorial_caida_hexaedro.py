import sys, os, random, time
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import ode

def escalap(vec, scal):
    vec[0] *= scal
    vec[1] *= scal
    vec[2] *= scal

def longitud (vec):
    return sqrt (vec[0]**2 + vec[1]**2 + vec[2]**2)

def preparacion_GL():
    # Viewport
    glViewport(0,0,640,480)

    # Initialize
    glClearColor(0.5,0.7,0.7,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_FLAT)

    # Projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective (45,1.3333,0.2,20)

    # Initialize ModelView matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Light source
    glLightfv(GL_LIGHT0,GL_POSITION,[0,0,1,0])
    glLightfv(GL_LIGHT0,GL_DIFFUSE,[1,1,1,1])
    glLightfv(GL_LIGHT0,GL_SPECULAR,[1,1,1,1])
    glEnable(GL_LIGHT0)

    # View transformation
    gluLookAt (2.4, 3.6, 4.8, 0.5, 0.5, 0, 0, 1, 0)

def dibujando_cuerpo(cuerpo):

    x,y,z = cuerpo.getPosition()
    R = cuerpo.getRotation()
    rot = [R[0], R[3], R[6], 0.,
           R[1], R[4], R[7], 0.,
           R[2], R[5], R[8], 0.,
           x, y, z, 1.0]
    glPushMatrix()
    glMultMatrixd(rot)
    if cuerpo.shape=="hexaedro":
        sx,sy,sz = cuerpo.sizebox
        glScalef(sx, sy, sz)
        glutSolidCube(1)
    glPopMatrix()


def creando_cuerpo(mundo, espacio, densidad, lx, ly, lz):

    cuerpo = ode.Body(mundo)
    M = ode.Mass()
    M.setBox(densidad,lx,ly,lz)
    cuerpo.setMass(M)

    cuerpo.shape = "hexaedro"
    cuerpo.sizebox = (lx,ly,lz)

    geometria = ode.GeomBox(espacio, lengths=cuerpo.sizebox)
    geometria.setBody(cuerpo)

    return cuerpo, geometria

def lanzando_objetos():
    global todos_cuerpos, geometria, contador, contador_objetos

    cuerpo, geometria = creando_cuerpo(mundo,espacio,2000,1.0,0.2,0.2)
    cuerpo.setPosition((random.gauss(0,0.1),5.0,random.gauss(0,0.1)))

    theta = random.uniform(0,2*pi)
    coseno = cos (theta)
    seno = sin (theta)
    cuerpo.setRotation([coseno, 0., -seno, 0., 1., 0., seno, 0., coseno])
    todos_cuerpos.append(cuerpo)
    todas_geometrias.append(geometria)
    contador = 0
    contador_objetos += 1


#reconociendo contactos y articulaciones entre dos cuerpos
def near_callback(args, geometria1,geometria2):
    contacto = ode.collide(geometria1,geometria2)

    mundo, grupo_contacto = args

    for c in contacto:
        c.setBounce(0.2)
        c.setMu(5000)
        j = ode.ContactJoint(mundo,grupo_contacto,c)
        j.attach(geometria1.getBody(), geometria2.getBody())


###########################################################

glutInit([])

#ventana
glutInitDisplayMode (GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)

x = 0
y = 0
width = 640
height = 480
glutInitWindowPosition (x, y);
glutInitWindowSize (width, height);
glutCreateWindow ("testode")

mundo = ode.World()
mundo.setGravity((0,-9.81,0))
mundo.setERP(0.8)
mundo.setCFM(1E-5)

espacio = ode.Space()

suelo = ode.GeomPlane(espacio,(0,1,0),0)

todos_cuerpos = []

todas_geometrias = []

grupo_contacto = ode.JointGroup()

fps = 60
dt = 1.0/fps
running = True
estado = 0
contador = 0
contador_objetos = 0
ultimo_momento = time.time()

def _keyfunc (c,x,y):
    sys.exit(0)

glutKeyboardFunc (_keyfunc)

def _drawfunc ():
    preparacion_GL()
    for b in todos_cuerpos:
        dibujando_cuerpo(b)
    
    glutSwapBuffers ()

glutDisplayFunc(_drawfunc)

def _idlefunc():
    global contador, estado, ultimo_momento

    t = dt - (time.time() - ultimo_momento)
    if (t > 0):
        time.sleep(t)

    contador += 1

    if estado==0:
        if contador == 30:
            lanzando_objetos()
        if contador_objetos == 1:
            estado = 1
            contador = 0

    glutPostRedisplay ()

    # Simulacion
    n = 4

    for i in range(n):
        # Detect collisions and create contact joints
        espacio.collide((mundo,grupo_contacto), near_callback)

        # Simulation step
        mundo.step(dt/n)

        # Remove all contact joints
        grupo_contacto.empty()

    ultimo_momento = time.time()

glutIdleFunc (_idlefunc)

glutMainLoop ()


