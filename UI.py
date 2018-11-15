#############################################
# 用户界面
#############################################


############################## 引入库函数
from tkinter import *
import tkinter as tk
import os


class Hello():
    def __init__(self, root):
        '''Init Form'''
        self.root = root
        self.frameTop()
        self.frameBottom()


    def frameBottom(self):
        """Create Bottom Frame"""
        self.bottom = tk.LabelFrame(self.root)
        self.bottom.grid(row=1, column=0, padx=20, pady=3)
        self.bottom_entry_var_0 = StringVar()
        self.bottom_entry_0 = tk.Entry(self.bottom, textvariable=self.bottom_entry_var_0)
        self.bottom_entry_0.grid(row=0, column=1, padx=20, pady=3)
        self.bottom_entry_var_1 = StringVar()
        self.bottom_entry_1 = tk.Entry(self.bottom, textvariable=self.bottom_entry_var_1, show='*')
        self.bottom_entry_1.grid(row=1, column=1, padx=20, pady=3)
        self.bottom_cbtn_int_0 = IntVar()
        self.bottom_cbtn_0 = tk.Checkbutton(self.bottom, variable=self.bottom_cbtn_int_0, text='记住密码', font=('宋体', 10))
        self.bottom_cbtn_0.grid(row=2, column=1, padx=20, pady=3, sticky='w')
        #self.bottom_btn_0 = tk.Button(self.bottom, text='登陆', relief=RIDGE, bd=4, width=10 \
                                    #  , font=('宋体', 12), command=self.print_nima)
        self.bottom_btn_0.grid(row=3, column=1, padx=20, pady=3)

    '''
    def print_nima(self):
        """btn callback"""
        print(self.bottom_entry_var_0.get())
        print(self.bottom_entry_var_1.get())
        print(self.bottom_cbtn_int_0.get())
    '''

'''
def fun_fuck():
    if __name__ == '__main__':
        """main loop"""
        root2 = tk.Tk()
        root2.title('=。=')
        Hello(root2)
        root2.mainloop()
'''

class Cycle():
    def __init__(self, root):
        """Init Form"""
        self.root = root
        self.frameTop()


    def frameTop(self):
        """top frame"""
        btn_toplevel = tk.Button(self.root, text='选择爬取/分析', command=self.toplevel_click)
        btn_toplevel.grid(row=0, column=0, padx=40, pady=30, sticky='wesn')


    def toplevel_click(self):
        """toplevel click"""
        func_list = ['Spider1', 'Spider2', 'Spider3', 'Analisys']
        self.frm_toplevel = tk.Toplevel(self.root)
        self.frm_toplevel.title('选择内容')
        for (count, func_name) in enumerate(func_list):
            btn = tk.Button(self.frm_toplevel, width=25, text=func_name)
            btn.grid(row=count // 2, column=2 * (count % 2), padx=5, pady=5)
            btn.bind('<Button-1>', self.hhhh)


    def hhhh(self, event):
        fff = event.widget['text']
        if fff == 'Spider1':
            # 打开.py
            os.system('Spider2.py')

        if fff == 'Spider2':
            os.system('Spider1.py')
            '''
            if askquestion('保存','是否保存',parent=self.frm_toplevel) == 'yes':
                saveasfile = asksaveasfilename()
            else:
                try:showerror('error!','show error!',parent=self.frm_toplevel)
                except:pass
            '''

        if fff == 'Spider3':
            # 打开.py
            os.system('Spider3.py')
        '''
            fun_fuck()
        self.frm_toplevel.destroy()
        '''

        if fff == 'Jieba':
            # 打开.py
            os.system('Analisys.py')


if __name__ == '__main__':
    '''main loop '''
    root = tk.Tk()
    root.title('欢迎使用！')
    # photo = PhotoImage(file='pig.jpg')
    Cycle(root)
    root.mainloop()

