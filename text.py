from tkinter import *
from tkinter import filedialog
import os

GREEN = (0,255,0)


class Menubar:
  def __init__(self, parent):
    menu = Menu(parent.master, font=("Fira Code", 11))
    parent.master.config(menu=menu)

    # File menubar item
    file_dropdown = Menu(menu, tearoff=0, font=("Fira Code", 8))
    file_dropdown.add_command(label="New File", accelerator="Ctrl+N", command=parent.new_file)
    file_dropdown.add_command(label="Open File", accelerator="Ctrl+O",command=parent.open_file)
    file_dropdown.add_separator()
    file_dropdown.add_command(label="Save", accelerator="Ctrl+S",command=parent.save)
    file_dropdown.add_command(label="Save as", accelerator="Ctrl+Shift+S",command=parent.save_as)
    file_dropdown.add_separator()
    file_dropdown.add_command(label="Exit", command=parent.exit)
    menu.add_cascade(label="File", menu=file_dropdown)

class Statusbar:
  def __init__(self, parent):
    self.status_bar = StringVar()
    self.status_bar.set("DG Text - 0.1 Hero")

    label = Label(parent.textarea, textvariable=self.status_bar, fg="green",
                  bg="black", font=("Fira Code", 8), anchor="sw")
    label.pack(side=BOTTOM, fill=BOTH)

  def update_status(self, *args):
    if isinstance(args[0], bool):
      self.status_bar.set("Your file has been saved.")
    else:
      self.status_bar.set("DG Text - 0.1 Hero")

class Application:
  def __init__(self, master):

    # Root or window configuration
    master.title("Untitle - DG Text")
    master.geometry("1380x800")
    master.configure(bg="black")
    self.master = master

    self.filename = None

    # Text configuration
    self.textarea = Text(master, bg="black", fg="#33FF33", bd="0", selectbackground="#009900")
    self.textarea.pack(side=LEFT, fill=BOTH, expand=True)
    self.textarea.configure(pady=5, insertbackground="#33FF33", font=("Fira Code", 10))

    # Scrollbar configuration
    self.scroll = Scrollbar(master, command=self.textarea.yview)
    # self.scroll.pack(side=RIGHT)

    # Menu configuration
    self.menu = Menubar(self)

    # Status Configuration
    self.status = Statusbar(self)

    self.bind_key()

  def new_title(self, name=None):
    if name:
      self.master.title(name + " - DG Text")
    else:
      self.master.title("Untitle - DG Text")

  def new_file(self, *args):
    self.textarea.delete(1.0, END)
    self.filename = None
    self.new_title()

  def open_file(self, *args):
    self.filename = filedialog.askopenfilename(
      defaultextension=".txt",
      filetypes=[("All Files", "*.*"),
                  ("Text Files", "*.txt"),
                  ("Python Files", "*.py"),
                  ("Html Files", "*.html"),
                  ("Css Files", "*.css"),
                  ("Javascipt Files", "*.js"),
                  ("java Files", "*.java"),])
    if self.filename:
      self.textarea.delete(1.0, END)
      with open(self.filename, "r") as f:
        self.textarea.insert(1.0, f.read())
      file_name = os.path.splitext(os.path.basename(self.filename))[0]
      self.new_title(file_name)

  def save(self, *args):
    if self.filename:
      try:
        text_content = self.textarea.get(1.0, END)
        with open(self.filename, "w") as f:
          f.write(text_content)
        self.status.update_status(True)
      except Exception as e:
        print(e)
    else:
      self.save_as()

  def save_as(self, *args):
    try:
        new_file = filedialog.asksaveasfilename(
          initialfile="Untitled.txt",
          defaultextension=".txt",
          filetypes=[("All Files", "*.*"),
                  ("Text Files", "*.txt"),
                  ("Python Files", "*.py"),
                  ("Html Files", "*.html"),
                  ("Css Files", "*.css"),
                  ("Javascipt Files", "*.js"),
                  ("java Files", "*.java"),])
        textarea_content = self.textarea.get(1.0, END)
        with open(new_file, "w") as f:
          f.write(textarea_content)
        self.filename = new_file
        file_name = os.path.splitext(os.path.basename(self.filename))[0]
        self.new_title(file_name)
        self.status.update_status(True)

    except Exception as e:
        print(e)

  def bind_key(self):
    self.textarea.bind("<Control-n>", self.new_file)
    self.textarea.bind("<Control-o>", self.open_file)
    self.textarea.bind("<Control-s>", self.save)
    self.textarea.bind("<Control-S>", self.save_as)
    self.textarea.bind("<Key>", self.status.update_status)

  def exit(self):
    pass

if __name__ == "__main__":
  root = Tk()
  app = Application(root)
  root.mainloop()