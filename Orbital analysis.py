'''                                                         
                                                                     
 ██████╗ ██████╗ ██████╗ ██╗████████╗ █████╗ ██╗          █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗██╗███████╗
██╔═══██╗██╔══██╗██╔══██╗██║╚══██╔══╝██╔══██╗██║         ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝██╔════╝██║██╔════╝
██║   ██║██████╔╝██████╔╝██║   ██║   ███████║██║         ███████║██╔██╗ ██║███████║██║   ╚████╔╝ ███████╗██║███████╗
██║   ██║██╔══██╗██╔══██╗██║   ██║   ██╔══██║██║         ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝  ╚════██║██║╚════██║
╚██████╔╝██║  ██║██████╔╝██║   ██║   ██║  ██║███████╗    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████║██║███████║
 ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝╚══════╝

'''

import numpy as np
import numpy.linalg as alg


#       ___  _  _ _   _ ____ _ ____ ____ _       ____ ___  ___  ____ ____ ____ ____ _  _ 
#       |__] |__|  \_/  [__  | |    |__| |       |__| |__] |__] |__/ |  | |__| |    |__| 
#       |    |  |   |   ___] | |___ |  | |___    |  | |    |    |  \ |__| |  | |___ |  | 
                                                                                 


''' What's an orbit ? 
It's the gravitationally curved trajectory of an object 
The major part of orbits are supposed circulars, but to fit with reality let's consider them elliptics. (After we will add functions to make them 
parabolic or hyperbolic).
We take the ecuador of the created object as the plane reference.
There are several types of orbits : Suborbitals trajectories and Escape trajectories.
To define our orbits we will need some parameters as : Eccentricity, Half-major axis, tilt, longitude of the ascending node, perry argument, 
periapsis and the position.'''

#    About the position : 

''' Let's consider the mean anomaly, which allows us to know the fraction of the orbital period that has elapsed since the last pass to the periapsis, 
expressed as an angle.
We note the mean anomaly 'M', we have : 'G' the gravitationnal constant, 'a' the half major axis, 'Ms' the mass of the planet, 'm' the mass of the 
studied object.
M = sqrt(G(Ms+m)/a³)*t'''

def mean_anomaly(Ms,m,t,a):
    M=np.sqrt(6.67408*10**-11*(Ms+m)/a**3)*t
    return M


''' The eccentric anomaly is the angle between the periapsis and the actual position projected in the cercle excircled perpendicularly to the half 
major axis. 
Let's note the eccentric anomaly 'E'. Then with 'e' the eccentricity , we have :
The iteration : E[i+1]=(M-e*(E[i]cos(E[i]-sin(E[i]))/1-e*cos(E[i])) , by doing 4 iterations, we can obtain a precise value of E for a t time.'''

def eccentric_anomaly(M,e):
    E=np.pi
    for i in range(1,5):
        E=(M-e*(E*np.cos(E)-np.sin(E)))/1-e*np.cos(E)
    return E


''' Finally the true anomaly is the angle between the periapsis and the actual position of the studied object (that's what we want). We name the real 
anomaly 'v', then : tan(v/2) : sqrt(1+e/1-e)*tan(E/2)'''

def true_anomaly(E,e):   # E = eccentric anomaly, e = eccentricity
    v=2*np.arctan(np.sqrt(1+e/1-e))*np.tan(E/2)
    return v


''' If we want to know what is the eccentricity of an orbit, thanks to apoapsis radius(Ra) and periapsis radius(Rp), with :
e = (Ra-Rp)/(Ra+Rp)
or 
e = sqrt(1-(b²/a²))   with b the half minor axis and a the half major axis.'''

def e(Ra,Rp):
    e = (Ra-Rp)/(Ra+Rp)
    return e


def e_V2(a,b):
    e=np.sqrt(1-(b**2/a**2))
    return e


''' Thanks all others functions we can determine for a 't' time, the value or the distance between the object and its center. :
We have a r(E) relation, but also a E(t) relation so a r(E(t)) relation , a is the half major axis again'''

def r(E,a,e):
    r=a*(1-e*np.cos(E))
    return r


''' We can now know what will be the orbital period and finally know what will be the 't' time where the studied object is at the periapsis : 
by calculating the mean angular motion , named n'''

def n(M,m,a):
    n=np.sqrt(6.67408*10**-11*(m+M)/a**3)
    return n


def T(n):
    T=2*np.pi/n
    return T     # Orbital period


def t_periapsis(M,n,t):
    tperi=(M/n)-t
    return tperi   # Time t0 where the object is at the periapsis


## What parameters will the user enter ?

''' We absolutly need some parameters : 
- The eccentricity
- The masses
- The Half major axis

As the eccentricity can be found with Ra and Rp we can just ask these values, that can be easily understood.
Al least we must ask the value of masses.

So what the user will enter ? 
- 'a' The half major axis       (not mandatory)
- 'b' The half minor axis       (same)
- 'm' Mass of the studied object (or add it when he want to study an object)
- 'M' Mass of the massive object
- 'v0' The inital speed
- The initial position by a click in the graphic structure

With theses value we can now know we will be the studied object in the orbit.

Let's define now how to define this orbit with theses parameters'''

##        __
##       /  \  _ |_  . |_ 
##       \__/ |  |_) | |_ 
                  

''' To locate a position in 3D, especially a orbit, we will need two parameters : the tilt and the argument of the periapsis.
Each can be found with user's entries.

Let's consider the cylindrical coordinates :
        ->     ->                                                                              ->
We call er and eθ respectively the elementary radial vector and the elementary tangent vector. ez is the elementary vector for height.
For any M point we have in the ellipse :
θ is the angle formed between the periapsis and the object.

->     ->     ->
OM = r*er + z*ez

->          ->             ->           ->
v = (dr/dt)*er + r*(dθ/dt)*eθ + (dz/dt)*ez

->            ->                     ->                ->             ->
a = (d²r/dt²)*er + 2*(dr/dt)*(dθ/dt)*eθ + r*(dθ/dt)**2*er + (d²z/dt²)*ez '''

## Tilt :

''' To calculate the tilt, we need to find first the orbital kinetic torque. And to find this last, we need the force exerciced on the studied object.'''

def F(M,m,v):  # Will be oriented in the contrary sens of the radial vector. So there is only a radial component, v is real anomaly and V is speed.
    F=6.67408*10**-11*((m*M)/r**2)
    Fx=F*np.cos(v)
    Fy=F*np.sin(v)
    R=np.array([Fx,Fy,0])
    return R


''' The orbital kinetic torque in a O point is :1
    -------->   ->  ->        ->            ->             ->           ->                      ->                ->
    L[orbital]= OM ^ mv  = OM*er m*((dr/dt)*er + r*(dθ/dt)*eθ + (dz/dt)*ez) ^  = OM*m*r*(dθ/dt)*ez - OM*m*(dz/dt)*eθ

      ->             
So on ez : L[orbital-z] = OM*m*r*(dθ/dt)
      -> 
   on eθ : L[orbital-θ] = -OM*m*(dz/dt)

Finding the initial orbital kentic torque is unique, it won't change, find the tilt by calculating the angle between the initial orbital kinetic 
torque and the ecuador plan. To find cos(angle) this we will divide the e-component of the kinetic torque by the norm of this last, and then use arccos.'''

# We will search the z-component of Lo(M) which is the orbital kinetic torque at a M point.   

def initial_orbital_kineic_torque(OM,m,v):  # OM is an array (so the vector) v is the vector with x,y,z components
    r=m*v
    L=np.dot(OM, r)
    return L


# Tilt : 

'''Let's search the angle between the initial orbital torque and the ecuador plan (supposed to be the horizontally)'''

def tilt(L):  # L is an array
    Lz=L[2]     # The z component
    e=Lz/L[0]+L[1]+L[2]
    e=np.arccos(e)
    return e


''' A little suumary of all the functions we have created:

- mean anomaly
- eccentric anomaly
- true anomaly
- eccentricity
- radius
- mean angular motion
- period
- periapsis time
- F
- initial orbital kinetic torque
- tilt'''


#Here's the function that calculates the resulting speed of a planet born from a collision between two others,
#This apply when the two colliding planets merge into a single one

def choc(A,B):
    m=A[0]+B[0]
    px=A[0]*A[3]+B[0]*B[3]
    py=A[0]*A[4]+B[0]*B[4]
    pz=A[0]*A[5]+B[0]*B[5]
    return px/m and py/m and pz/m
    

