from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess,os
from PIL import ImageTk, Image

compiler = Tk()
compiler.title('HN IDE')
file_path = ''
run_file = False
run_path=''
run_img = ImageTk.PhotoImage(Image.open("run_program.png"))
compile_img = ImageTk.PhotoImage(Image.open("compile.png"))

def set_file_path(path):
    global file_path
    file_path = path

def open_file():
    path = askopenfilename(filetypes=[('Pascal Files', '*.pas')])
    if path:
        with open(path,'r') as file:
            code = file.read()
            editor.delete('1.0',END)
            editor.insert('1.0',code)
            set_file_path(path)
    set_file_path(path)

def save():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Pascal Files', '*.pas')])
        if not '.pas' in path:
            path += '.pas'
    else:
        path = file_path
    if path:
        with open(path, 'w') as file:
            code = editor.get('1.0',END)
            file.write(code)
            set_file_path(path)
        return True
        set_file_path(path)
    else:
        return False

def save_as():
    path = asksaveasfilename(filetypes=[('Pascal Files', '*.pas')])
    if path:
        with open(path, 'w') as file:
            code = editor.get('1.0',END)
            file.write(code)
            set_file_path(path)

def exit():
    compiler.destroy

def run():
    global run_file,run_path
    if file_path == '':
        save_promt = Toplevel()
        text = Label(save_promt,text='Hãy lưu File trước khi chạy')
        text.pack()
        return
    run_path = file_path.replace('/','\\\\')
    run_path = run_path.replace('.pas','')
    os.system(run_path)

def compile_file():
    compile_message = ''
    if save():
        compile_path = file_path.replace('\\','\\\\')
        command = f'fpc {compile_path}'
        process = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output,error = process.communicate()
    
        with open("output.txt",'w') as f:
            f.write(output.decode("utf-8"))
        i = open_txt()
        for l in range(6,len(i)):
            compile_message += i[l]
        
        if 'Error:' in str(output):
            notice_text.config(text="Trạng thái: Lỗi    ",fg='red')
            code_output.config(height=7,fg='red')
            compile_message = "Đã xảy ra lỗi!\n"+compile_message
        else:
            notice_text.config(text="Trạng thái: Ổn định",fg='green')
            code_output.config(height=7,fg='black')
            compile_message = "Đã dịch xong CT, không xảy ra lỗi\n"+compile_message

        code_output.delete('1.0',END)
        code_output.insert('1.0',compile_message)
    else:
        code_output.delete('1.0',END)
        code_output.insert('1.0',"Chua luu file, khong the chay!")

def about():
    thong_tin = Toplevel()
    text = Label(thong_tin,text="Phần mềm này được tạo bởi Hoàng Nguyên - NTPL")
    text.pack()
    text2 = Label(thong_tin,text="Với mục đích hỗ trợ gõ chương trình Pascal")
    text2.pack()
    text3 = Label(thong_tin,text="như chạy và dịch chương trình. Với giao diện")
    text3.pack()
    text4 = Label(thong_tin,text="khá ổn và dễ nhìn. Mong bạn thích nó :D")
    text4.pack()

def github():
    pass

def open_txt():
    with open("output.txt", 'r') as f:
        i = f.readlines()
    return i

def back_ground(e):
    pos = editor.index(INSERT)
    if e.char == '(':
        pos = editor.index(INSERT)
        editor.insert(pos,')')
        editor.mark_set("insert", pos)
    elif e.char == '"':
        pos = editor.index(INSERT)
        editor.insert(pos,'"')
        editor.mark_set("insert", pos)
    elif e.char == "'":
        pos = editor.index(INSERT)
        editor.insert(pos,"'")
        editor.mark_set("insert", pos)
    elif e.char == "[":
        pos = editor.index(INSERT)
        editor.insert(pos,"]")
        editor.mark_set("insert", pos)
    elif e.char == "{":
        pos = editor.index(INSERT)
        editor.insert(pos,"}")
        editor.mark_set("insert", pos)

def new_file():
    global file_path
    editor.delete("1.0",END)
    file_path = ''


menu_bar = Menu(compiler)

first_text = Label(text="\tMade by HN\t\t\t\t\t\t\t\t\t\t\t\t")
first_text.pack()

# File menu =============================== #
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Moi', command=new_file)
file_menu.add_command(label='Mở', command=open_file)
file_menu.add_command(label='Lưu', command=save)
file_menu.add_command(label='Lưu ở', command=save_as)
file_menu.add_command(label='Thoát', command=compiler.destroy)
menu_bar.add_cascade(label='Tệp', menu=file_menu)

# Run menu ================================ #
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Chạy...', command=run)
run_bar.add_command(label='Dịch...', command=compile_file)
menu_bar.add_cascade(label='Chạy', menu=run_bar)

info_bar = Menu(menu_bar, tearoff=0)
info_bar.add_command(label='Về ứng dụng', command=about)
info_bar.add_command(label='GitHub', command=github)
menu_bar.add_cascade(label='Thông tin', menu=info_bar)

compiler.config(menu=menu_bar)
# Main Frame ============================== #
my_frame = Frame(compiler)
my_frame.pack()

text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

editor = Text(my_frame,undo=True,wrap="none",yscrollcommand=text_scroll.set,xscrollcommand=hor_scroll.set)
editor.pack()

# ========================================== # 
another_frame = Frame(compiler)
another_frame.pack()

run_btn = Button(another_frame,image=run_img,text='Chạy chương trình',bd=1,width=111,command=run,border=0)
run_btn.grid(row=0,column=0)

compile_btn = Button(another_frame,image=compile_img,text='Dịch chương trình',bd=1,width=111,command=compile_file,border=0)
compile_btn.grid(row=0,column=1)

notice_text = Label(another_frame,text="\t*Lưu ý: Dịch chương trình trước khi chạy, không có thể xảy ra lỗi")
notice_text.grid(row = 0,column=2)

# =========================================== #

code_output = Text(height=7)
code_output.pack()

compiler.resizable(False, False)

notice_text = Label(text="Trạng thái: Ổn định",fg='green')
notice_text.pack(side=RIGHT)

# Key binds ================================== #
compiler.bind("<Key>",back_ground)

compiler.mainloop()
