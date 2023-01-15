from tkinter import *
from tkinter import filedialog
import os


root = Tk()
root.geometry('500x600')
root.title("Application")
root.configure(bg='#0a5688')


global x
global y
global z


offset = 0
dim = 1

ans = 0

global fileName
    

def clicked():
    fileName = root.filename = filedialog.askopenfilename(initialdir="/Project/StepFiles", title="select a file")
    x=int(xInput.get())
    y=int(yInput.get())
    z=int(zInput.get())
    print("x: ", x)
    print("y: ", y)
    print("z: ", z)

    answer = int(mainlogic(x,y,z,fileName))
    
    ansLabel =Label(root, text="Number of components : "+str(answer), bg='#9ae8e1', fg='#111457',  font=('Tahoma', 16,'bold'))
    ansLabel.place(x=90, y=410)
    
    
    
def mainlogic(boxx, boxy, boxz, filename):
     #converter modules
    import trimesh
    import gmsh

    #dimension modules
    import numpy as np
    import stl
    from stl import mesh
    import math


    #converter Code

    #if ((filename[-3:]).lower()=='.stp' or (filename[-4:]).lower()=='.step')

    mesh1 = trimesh.Trimesh(**trimesh.interfaces.gmsh.load_gmsh(file_name = filename, gmsh_args = [
                ("Mesh.Algorithm", 1), #Different algorithm types, check them out
                ("Mesh.CharacteristicLengthFromCurvature", 10), #Tuning the smoothness, + smothness = + time
                ("General.NumThreads", 2), #Multithreading capability
                ("Mesh.MinimumCirclePoints", 16)])) 
    mesh1.export('converted.STL')
    print("file converted!")


    #dimensions Code
    your_mesh = mesh.Mesh.from_file('converted.stl')

    #volume, cog, inertia = your_mesh.get_mass_properties()
    #print("Volume= {0}".format(volume))

    def find_mins_maxs(obj):
        minx = obj.x.min()
        maxx = obj.x.max()
        miny = obj.y.min()
        maxy = obj.y.max()
        minz = obj.z.min()
        maxz = obj.z.max()
        return minx, maxx, miny, maxy, minz, maxz
      
    minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(your_mesh)

    x=maxx - minx
    y=maxy - miny
    z=maxz - minz

    os.remove("converted.STL")
    boxes(boxx,boxy, boxz,x,y,z)

    #componentDimensions
    compDim= Label(root, text="Component Dimensions:", bg='#0a5688', fg='#ffffff', font= ('Sans 14 bold'))
    compDim.place(x=125, y=340)

    #x
    xComp= Label(root, text="X:", bg='#0a5688', fg='#ffffff', font= ('Sans 12 bold'))
    xComp.place(x=95, y=370)

    xL= Label(root, text=str(round(x, 2))+' mm', bg='#0a5688', fg='#ffffff', font= ('Sans 12 bold'))
    xL.place(x=115, y=370)

    #y
    yComp= Label(root, text="Y:", bg='#0a5688', fg='#ffffff', font= ('Sans 12 bold'))
    yComp.place(x=215, y=370)

    yL= Label(root, text=str(round(y, 2))+' mm', bg='#0a5688', fg='#ffffff', font= ('Sans 12 bold'))
    yL.place(x=235, y=370)

    #z
    zComp= Label(root, text="Z:", bg='#0a5688', fg='#ffffff', font= ('Sans 12 bold'))
    zComp.place(x=320, y=370)

    zL= Label(root, text=str(round(z, 2))+' mm', bg='#0a5688', fg='#ffffff', font= ('Sans 12 bold'))
    zL.place(x=340, y=370)
    
    return ans

def boxes (l,m,n,a,b,c):

    arr = [0,0,0,0,0,0]
    maxii = [0,0,0]
    prevmaxii = 0
    arr[0] = int(l/a) * int(m/b) * int(n/c)
    if(prevmaxii < arr[0]):
        maxii[0] = a
        maxii[1] = b
        maxii[2] = c
        prevmaxii = arr[0]
    
    arr[1] = int(l/a) * int(m/c) * int(n/b)
    if(prevmaxii < arr[1]):
        maxii[0] = a
        maxii[1] = c
        maxii[2] = b
        prevmaxii = arr[1]
    
    arr[2] = int(l/b) * int(m/a) * int(n/c)
    if(prevmaxii < arr[2]):
        maxii[0] = b
        maxii[1] = a
        maxii[2] = c
        prevmaxii = arr[2]
    
    arr[3] = int(l/b) * int(m/c) * int(n/a)
    if(prevmaxii < arr[3]):
        maxii[0] = b
        maxii[1] = c
        maxii[2] = a
        prevmaxii = arr[3]
    
    arr[4] = int(l/c) * int(m/b) * int(n/a)
    if(prevmaxii < arr[4]):
        maxii[0] = c
        maxii[1] = b
        maxii[2] = a
        prevmaxii = arr[4]
    
    arr[5] = int(l/c) * int(m/a) * int(n/b)
    if(prevmaxii < arr[5]):
        maxii[0] = c
        maxii[1] = a
        maxii[2] = b
        prevmaxii = arr[5]
    
    
    global ans
    global offset
    global dim
    
    print(max(arr))

    if max(arr)!=0:
        templabel =Label(root, text="Dimension " + str(dim) + " : " +str(max(arr)), bg='#0a5688', fg='#ffffff',  font=('Tahoma', 11,'bold'))
        templabel.place(x=160, y=(450+offset))
        offset+=25
        dim+=1
        
    
    ans += max(arr)

    if(max(arr) == 0):
        return
    
    if(l%maxii[0] >= m%maxii[1] and l%maxii[0] >= n%maxii[2]):
        boxes(l%maxii[0],m,n,a,b,c)
        
    elif(m%maxii[1] >= l%maxii[0] and m%maxii[1] >= n%maxii[2]):
        boxes(l,m%maxii[1],n,a,b,c)
        
    elif(n%maxii[2] >= l%maxii[0] and n%maxii[2] >= m%maxii[1]):
        boxes(l,m,n%maxii[2],a,b,c)


#BoxLabel
boxLabel = Label(root, text="Enter dimensions of Box (in mm)", bg='#08548e', fg='#ffffff', font=('Tahoma', 17, 'bold'))
boxLabel.place(x=60, y=40) 
    
#X entry
xLabel = Label(root, text="Enter X value:", bg='#0a5688', fg='#ffffff', font= ('Sans 12 bold'))
xLabel.place(x=100, y=100)


xInput=Entry(root,font= ('Lucida 12 bold'))
xInput.place(x=215, y=100)

#Y entry
yLabel = Label(root, text="Enter Y value:", bg='#0a5688', fg='#ffffff', font= ('Sans 12 bold'))
yLabel.place(x=100, y=150)

yInput=Entry(root, font= ('Lucida 12 bold'))
yInput.place(x=215, y=150)

#Z entry
zLabel = Label(root, text="Enter Z value:", bg='#0a5688', fg='#ffffff', font= ('Sans 12 bold'))
zLabel.place(x=100, y=200)

zInput=Entry(root,font= ('Lucida 12 bold'))
zInput.place(x=215, y=200)

button1=Button(root, text='Select STEP file', command=clicked,fg='#0b3252',bg='#f3954f', height=2, width=20, font= ('Tahoma 14 bold'))
button1.place(x=120, y=260)


root.mainloop()

