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
		
class PyKkMgr(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")

        button = Tkinter.Button(self,text=u"Click me !",
                                command=self.OnButtonClick)
        button.grid(column=1,row=0)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Hello !")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
	
    def OnButtonClick(self):
        cmd = self.entryVariable.get()
        #import pdb; pdb.set_trace()
        stdout, stderr, code = exec_with_constraints(cmd)
        self.labelVariable.set(stdout)
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
    app = PyKkMgr(None)
    app.title('Python Package Manager')
    app.mainloop()