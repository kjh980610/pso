import numpy as np
import math
import matplotlib.pyplot as plt
import random

init_th = np.pi*random.random()

def get_length(c, c1, c2) :
    len = math.sqrt((c[c1,0] - c[c2,0])**2 + (c[c1,1] - c[c2,1])**2)
    return len

def get_theta(l1, l2, l3) :
    if not _check_tri(l1,l2,l3):
        raise Exception('삼각형X')
    th = math.acos((l1**2 + l3**2 - l2**2)/(2*l1*l3))
    return th

def cal_end(l,theta) :
    c = np.zeros((9,2))
    c[1]= [-l[0],0]
    c[2] = [0,l[1]]
    c[3] = c[2] + [math.cos(theta)*l[2],math.sin(theta)*l[2]]

    l13 = get_length(c,1,3)
    l30 = get_length(c,3,0)

    th310 = get_theta(l13,l30,l[0])
    if c[3,1] < 0:
        th310 = -th310

    th413 = get_theta(l[4],l[3],l13)
    th410 = th413+th310
    c[4] = [c[1,0]+math.cos(th410)*l[4],math.sin(th410)*l[4]]

    th713 = get_theta(l[6],l[5],l13)
    th710 = th713 - th310
    c[7]= [c[1,0]+math.cos(th710)*l[6],-math.sin(th710)*l[6]]

    th514 = get_theta(l[8],l[7],l[4])
    th510 = th514 + th410
    c[5]= [c[1,0]+math.cos(th510)*l[8],math.sin(th510)*l[8]]

    l57 = get_length(c,5,7)
    th751=get_theta(l[8],l[6],l57)
    th756=get_theta(l[9],l[10],l57)
    th56=th751+th756 -(th510-np.pi)
    c[6]= [c[5,0]+math.cos(th56)*l[9],c[5,1]+math.sin(-th56)*l[9]]

    th567 = get_theta(l[9],l57,l[10])
    th768 = get_theta(l[11],l[12],l[10])
    th68 = th567 + th768 - (np.pi-th56)
    c[8]= [c[6,0]+math.cos(th68)*l[11],c[6,1]+math.sin(-th68)*l[11]]
    return c


def cal_yan(link) :
    l =np.array([38, 8, 15, 50, 41.5, 61.9, 39.3, 55.8, 40.1, 39.4, 36.7, 65.7, 49])
    l[3:] = link

    check_link(l)

    n=1000
    theta = np.linspace(init_th,np.pi*2+init_th,n+1)
    c = np.zeros((n,9,2))

    for i in range(n) :
        theta[i] = theta[i]%(np.pi*2)
        c[i] = cal_end(l,theta[i])
        check_c(l,c[i])

    ep = c[:,8,:]
    gac = 0
    gl = 0
    max_vel = 0
    min_vel = 100
    max_gl_y = -100
    for t in range(n):
        n_t = t+1
        if t == n-1 :
            n_t = 0

        dx = ep[n_t,0]-ep[t,0]
        dy = ep[n_t,1]-ep[t,1]

        ga=np.rad2deg(math.atan2(dy,dx))

        if abs(ga) <= 5 :
            # _check_und(t,n_t,ep)
            vel = math.sqrt(dx**2+dy**2)

            if vel > max_vel:
                max_vel = vel
            elif vel < min_vel:
                min_vel = vel
            if ep[t,1] > max_gl_y:
                max_gl_y = ep[t,1]
            gl=gl+vel
            gac=gac+1

    dev = max_vel - min_vel
    dev = dev ** 2
    y_dev = max_gl_y - min(ep[:,1])
    gac = gac/n
    ob = [gl, gac, dev, y_dev]

    return ob



def check_link(l):
    if not _check_tri(l[4],l[7],l[8]):
        raise Exception("not triangle1")
    
    if not _check_tri(l[10],l[11],l[12]):
        raise Exception("not triangle2")
    
    if not l[2] < l[3]:
        raise Exception("c2")
    
    if not l[2] < l[5]:
        raise Exception("c6")
    return True

def check_c(l,c):
    if not get_length(c,1,2) + l[2] < l[3] + l[4] :
        raise Exception("c3")
    
    if not get_length(c,1,2) + l[2] < l[5] + l[6]:
        raise Exception("c7")

    if not c[1,1] > (c[7,1]-c[5,1])/(c[7,0]-c[5,0]) * (c[1,0]-c[5,0]) + c[5,1] :
        raise Exception("c5")

    if not c[7,1] < (c[1,1]-c[3,1])/(c[1,0]-c[3,0]) * (c[7,0]-c[3,0]) + c[3,1] :
        raise Exception("c4")

def _check_tri(l1, l2, l3):
    l=[l1,l2,l3]
    if sum(l)-2*max(l) > 0 :
        return True
    else:
        return False


def _check_und(t,n_t,ep): #up&down
    upidx = np.where(ep[:,0]>ep[t,0])
    undidx = np.where(ep[upidx,0]<ep[n_t,0])[1]
    if (ep[undidx,1] < ep[t,1]).any():
        print('왜 꼬임')
        # raise Exception('꼬임')

def print_link(link):
    l =np.array([38, 8, 15, 50, 41.5, 61.9, 39.3, 55.8, 40.1, 39.4, 36.7, 65.7, 49])
    l[3:] = link

    check_link(l)

    n=1000
    theta = np.linspace(init_th,np.pi*2+init_th,n)
    c = np.zeros((n,9,2))

    for i in range(n) :
        theta[i] = theta[i]%(np.pi*2)
        c[i] = cal_end(l,theta[i])
        check_c(l,c[i])
        
    ep = c[:,8,:]
    plt.plot(ep[:,0],ep[:,1])
    for t in range(n):
        
        n_t = t+1
        if t == n-1 :
            n_t = 0
            
        dx = ep[n_t,0]-ep[t,0]
        dy = ep[n_t,1]-ep[t,1]

        ga=np.rad2deg(math.atan2(dy,dx))

        if abs(ga) <= 11.3 :
            plt.plot(ep[[t,n_t],0],ep[[t,n_t],1],'r')

    frame = c[0,:,:]
    plt.plot(frame[2:,0],frame[2:,1],'k')
    plt.plot(frame[[4,1,7,3],0],frame[[4,1,7,3],1],'k')
    plt.plot(frame[[1,5],0],frame[[1,5],1],'k')
    plt.plot(frame[[6,8],0],frame[[6,8],1],'k')
    plt.axis([-110, 50, -110, 50])
    


    plt.show()
