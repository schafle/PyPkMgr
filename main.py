import Tkinter
import subprocess32 as subprocess

def exec_with_constraints(cmd, timeout=30, cwd=None):
		""" 
			Runs a process and returns stdout, stderr and exit_code:
			:param cmd: command used to run the process
			:return: tuple (stdout, stderr, exit_code) [ (str, str, int) OR (file, file, int) ],
			:raise ApplicationHangError: process timed out or could not be terminated properly.
		"""
		# kick off the process
		if not cwd:
			process = subprocess.Popen("pip install "+cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		else:
			process = subprocess.Popen("pip install "+cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
		#Try waiting for the process to finish and ....
		try:
			(stdout, stderr) = process.communicate(timeout=timeout)
		#kill it if it doesn't get completed before timeout happens
		except subprocess.TimeoutExpired:
			process.kill()
			(stdout, stderr) = process.communicate()
		
		# get exit code
		code = process.poll()

		return stdout, stderr, code

def get_installed_packages():
    import pip
    phonelist = pip.get_installed_distributions()
    phonelist = sorted([(i.key, i.version) for i in phonelist])
    return phonelist
		
class PyKkMgr(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.phonelist = get_installed_packages()
        self.initialize()
        self.setSelect()
	
    def whichSelected(self) :
        print "At %s of %d" % (select.curselection(), len(self.phonelist))
        return int(select.curselection()[0])

    def addEntry(self) :
        self.phonelist.append ([nameVar.get(), phoneVar.get()])
        setSelect ()

    def updateEntry(self) :
        self.phonelist[self.whichSelected()] = [nameVar.get(), phoneVar.get()]
        setSelect ()
    
    def deleteEntry(self) :
        del self.phonelist[self.whichSelected()]
        setSelect ()
    
    def loadEntry  (self) :
        name, phone = self.phonelist[self.whichSelected()]
        nameVar.set(name)
        phoneVar.set(phone)
	
    def initialize(self):
		global nameVar, phoneVar, select

		frame1 = Tkinter.Frame(self)
		frame1.pack()

		Tkinter.Label(frame1, text="Name").grid(row=0, column=0, sticky=Tkinter.W)
		nameVar = Tkinter.StringVar()
		name = Tkinter.Entry(frame1, textvariable=nameVar)
		name.grid(row=0, column=1, sticky=Tkinter.W)

		Tkinter.Label(frame1, text="Phone").grid(row=1, column=0, sticky=Tkinter.W)
		phoneVar= Tkinter.StringVar()
		phone= Tkinter.Entry(frame1, textvariable=phoneVar)
		phone.grid(row=1, column=1, sticky=Tkinter.W)

		frame2 = Tkinter.Frame(self)       # Row of buttons
		frame2.pack()
		b1 = Tkinter.Button(frame2,text=" Add  ",command=self.addEntry)
		b2 = Tkinter.Button(frame2,text="Update",command=self.updateEntry)
		b3 = Tkinter.Button(frame2,text="Delete",command=self.deleteEntry)
		b4 = Tkinter.Button(frame2,text=" Load ",command=self.loadEntry)
		b1.pack(side=Tkinter.LEFT); b2.pack(side=Tkinter.LEFT)
		b3.pack(side=Tkinter.LEFT); b4.pack(side=Tkinter.LEFT)

		frame3 = Tkinter.Frame(self)       # select of names
		frame3.pack()
		scroll = Tkinter.Scrollbar(frame3, orient=Tkinter.VERTICAL)
		select = Tkinter.Listbox(frame3, yscrollcommand=scroll.set, height=6)
		scroll.config (command=select.yview)
		scroll.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
		select.pack(side=Tkinter.LEFT,  fill=Tkinter.BOTH, expand=1)
	
    def setSelect(self) :
		self.phonelist.sort()
		select.delete(0,Tkinter.END)
		for name,phone in self.phonelist :
			select.insert (Tkinter.END, name)

if __name__ == "__main__":
    app = PyKkMgr()
    app.title('Python Package Manager')
    app.mainloop()