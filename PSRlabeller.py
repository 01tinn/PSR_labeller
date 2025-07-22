"""
### Before using the program

Unzip the tarball to get get the generated folder


### To run the program:

$ python labeller_v1.py <folder name>

where <folder name> is the name of the base folder extracted from the tarball
### Note

PSR: pulsar candidate
Unk: not a pulsar but not obvious rfi either
RFI: RFI
Tier2: Something interesting or possible pulsar candidate

After pressing the Quit button or q key the program will generate a result file.

The filter/counting does not work until this results file is generated. Closing and running the script a second time will fix this.
"""

import tkinter as tk
from tkinter import *
import numpy as np
from astropy.io import ascii
from PIL import Image, ImageTk
import glob
import sys
import getpass

user = getpass.getuser()

### Candidates images ###

folder_name = sys.argv[1]

with open(folder_name + '/candidates.csv','r') as csv:
    lines = csv.readlines()

imgs = []
rank1s = []
rank2s = []
dms = []

for line in lines[1:]:
    img = line.split(',')[29]
    rank1 = float(line.split(',')[28])
    rank2 = float(line.split(',')[27])
    dm = float(line.split(',')[20])

    if dm > 2.0:
        imgs.append(img)
        rank1s.append(rank1)
        rank2s.append(rank2)
        dms.append(dm)
            
rankt = np.array(rank1s) + np.array(rank2s)
i = np.argsort(rankt)[::-1]

PSR_images = []
for j in i:
    PSR_images.append(folder_name + '/' + imgs[j])

PSR_results = []
count_for_search = str(np.arange(len(PSR_images))+1)
#print(count_for_search)

find_result = glob.glob('result_'+user+'_'+folder_name+'.csv')
if find_result == []:
    for i in range(0,len(PSR_images)):
        PSR_results.append('None')
    #print(PSR_results)

else:
    name_results, PSR_results = np.loadtxt(find_result[0],str,skiprows = 1,usecols = (0,1),unpack=True)
    # change result form v1.1 to newer version
    PSR_results = np.where(PSR_results=='UNK', 'Noise', PSR_results)
'''
else:
    name_results, PSR_results2 = np.loadtxt(find_result[0],str,skiprows = 1,usecols = (0,1),unpack=True)
    # change result form v1.1 to newer version
    PSR_results2 = np.where(PSR_results2=='UNK', 'Noise', PSR_results2)
    #print(PSR_results)
    for i in range(0,len(PSR_images)):
        PSR_results.append('None')
    for i in range (0,len(name_results)):
        PSR_results[PSR_images.index(name_results[i].replace('candidates/',''))] = PSR_results2[i]
'''

i = 0
j = 2

real_width = 2339
real_height = 1653

width = [round(0.3*real_width),round(0.4*real_width),round(0.5*real_width),round(0.7*real_width),round(0.8*real_width),real_width]
height = [round(0.3*real_height),round(0.4*real_height),round(0.5*real_height),round(0.7*real_height),round(0.8*real_height),real_height]


forfilter = np.arange(len(PSR_images))

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()
    
    #Creation of init_window
    def init_window(self):
        ### apply filter
        def checkfilter():
            global CheckVar1, CheckVar2, CheckVar3, CheckVar4, img, i, j, forfilter, w, wr, wr_name
            filterpsr = np.where(PSR_results == 'PSR')
            filterunk = np.where(PSR_results == 'Noise')
            filterrfi = np.where(PSR_results == 'RFI')
            filternon = np.where(PSR_results == 'None')
            filtert2 = np.where(PSR_results == 'Tier2')
            forfilter = []
            if self.CheckVar1.get() == 1:
                forfilter = np.concatenate([forfilter,filternon[0]])
            if self.CheckVar2.get() == 1:
                forfilter = np.concatenate([forfilter,filterpsr[0]])
            if self.CheckVar3.get() == 1:
                forfilter = np.concatenate([forfilter,filterunk[0]])
            if self.CheckVar4.get() == 1:
                forfilter = np.concatenate([forfilter,filterrfi[0]])
            if self.CheckVar5.get() == 1:
                forfilter = np.concatenate([forfilter,filtert2[0]])
            forfilter = np.sort(forfilter)
            forfilter = forfilter.astype(int)
            i = 0
            img.destroy()
            load = Image.open(PSR_images[forfilter[i]])
            load = load.resize((width[j],height[j]), Image.Resampling.LANCZOS)
            render = ImageTk.PhotoImage(load)
            img = Label(self, image=render)
            img.image = render
            img.place(x=0, y=75)
            w = tk.Label(root, text=str(forfilter[i]+1)+' out of '+str(len(PSR_images))+'     ')
            w.place(x=200, y=25)
            wr = tk.Label(root, text='classification: ' + str(PSR_results[forfilter[i]]) + ' ')
            wr.place(x=600, y=25) 
            wr_name = tk.Label(root, text=str(PSR_images[forfilter[i]]) +'  ')
            wr_name.place(x=0, y=0)
            #print(forfilter)
            return forfilter

        
        # move to next image
        def forward():
            global i, j, img, w, wr, wr_name
            i = i + 1
            if i > len(forfilter) - 1:
                i = i - 1
            img.destroy()
            w.destroy()
            wr.destroy()
            wr_name.destroy()
            load = Image.open(PSR_images[forfilter[i]])
            load = load.resize((width[j],height[j]), Image.Resampling.LANCZOS)
            render = ImageTk.PhotoImage(load)
            load.close()
            img = Label(self, image=render)
            img.image = render
            img.place(x=0, y=75)
            w = tk.Label(root, text=str(forfilter[i]+1)+' out of '+str(len(PSR_images))+'     ')
            w.place(x=200, y=25)
            wr = tk.Label(root, text='classification: ' + str(PSR_results[forfilter[i]]) + '   ')
            wr.place(x=600, y=25)   
            wr_name = tk.Label(root, text=str(PSR_images[forfilter[i]]) +'  ')
            wr_name.place(x=0, y=0)
            

        # move to previous image
        def backward():
            global i, j, img, w, wr, wr_name
            i = i - 1
            if i < 0:
                i = i + 1
            img.destroy()
            w.destroy()
            wr.destroy()
            wr_name.destroy()
            load = Image.open(PSR_images[forfilter[i]])
            load = load.resize((width[j],height[j]), Image.Resampling.LANCZOS)
            render = ImageTk.PhotoImage(load)
            load.close()
            img = Label(self, image=render)
            img.image = render
            img.place(x=0, y=75)
            w = tk.Label(root, text=str(forfilter[i]+1)+' out of '+str(len(PSR_images))+'     ')
            w.place(x=200, y=25)
            wr = tk.Label(root, text='classification: ' + str(PSR_results[forfilter[i]]) + '   ')
            wr.place(x=600, y=25) 
            wr_name = tk.Label(root, text=str(PSR_images[forfilter[i]]) +'  ')
            wr_name.place(x=0, y=0)
        
            
            
        # pulsar!    
        def tup():
            global i, j, img, wr, wnone, wpsr, wunk, wrfi, wt2
            wr.destroy()
            wnone.destroy()
            wpsr.destroy()
            wunk.destroy()
            wrfi.destroy()
            wt2.destroy()
            PSR_results[forfilter[i]] = 'PSR'
            wr = tk.Label(root, text='classification: ' + str(PSR_results[forfilter[i]])+'   ')
            wr.place(x=600, y=25)
            wnone = tk.Label(root, text='None = '+str(len(np.where(PSR_results == 'None')[0]))+'     ')
            wnone.place(x=1300, y=25)
            wpsr = tk.Label(root, text='PSR = '+str(len(np.where(PSR_results == 'PSR')[0]))+'     ')
            wpsr.place(x=1450, y=25)
            wunk = tk.Label(root, text='Noise = '+str(len(np.where(PSR_results == 'Noise')[0]))+'     ')
            wunk.place(x=1300, y=50)
            wrfi = tk.Label(root, text='RFI = '+str(len(np.where(PSR_results == 'RFI')[0]))+'     ')
            wrfi.place(x=1450, y=50)
            wt2 = tk.Label(root, text='Tier2 cand = '+str(len(np.where(PSR_results == 'Tier2')[0]))+'     ')
            wt2.place(x=1600, y=25)
            forward()

        #none pulsar    
        def tdown():
            global i, j, img, wr, wnone, wpsr, wunk, wrfi, wt2
            wr.destroy()
            wnone.destroy()
            wpsr.destroy()
            wunk.destroy()
            wrfi.destroy()
            wt2.destroy()
            PSR_results[forfilter[i]] = 'Noise'
            wr = tk.Label(root, text='classification: ' + str(PSR_results[forfilter[i]])+'   ')
            wr.place(x=600, y=25)
            wnone = tk.Label(root, text='None = '+str(len(np.where(PSR_results == 'None')[0]))+'     ')
            wnone.place(x=1300, y=25)
            wpsr = tk.Label(root, text='PSR = '+str(len(np.where(PSR_results == 'PSR')[0]))+'     ')
            wpsr.place(x=1450, y=25)
            wunk = tk.Label(root, text='Noise = '+str(len(np.where(PSR_results == 'Noise')[0]))+'     ')
            wunk.place(x=1300, y=50)
            wrfi = tk.Label(root, text='RFI = '+str(len(np.where(PSR_results == 'RFI')[0]))+'     ')
            wrfi.place(x=1450, y=50)
            wt2 = tk.Label(root, text='Tier2 cand = '+str(len(np.where(PSR_results == 'Tier2')[0]))+'     ')
            wt2.place(x=1600, y=25)
            forward()

        #RFI    
        def trfi():
            global i, j, img, wr, wnone, wpsr, wunk, wrfi, wt2
            wr.destroy()
            wnone.destroy()
            wpsr.destroy()
            wunk.destroy()
            wrfi.destroy()
            wt2.destroy()
            PSR_results[forfilter[i]] = 'RFI'
            wr = tk.Label(root, text='classification: ' + str(PSR_results[forfilter[i]])+'   ')
            wr.place(x=600, y=25)
            wnone = tk.Label(root, text='None = '+str(len(np.where(PSR_results == 'None')[0]))+'     ')
            wnone.place(x=1300, y=25)
            wpsr = tk.Label(root, text='PSR = '+str(len(np.where(PSR_results == 'PSR')[0]))+'     ')
            wpsr.place(x=1450, y=25)
            wunk = tk.Label(root, text='Noise = '+str(len(np.where(PSR_results == 'Noise')[0]))+'     ')
            wunk.place(x=1300, y=50)
            wrfi = tk.Label(root, text='RFI = '+str(len(np.where(PSR_results == 'RFI')[0]))+'     ')
            wrfi.place(x=1450, y=50)
            wt2 = tk.Label(root, text='Tier2 cand = '+str(len(np.where(PSR_results == 'Tier2')[0]))+'     ')
            wt2.place(x=1600, y=25)
            forward()

        #pulsar-like    
        def t2():
            global i, j, img, wr, wnone, wpsr, wunk, wrfi, wt2
            wr.destroy()
            wnone.destroy()
            wpsr.destroy()
            wunk.destroy()
            wrfi.destroy()
            wt2.destroy()
            PSR_results[forfilter[i]] = 'Tier2'
            wr = tk.Label(root, text='classification: ' + str(PSR_results[forfilter[i]])+'   ')
            wr.place(x=600, y=25)
            wnone = tk.Label(root, text='None = '+str(len(np.where(PSR_results == 'None')[0]))+'     ')
            wnone.place(x=1300, y=25)
            wpsr = tk.Label(root, text='PSR = '+str(len(np.where(PSR_results == 'PSR')[0]))+'     ')
            wpsr.place(x=1450, y=25)
            wunk = tk.Label(root, text='Noise = '+str(len(np.where(PSR_results == 'Noise')[0]))+'     ')
            wunk.place(x=1300, y=50)
            wrfi = tk.Label(root, text='RFI = '+str(len(np.where(PSR_results == 'RFI')[0]))+'     ')
            wrfi.place(x=1450, y=50)
            wt2 = tk.Label(root, text='Tier2 cand = '+str(len(np.where(PSR_results == 'Tier2')[0]))+'     ')
            wt2.place(x=1600, y=25)
            forward() 
            
        #rescale
        def plusscale():
            global j
            global img
            if j != 5:
                j = j + 1
                img.destroy()
                load = Image.open(PSR_images[i])
                load = load.resize((width[j],height[j]), Image.Resampling.LANCZOS)
                render = ImageTk.PhotoImage(load)
                img = Label(self, image=render)
                img.image = render
                img.place(x=0, y=75)
        def minusscale():
            global j
            global img
            if j != 0:
                j = j - 1
                img.destroy()
                load = Image.open(PSR_images[i])
                load = load.resize((width[j],height[j]), Image.Resampling.LANCZOS)
                render = ImageTk.PhotoImage(load)
                img = Label(self, image=render)
                img.image = render
                img.place(x=0, y=75)

        ### Searching by order
        def search():
            global i, j, img, CheckVar1, CheckVar2, CheckVar3, CheckVar4, forfilter, w, wr, wnone
            i_dummy=search_entry.get()
            if i_dummy in count_for_search:
                i = int(i_dummy)-1
                img.destroy()
                load = Image.open(PSR_images[i])
                load = load.resize((width[j],height[j]), Image.Resampling.LANCZOS)
                render = ImageTk.PhotoImage(load)
                img = Label(self, image=render)
                img.image = render
                img.place(x=0, y=75)
                w = tk.Label(root, text=str(i+1)+' out of '+str(len(PSR_images))+'     ')
                w.place(x=200, y=25)
                wr = tk.Label(root, text='classification: ' + str(PSR_results[i]) + ' ')
                wr.place(x=600, y=25) 
                wr_name = tk.Label(root, text=str(PSR_images[i]) +'  ')
                wr_name.place(x=0, y=0)
                self.CheckVar1 = IntVar(value=1)
                self.CheckVar2 = IntVar(value=1)
                self.CheckVar3 = IntVar(value=1)
                self.CheckVar4 = IntVar(value=1)
                self.CheckVar5 = IntVar(value=1)
                Cnone = Checkbutton(root, text = "None", variable = self.CheckVar1, onvalue = 1, offvalue = 0, height=2, width = 5)
                Cpsr = Checkbutton(root, text = "PSR", variable = self.CheckVar2, onvalue = 1, offvalue = 0, height=2, width = 5)
                Cunk = Checkbutton(root, text = "Noise", variable = self.CheckVar3, onvalue = 1, offvalue = 0, height=2, width = 5)
                Crfi = Checkbutton(root, text = "RFI", variable = self.CheckVar4, onvalue = 1, offvalue = 0, height=2, width = 5)
                Ct3 = Checkbutton(root, text = "Tier2", variable = self.CheckVar5, onvalue = 1, offvalue = 0, height=2, width = 5)
                Cnone.place(x=1000,y=25)
                Cpsr.place(x=1050,y=25)
                Cunk.place(x=1100,y=25)
                Crfi.place(x=1150,y=25)
                Ct2.place(x=1200,y=25)
                forfilter = np.arange(len(PSR_images))
                return forfilter



            
        # changing the title of our master widget      
        self.master.title("CandidateLabeller")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating buttons instance
        quitButton = Button(self, text="Quit(q)",command=self.quit)
        root.bind("<q>", lambda x: self.quit())
        backButton = Button(self, text="back(a)",command=backward)
        root.bind("<a>", lambda x: backward())
        nextButton = Button(self, text="next(d)",command=forward)
        root.bind("<d>", lambda x: forward())
        rfiButton = Button(self, text="RFI(i)",command=trfi)
        root.bind("<i>", lambda x: trfi())
        tdownButton = Button(self, text="Noise(o)",command=tdown)
        root.bind("<o>", lambda x: tdown())
        tupButton = Button(self, text="PSR(p)",command=tup)
        root.bind("<p>", lambda x: tup())
        t2Button = Button(self, text="Tier2(j)",command=t2)
        root.bind("<j>", lambda x: t2())
        plusButton = Button(self, text="Zoom in(l)",command=plusscale)
        root.bind("<l>", lambda x: plusscale())
        minusButton = Button(self, text="Zoom out(k)",command=minusscale)
        root.bind("<k>", lambda x: minusscale())
        filterButton = Button(self, text="Filter(f)",command=checkfilter)
        root.bind("<f>", lambda x: checkfilter())
        
        
        # placing the button on my window
        quitButton.place(x=0, y=50)
        backButton.place(x=90, y=50)
        nextButton.place(x=180, y=50)
        rfiButton.place(x=270,y=50)
        tdownButton.place(x=360, y=50)
        tupButton.place(x=450, y=50)
        t2Button.place(x=540,y=50)
        plusButton.place(x=630, y=50)
        minusButton.place(x=740, y=50)
        filterButton.place(x=1075, y=50)
        
        global img, w, wr, wr_name, wnone, wpsr, wunk, wrfi, wt2
        load = Image.open(PSR_images[i])
        load = load.resize((width[j],height[j]), Image.Resampling.LANCZOS)
        render = ImageTk.PhotoImage(load)
        
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=75)

        w = tk.Label(root, text=str(i+1)+' out of '+str(len(PSR_images))+'     ')
        w.place(x=200, y=25)
        v = StringVar()
        wr = tk.Label(root, text= 'classification: ' + str(PSR_results[i]))
        wr.place(x=600, y=25)
        wr_name = tk.Label(root, text=str(PSR_images[i]) +'  ')
        wr_name.place(x=0, y=0)

        ### searching
        search_entry = tk.Entry(root,font=('calibre',10,'normal')) 
        search_entry.place(x=850,y=25)
        search_btn=tk.Button(root,text = 'Search', command = search)
        search_btn.place(x=880,y=50)

        ### Filter
        #wr = tk.Label(root, text= 'Filter')
        #wr.place(x=1075, y=0)
        self.CheckVar1 = IntVar(value=1)
        self.CheckVar2 = IntVar(value=1)
        self.CheckVar3 = IntVar(value=1)
        self.CheckVar4 = IntVar(value=1)
        self.CheckVar5 = IntVar(value=1)
        Cnone = Checkbutton(root, text = "None", variable = self.CheckVar1, onvalue = 1, offvalue = 0, height=2, width = 5)
        Cpsr = Checkbutton(root, text = "PSR", variable = self.CheckVar2, onvalue = 1, offvalue = 0, height=2, width = 5)
        Cunk = Checkbutton(root, text = "Noise", variable = self.CheckVar3, onvalue = 1, offvalue = 0, height=2, width = 5)
        Crfi = Checkbutton(root, text = "RFI", variable = self.CheckVar4, onvalue = 1, offvalue = 0, height=2, width = 5)
        Ct2 = Checkbutton(root, text = "Tier2", variable = self.CheckVar5, onvalue = 1, offvalue = 0, height=2, width = 5)
        Cnone.place(x=1000,y=20)
        Cpsr.place(x=1050,y=20)
        Cunk.place(x=1100,y=20)
        Crfi.place(x=1150,y=20)
        Ct2.place(x=1200,y=20)


        wnone = tk.Label(root, text='None = '+str(len(np.where(PSR_results == 'None')[0]))+'     ')
        wnone.place(x=1300, y=25)
        wpsr = tk.Label(root, text='PSR = '+str(len(np.where(PSR_results == 'PSR')[0]))+'     ')
        wpsr.place(x=1450, y=25)
        wunk = tk.Label(root, text='Noise = '+str(len(np.where(PSR_results == 'Noise')[0]))+'     ')
        wunk.place(x=1300, y=50)
        wrfi = tk.Label(root, text='RFI = '+str(len(np.where(PSR_results == 'RFI')[0]))+'     ')
        wrfi.place(x=1450, y=50)
        wt2 = tk.Label(root, text='Tier2 cand = '+str(len(np.where(PSR_results == 'Tier2')[0]))+'     ')
        wt2.place(x=1600, y=25)



        
        #print(self.CheckVar1.get())
        def quit():
            self.root.destroy()


root = Tk()

#size of the window
root.geometry("2400x1800")

app = Window(root)
root.mainloop() 


PSR=[]
Noise=[]
RFI=[]
Tier2=[]
#writing csv file
for i in range (0,len(PSR_results)):
    if PSR_results[i] == 'PSR':
        PSR.append('True')
        Noise.append('False')
        RFI.append('False')
        Tier2.append('False')
    elif PSR_results[i] == 'Noise':
        PSR.append('False')
        Noise.append('True')
        RFI.append('False')
        Tier2.append('False')
    elif PSR_results[i] == 'RFI':
        PSR.append('False')
        Noise.append('False')
        RFI.append('True')
        Tier2.append('False')
    elif PSR_results[i] == 'Tier2':
        PSR.append('False')
        Noise.append('False')
        RFI.append('False')
        Tier2.append('True')
    else:
        PSR.append('-')
        Noise.append('-')
        RFI.append('-')
        Tier2.append('-')
#print(PSR_results)
ascii.write([PSR_images, PSR_results,PSR,Noise,RFI,Tier2], 'result_' + user + '_' + folder_name+'.csv', names=['name', 'type','PSR','Noise','RFI','Tier2'], fast_writer=False)

