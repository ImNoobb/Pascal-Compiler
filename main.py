from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess,os
from PIL import ImageTk, Image
from tkinter import messagebox as mb

# Varibles === #
file_path = ''
save_yet = False

# Definds #
def set_file_path(path):
    global file_path
    file_path = path

def new_file():
    if editor.get("1.0",END) == "\n":
        set_file_path('')
        pass
    elif save_file_notice():
        pass
    editor.delete('1.0', END)
    set_file_path('')

def open_file():
    if editor.get("1.0",END) == '\n':
        pass_=True
    elif save_file_notice() and pass_==False:
        pass
    path = askopenfilename(filetypes=[('Pascal Files', '*.pas')])
    if path:
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0',code)
    set_file_path(path)

def save_file(e):
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Pascal Files', '*.pas')])
        if not '.pas' in path and path!='':
            path += '.pas'
    else:
        path = file_path
    if path:
        with open(path, 'w') as file:
            code = editor.get('1.0',END)
            file.write(code)
        set_file_path(path)
        return True
    else:
        return False
    
def save_as_file():
    path = asksaveasfilename(filetypes=[('Pascal Files', '*.pas')])
    if path:
        with open(path,'w') as file:
            code = editor.get('1.0',END)
            file.write(code)
        set_file_path(path)

def quit_():
    if save_file_notice():
        pass
    window.destroy()

def compile_file():
    compile_message = ''
    if save_file():
        compile_path = file_path.replace('\\','\\\\')
        command = f'fpc {compile_path}'
        process = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output,error = process.communicate()

        if 'Error:' in str(output):
            status_text.config(text="Tr???ng th??i: L???i",fg='red')
            code_output.config(fg='red')
            compile_message = "???? x???y ra l???i!\n"+str(output.decode('utf-8'))
        else:
            status_text.config(text="Tr???ng th??i: ???n ?????nh",fg='green')
            code_output.config(fg='black')
            compile_message = "???? d???ch xong CT, kh??ng x???y ra l???i\n"+str(output.decode('utf-8'))
        code_output.delete("1.0",END)
        code_output.insert("1.0",compile_message)
    else:
        code_output.delete("1.0",END)
        code_output.insert("1.0","Ch??a l??u file, kh??ng th??? d???ch!")
def run_file():
    if file_path == '':
        if save_file_notice():
            pass
    run_path = file_path.replace('/','\\\\')
    run_path = run_path.replace('.pas','')
    os.system(run_path)

def about():
    about_window = Toplevel()
    text1= Label(about_window,text='Made 100% by HN! :)')
    text1.pack()

def github():
    github_window = Toplevel()
    link = Label(github_window,text='Link: https://github.com/ImNoobb/Pascal-Compiler')
    link.pack()

def save_file_notice():
    result = mb.askyesnocancel("Khoan ????","C?? l??u file hi???n t???i?")
    if result:
        save_file(1)
    elif result == False:
        pass
    else:
        return True

def back_ground(event):
    widget = window.focus_get()
    if '.!frame.!text'in str(widget):
        pos = editor.index(INSERT)
        if event.char == '(':
            editor.insert(pos,')')
            editor.mark_set("insert",pos)
        elif event.char == '[':
            editor.insert(pos,']')
            editor.mark_set("insert",pos)
        elif event.char == '{':
            editor.insert(pos,'}')
            editor.mark_set("insert",pos)
        elif event.char == '"':
            editor.insert(pos,'"')
            editor.mark_set("insert",pos)
        elif event.char == "'":
            editor.insert(pos,"'")
            editor.mark_set("insert",pos)


# Setup window #
window = Tk()
window.title('HN - PascalEditor')
window.resizable(False, False)

run_img = ImageTk.PhotoImage(Image.open("run_program.png"))
compile_img = ImageTk.PhotoImage(Image.open("compile.png"))

# ====================== Menu bar ====================== #
menu_bar = Menu(window)
# File menu #
file_menu = Menu(menu_bar,tearoff=0)
file_menu.add_command(label='M???i', command=new_file)
file_menu.add_command(label='M???', command=open_file)
file_menu.add_command(label='L??u', command=save_file)
file_menu.add_command(label='L??u ???', command=save_as_file)
file_menu.add_command(label='Tho??t', command=quit_)

menu_bar.add_cascade(label='T???p', menu=file_menu)
# Run menu #
run_menu = Menu(menu_bar,tearoff=0)
run_menu.add_command(label='D???ch ch????ng tr??nh', command=compile_file)
run_menu.add_command(label='Ch???y ch????ng tr??nh', command=run_file)

menu_bar.add_cascade(label='Ch???y',menu=run_menu)
# Info menu #
info_menu = Menu(menu_bar,tearoff=0)
info_menu.add_command(label='V??? ???ng d???ng', command=about)
info_menu.add_command(label='Source code (GitHub)', command=github)

menu_bar.add_cascade(label='Th??ng tin', menu=info_menu)

window.config(menu=menu_bar)
# ====================================================== #
file_path_text = Label(text='\t\t\t\t\tMade by HN\t\t\t\t\t\t\t\t')
file_path_text.pack()
# Main Frame ========================= #
main_frame = Frame(window)
main_frame.pack()
# Scroll bar #
text_scroll = Scrollbar(main_frame)
text_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(main_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)
# Editor Area #
editor = Text(main_frame,undo=True,wrap="none",yscrollcommand=text_scroll.set,xscrollcommand=hor_scroll.set)
editor.pack()
# ==================================== #

# Compile Frame ====================== #
comp_frame = Frame(window)
comp_frame.pack()
# Buttons #
run_btn = Button(comp_frame,text='RUN',command=run_file,image=run_img,bd=0)
run_btn.grid(row=0,column=0)

compile_btn = Button(comp_frame,text='COMPILE',command=compile_file,image=compile_img,bd=0)
compile_btn.grid(row=0,column=1)
# Notice text #
notice_text = Label(comp_frame,text='*L??u ??: H??y d???ch tr?????c khi ch???y CT, khi d???ch ch????ng tr??nh th?? s??? t??? l??u')
notice_text.grid(row=0,column=2)
# ==================================== #

# Compile Output text ================ #
# Output #
code_output = Text(height=7,bg="light cyan")
code_output.pack()
# Status #
status_text = Label(text="Tr???ng th??i: ???n ?????nh",fg='green')
status_text.pack(side=RIGHT)
# ==================================== #
# Key binds ==== #
window.bind('<Control-Key-s>', save_file)
window.bind("<Key>",back_ground)


window.mainloop()
