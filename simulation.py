from asyncio import threads
from asyncio.windows_events import NULL
from cProfile import label
from glob import glob
from textwrap import fill
from tkinter import *
from tokenize import String
from turtle import width
import time
import threading
import scene1
import random
from PIL import ImageTk, Image

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def takeFirst(elem):
    return elem[0]

def update_setting():
    global passengerNumber
    passengerNumber = int(var_passenger_number.get())

    global maxSpeed
    maxSpeed = float(var_max_speed.get())

    global minSpeed
    minSpeed = float(var_min_speed.get())
    
    global interval
    interval = float(var_interval.get())

    global playspeed
    playspeed = float(var_playSpeed.get())
    print("Settings Updated:\nPassenger Numbers {0}\nMax Speed {1}\nMin Speed {2}\nInterval {3} s\nPlay Speed {4}x".format(passengerNumber,maxSpeed,minSpeed,interval,playspeed)
    )
def move_figure(passenger,figure,dx,dy):
    cv.move(figure,dx,dy)
    passenger.xpos += dx
    passenger.ypos += dy

def generate_passenger():
    global ID
    starttime = time.time()
    actual_speed = random.uniform(minSpeed,maxSpeed)
    speed = actual_speed * currentScene.prop * 0.1 * playspeed
    actual_rowspeed = random.uniform(minSpeed,maxSpeed) / 3
    rowspeed = actual_rowspeed * currentScene.prop * 0.1 * playspeed
    strength = random.randint(1,5)
    row = random.randint(1,currentScene.maxRow)
    column = random.randint(1,currentScene.maxColumn)
    while(currentScene.seatsUsed[row][column]):
        row = random.randint(1,currentScene.maxRow)
        column = random.randint(1,currentScene.maxColumn)
    currentScene.seatsUsed[row][column] = True
    weight = [random.randint(1,100),random.randint(1,100)]
    randomized_passenger = People(ID,speed,rowspeed,strength,weight,(row,column),lane_start,lane)
    ID += 1
    passengers.append(randomized_passenger)
    endtime = time.time()
    print("[Generation] Generated random passenger: seat {}, speed {:.3f} m/s, rowspeed {:.3f} m/s, bags {}, using time {:.6f} s".format((row,column),actual_speed,actual_rowspeed,weight,endtime-starttime))

def clear_simulation():
    currentScene.seatsUsed.clear()
    currentScene.initialize()
    currentScene.rowBusy.clear()
    passengers.clear()
    cv.delete("all")
    cv.create_image(0, 0, anchor='nw',image=image_file)
    cv.create_circle(lane_start, lane, 10, fill='yellow')
    cv.update()

def replay():
    currentScene.seatsUsed.clear()
    currentScene.initialize()
    currentScene.rowBusy.clear()
    cv.delete("all")
    cv.create_image(0, 0, anchor='nw',image=image_file)
    cv.create_circle(lane_start, lane, 10, fill='yellow')
    cv.update()
#Settings
passengerNumber = 10
maxSpeed = 2
minSpeed = 0.8
interval = 1
playspeed = 1

#current scene in use
currentScene = scene1
image_file = NULL

#the y value of the starting point
lane = currentScene.lane

#the x value of the starting point
lane_start = currentScene.lane_start

#global variable canvas
global cv

#list of all passengers
passengers = []
ID = 0

#is the simulation paused
isPause = False

#Time used
generationTime = 0
runTime = 0
totalTime = 0

class People:
    def __init__(self, ID,speed, rowspeed,strength,bags,seat,x,y):
        self.ID = ID
        #moving speed in passthroughs, in m/s
        self.speed = speed
        #moving speed in rows, in m/s
        self.rowspeed = rowspeed
        #strength of lifting their bags overhead, in N
        self.strength = strength
        #The weight of bags carrying, in Kg
        self.bags = bags
        #coordinate of the seat
        (self.seat_row,self.seat_column)=seat
        #current status
        self.status = 0
        #current coordinate
        (self.xpos,self.ypos) = (x,y)

class Behaviours(threading.Thread):
    def __init__(self, threadID, passenger):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.passenger = passenger
    def run(self):
        print("[Thread{0}] Thread started".format(self.threadID))
        starttime = time.time()
        #assign random color to the figure
        color = "#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])

        #create one's figure on the canvas
        self.figure = cv.create_circle(self.passenger.xpos,self.passenger.ypos,5,fill=color)
        currentScene.rowBusy.append((self.passenger.xpos,self.passenger.ID))
        while(self.passenger.xpos < currentScene.rows[self.passenger.seat_row]):
            #moving in walkthrough to one's row
            currentSpeed = self.passenger.speed
            if(self.passenger.xpos + self.passenger.speed > currentScene.rows[self.passenger.seat_row]):
                currentSpeed = currentScene.rows[self.passenger.seat_row] - self.passenger.xpos
            next = 100000
            if(currentScene.rowBusy.index((self.passenger.xpos,self.passenger.ID)) < len(currentScene.rowBusy) - 1):
                next = currentScene.rowBusy[currentScene.rowBusy.index((self.passenger.xpos,self.passenger.ID))+1][0]
            if(not isPause and next-self.passenger.xpos >= 10):
                currentScene.rowBusy.remove((self.passenger.xpos,self.passenger.ID))
                currentScene.rowBusy.append((self.passenger.xpos + currentSpeed,self.passenger.ID))
                currentScene.rowBusy.sort(key=takeFirst)
                move_figure(self.passenger,self.figure,currentSpeed,0)
                #print("Current coordinate is ({0},{1})".format(self.passenger.xpos,self.passenger.ypos))
            time.sleep(0.1)
        #time.sleep()
        currentScene.rowBusy.remove((self.passenger.xpos,self.passenger.ID))
        currentSpeed = self.passenger.rowspeed
        if(self.passenger.seat_column >= 4):
            #moving down to one's seat
            while(self.passenger.ypos < currentScene.columns[self.passenger.seat_column]):
                if(self.passenger.ypos + self.passenger.rowspeed > currentScene.columns[self.passenger.seat_column]):
                    currentSpeed = currentScene.columns[self.passenger.seat_column] - self.passenger.ypos
                if(not isPause):
                    move_figure(self.passenger,self.figure,0,currentSpeed)
                    #print("Current coordinate is ({0},{1})".format(self.passenger.xpos,self.passenger.ypos))
                time.sleep(0.1)
        else:
            #moving up to one's seat
            while(self.passenger.ypos > currentScene.columns[self.passenger.seat_column]):
                if(self.passenger.ypos - self.passenger.rowspeed < currentScene.columns[self.passenger.seat_column]):
                    currentSpeed = self.passenger.ypos - currentScene.columns[self.passenger.seat_column]
                if(not isPause):
                    move_figure(self.passenger,self.figure,0,-currentSpeed)
                    #print("Current coordinate is ({0},{1})".format(self.passenger.xpos,self.passenger.ypos))
                time.sleep(0.1)
        
        endtime = time.time()
        print("[Thread{}] Passenger# {} stopped at ({:.0f},{:.0f}), using time: {:.6f} ({:.6f}) seconds".format(self.threadID,self.passenger.ID,self.passenger.xpos,self.passenger.ypos,(endtime-starttime) * playspeed,endtime-starttime))

class Generate(threading.Thread):
    def __init__(self, number):
        threading.Thread.__init__(self)
        #numbers of random passengers generated
        self.number = number
    def run(self):
        threads = []
        startTime = time.time()
        for i in range(self.number):
            print("[Generation] Generating passenger #{0}...".format(i))
            generate_passenger()
        endTime = time.time()
        global generationTime
        generationTime = endTime - startTime
        print("[Generation] Generation finished. {} passengers generated. Total time: {:.6f} seconds".format(self.number,generationTime))
        runStartTime = time.time()
        for i in range(self.number):
            exec("thread{0} = Behaviours({0},passengers[{0}])".format(i))
            exec("threads.append(thread{0})".format(i))
            exec("thread{0}.start()".format(i))
            time.sleep(interval / playspeed)
        for t in threads:
            t.join()
        endTime = time.time()
        global totalTime
        global runTime
        totalTime = endTime - startTime
        runTime = endTime - runStartTime
        print("[Main Thread] All passengers have stopped. The simulation terminated")
        print('-'*30)
        print("{:30s}{:10.6f} Seconds".format("Generation Time",generationTime))
        print("{:30s}{:10.6f} Seconds".format("Simulation Time (Actual)",runTime))
        print("{:30s}{:10.6f} Seconds".format("Total Runtime",totalTime))
        print("\n{:30s}{:17.2f}x".format("Playspeed",playspeed))
        print("{:30s}{:10.6f} Seconds".format("Simulation Time (Equvalent)",runTime * playspeed))
#initialize the simulation
def generate_simulation():
    global isPause
    isPause = False
    thread = Generate(passengerNumber)
    thread.start()

#resume the simulation
def play_simulation():
    global isPause
    isPause = False

#pause the simulation
def pause_simulation():
    global isPause
    isPause = True

#basic form settings
root = Tk()
root.title("Simulation")
root.geometry('1300x650')

#frames
frame1 = Frame(root,bg='gray',height = 400,width=200)
frame2 = Frame(root,bg='gray',height = 200,width=200)
frame3 = Frame(root,bg='red')
frame1.place(x=20, y=20, anchor='nw')
frame2.place(x=20, y=440, anchor='nw')
frame3.place(x=230, y=20, anchor='nw')

#entry area
var_passenger_number = StringVar()
var_passenger_number.set(str(passengerNumber))
Label(frame1,text="Number of passengers").pack(padx=10)
entryNumber = Entry(frame1,textvariable=var_passenger_number)
entryNumber.pack(padx= 10,pady=10)

var_max_speed = StringVar()
var_max_speed.set(str(maxSpeed))
Label(frame1,text="Max Speed").pack(padx=10)
entryMaxSpeed = Entry(frame1,textvariable=var_max_speed)
entryMaxSpeed.pack(padx= 10,pady=10)

var_min_speed = StringVar()
var_min_speed.set(str(minSpeed))
Label(frame1,text="Min Speed").pack(padx=10)
entryMinSpeed = Entry(frame1,textvariable=var_min_speed)
entryMinSpeed.pack(padx= 10,pady=10)

var_interval = StringVar()
var_interval.set(str(interval))
Label(frame1,text="Interval").pack(padx=10)
entryInterval = Entry(frame1,textvariable=var_interval)
entryInterval.pack(padx= 10,pady=10)

var_playSpeed = StringVar()
var_playSpeed.set(str(playspeed))
Label(frame1,text="Play Speed").pack(padx=10)
entryPlaySpeed = Entry(frame1,textvariable=var_playSpeed)
entryPlaySpeed.pack(padx= 10,pady=10)

buttonSubmit = Button(frame1,text="OK",command=update_setting)
buttonSubmit.pack(padx=10,pady=10)

#control area
buttonGenerate = Button(frame2, text="Generate", command=generate_simulation)
buttonGenerate.pack(padx=5,pady=5)
buttonPause = Button(frame2, text="Pause", command=pause_simulation)
buttonPause.pack(padx=5,pady=5)
buttonPlay = Button(frame2, text="Play", command=play_simulation)
buttonPlay.pack(padx=5,pady=5)
buttonReplay = Button(frame2, text="Replay", command=play_simulation)
buttonReplay.pack(padx=5,pady=5)
buttonReset = Button(frame2, text="Reset", command=clear_simulation)
buttonReset.pack(padx=5,pady=5)

#canvas
cv = Canvas(frame3,height = 400,width = 1100)

#background image
image_file = ImageTk.PhotoImage(Image.open(currentScene.backgroundPicture))
cv.create_image(0, 0, anchor='nw',image=image_file)

#start point
cv.create_circle(lane_start, lane, 10, fill='yellow')

#pack canvas
cv.pack()

#start mainloop
root.mainloop()