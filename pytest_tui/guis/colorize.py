# import all functions from the tkinter
import tkinter as tk
from tkinter.font import Font

# create a Pad class
class Pad(tk.Frame):

	# constructor to add buttons and text to the window
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)

		self.toolbar = tk.Frame(self, bg="#eee")
		self.toolbar.pack(side="top", fill="x")

		# this will add Highlight button in the window
		self.bold_btn = tk.Button(self.toolbar, text="Highlight",
								command=self.highlight_text)
		self.bold_btn.pack(side="left")

		# this will add Clear button in the window
		self.clear_btn = tk.Button(self.toolbar, text="Clear",
								command=self.clear)
		self.clear_btn.pack(side="left")

		# adding the text
		self.text = tk.Text(self)
		self.text.insert("end", "Pandemic has resulted in economic slowdown worldwide")
		self.text.focus()
		self.text.pack(fill="both", expand=True)

		#configuring a tag called start
		self.text.tag_configure("start", background="black", foreground="red")

	# method to highlight the selected text
	def highlight_text(self):

		# if no text is selected then tk.TclError exception occurs
		try:
			self.text.tag_add("start", "sel.first", "sel.last")
		except tk.TclError:
			pass

	# method to clear all contents from text widget.
	def clear(self):
		self.text.tag_remove("start", "1.0", 'end')

# function
def demo():

	# Create a GUI window
	root = tk.Tk()

	# place Pad object in the root window
	Pad(root).pack(expand=1, fill="both")

	# start the GUI
	root.mainloop()

# Driver code
if __name__ == "__main__":

	# function calling
	demo()
