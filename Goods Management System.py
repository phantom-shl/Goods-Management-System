import tkinter as tk
import tkinter.ttk as ttk

scrw = 0
scrh = 0
word = ""
s=['名称', '编号', '销量', '价格', '类型', '销量占总量的百分比']

# 定义类存储书本信息
class Good:
    def __init__(self, name, id, num, price, ty):
        # 物品 名称 编号 销量 价格 类型
        self.name = name
        self.id = id
        self.num = num
        self.price = price
        self.ty = ty

goods = []

def message(data):
    global scrw, scrh
    info = tk.Tk()
    winw = 150  # 窗口宽度
    winh = 100  # 窗口高度
    scrw = info.winfo_screenwidth()  # 屏幕宽度
    scrh = info.winfo_screenheight()  # 屏幕高度
    x = (scrw - winw) / 2  # 水平位置
    y = (scrh - winh) / 2  # 垂直位置
    info.geometry('%dx%d+%d+%d' % (winw, winh, x, y))  # 设置窗口大小和位置
    tk.Label(info, text=data, font=("微软雅黑", 15)).pack(pady=25)
    info.after(700, info.quit)
    info.after(700, info.destroy)
    info.mainloop()

def Begin():
    try:  # 读入先前存储的物品信息
        with open("goods.txt", "r", encoding='utf-8') as f:  # utf-8是常用的中文文件编码方式,防止读取文件中存在中文报错
            lines = f.readlines()  # 按行读入
            lines = [line.strip() for line in lines]  # 去除换行符
            for i in range(len(lines)):
                temp = lines[i].split()
                if not temp: continue
                goods.append(Good(temp[0], int(temp[1]), int(temp[2]), int(temp[3]), temp[4]))  # 存储信息
            f.close()
    except FileNotFoundError:  # 若没有先前存储的信息,新建一个文档以存储
        with open("goods.txt", "w", encoding='utf-8') as f:
            f.write("")
            f.close()
    message("初始化已完成")

def End():
    file = open("goods.txt", "w", encoding='utf-8')
    for i in goods:
        temp = i.name + ' ' + str(i.id) + ' ' + str(i.num) + ' ' + str(i.price) + ' ' + i.ty
        file.write(temp + '\n')
    file.close()

def Add_t(n, i, m, p, ty):
    global goods
    goods.append(Good(n.get(), i.get(), m.get(), p.get(), ty.get()))
    message("添加完成")
    n.delete(0, tk.END)
    i.delete(0, tk.END)
    m.delete(0, tk.END)
    p.delete(0, tk.END)
    ty.delete(0, tk.END)

def Add():
    add_t = tk.Tk()
    winw = 220
    winh = 240
    add_t.geometry('%dx%d+%d+%d' % (winw, winh, (scrw - winw) / 2, (scrh - winh) / 2))
    tk.Label(add_t, text="请输入物品信息").grid(row=0, column=0, columnspan=2)
    text = ["名称:", "编号:", "销量:", "价格:", "类型:"]
    for i in range(0, 5):
        tk.Label(add_t, text=text[i]).grid(row=i + 1, column=0, padx=5)
    name_data = tk.Entry(add_t)
    id_data = tk.Entry(add_t)
    num_data = tk.Entry(add_t)
    price_data = tk.Entry(add_t)
    ty_data = tk.Entry(add_t)
    name_data.grid(row=1, column=1)
    id_data.grid(row=2, column=1)
    num_data.grid(row=3, column=1)
    price_data.grid(row=4, column=1)
    ty_data.grid(row=5, column=1)
    id_data.insert(tk.END, goods[len(goods)-1].id+1)
    tk.Button(add_t, text="完成", command=lambda: Add_t(num_data, id_data, name_data, price_data, ty_data)).grid(
        row=6, columnspan=2)
    tk.Button(add_t, text="退出", command=lambda: (add_t.destroy(), add_t.quit())).grid(row=7, columnspan=2)
    tk.Label(add_t, text="tips:填写完毕后点击'完成'再点击退出").grid(row=8, columnspan=2)
    add_t.mainloop()

def Output_window(data):
    data_list = tk.Tk()
    data_list.title('list')
    scrollbar = tk.Scrollbar(data_list, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    # 表格
    l = ttk.Treeview(data_list, yscrollcommand=scrollbar.set)
    l['columns'] = ('名称', '编号', '销量', '价格', '类型', '销量占总量的百分比')
    # 设置列和表头
    l.column('#0', width=50, anchor='center')
    for i in range(0, len(s)):
        l.column(s[i], anchor='center')
        l.heading(s[i], text=s[i], anchor='center')
    goods_sum = 0
    for i in goods:
        goods_sum += int(i.num)
    # 添加数据
    for i in range(len(data)):
        l.insert('', 'end', text=str(i + 1),
                 values=(data[i].name, str(data[i].id), str(data[i].num),
                         str(data[i].price), data[i].ty, str(round((int(data[i].num) / goods_sum) * 100, 2)) + '%'))
    l.pack()
    scrollbar.config(command=l.yview)
    data_list.mainloop()

def output_sort(f, data):
    if f==1: data=sorted(data, key=lambda x: x.num, reverse=True)
    elif f==2: data=sorted(data, key=lambda x: x.price)
    Output_window(data)

def Output(data):  # 数据数组
    temp=tk.Tk()
    tk.Button(temp, text="按编号排序", command=lambda: Output_window(data)).grid(row=0, column=0)
    tk.Button(temp, text="按销量排序", command=lambda: output_sort(1, data)).grid(row=0, column=1)
    tk.Button(temp, text="按价格排序", command=lambda: output_sort(2, data)).grid(row=1, column=0, columnspan=2)
    tk.Button(temp, text="退出", command=lambda: (temp.destroy(), temp.quit)).grid(row=2, columnspan=2)


def Find_t(temp,data):
    global word
    word=data.get()
    temp.quit()
    temp.destroy()

def Find(k):
    global word
    word=""
    data_list=[]
    temp=tk.Tk()
    temp.title("请输入信息")
    winw = 225
    winh = 65
    temp.geometry('%dx%d+%d+%d' % (winw, winh, (scrw - winw) / 2, (scrh - winh) / 2))
    tk.Label(temp, text="请输入信息").grid(row=0, column=0, padx=5, pady=5)
    data=tk.Entry(temp)
    data.grid(row=0, column=1)
    tk.Button(temp, text="完成", command=lambda: Find_t(temp, data)).grid(row=2, columnspan=2)
    temp.mainloop()
    for i in goods:
        if k == 1 and word == i.name:
            data_list.append(Good(i.name, int(i.id), int(i.num), int(i.price), i.ty))
        elif k == 2 and word == i.id:
            data_list.append(Good(i.name, int(i.id), int(i.num), int(i.price), i.ty))
        elif k == 3 and word == i.num:
            data_list.append(Good(i.name, int(i.id), int(i.num), int(i.price), i.ty))
        elif k == 4 and word == i.price:
            data_list.append(Good(i.name, int(i.id), int(i.num), int(i.price), i.ty))
        elif k == 5 and word == i.ty:
            data_list.append(Good(i.name, int(i.id), int(i.num), int(i.price), i.ty))
    if word != "":
        if not data_list:
            message("无查询结果")
        else:
            Output_window(data_list)
    return None

def Find_window():
    find=tk.Tk()
    winw = 150
    winh = 125
    find.geometry('%dx%d+%d+%d' % (winw, winh, (scrw - winw) / 2, (scrh - winh) / 2))
    tk.Button(find, text="按名称查询", command=lambda: Find(1)).grid(row=0, column=0,padx=2.5)
    tk.Button(find, text="按编号查询", command=lambda: Find(2)).grid(row=0, column=1)
    tk.Button(find, text="按销量查询", command=lambda: Find(3)).grid(row=1, column=0)
    tk.Button(find, text="按价格查询", command=lambda: Find(4)).grid(row=1, column=1)
    tk.Button(find, text="按类型查询", command=lambda: Find(5)).grid(row=2, column=0, columnspan=2)
    tk.Button(find, text="退出", command=lambda: (find.quit(), find.destroy())).grid(row=3, column=0, columnspan=2)
    find.mainloop()


def Check():  # 查看物品剩余销量
    data_list = tk.Tk()
    data_list.title('list')
    scrollbar = tk.Scrollbar(data_list, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    # 表格
    l = ttk.Treeview(data_list, yscrollcommand=scrollbar.set)
    l['columns'] = ('名称', '销量')
    # 设置列
    l.column('#0', width=40, anchor='center')
    l.column('名称', anchor='center')
    l.column('销量', anchor='center')
    # 设置表头
    l.heading('名称', text='名称', anchor='center')
    l.heading('销量', text='销量', anchor='center')
    # 添加数据
    for i in range(len(goods)):
        l.insert('', 'end', text=str(i + 1), values=(goods[i].name, goods[i].num))
    l.pack()
    scrollbar.config(command=l.yview)
    data_list.mainloop()

def Change():
    list_window = tk.Tk()
    list_window.title("列表")
    winw = 200
    winh = 240
    list_window.geometry('%dx%d+%d+%d' % (winw, winh, (scrw - winw) / 2, (scrh - winh) / 2))
    listbox = tk.Listbox(list_window)
    title_label = tk.Label(list_window, text="请选择要更改的物品", font=("微软雅黑", 10))
    title_label.pack(pady=(10, 5))
    scrollbar = tk.Scrollbar(list_window, command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.pack(side="left", expand=True)
    scrollbar.pack(side="right", fill="y")
    # 添加列表项
    for i in range(0, len(goods)):
        temp = goods[i].name
        listbox.insert(tk.END, temp)
    # 绑定
    listbox.bind('<<ListboxSelect>>', lambda event: change_t(listbox))
    list_window.mainloop()

def change_(s, name, id, num, price, ty):
    goods[s].name = name
    goods[s].id = int(id)
    goods[s].num = int(num)
    goods[s].price = int(price)
    goods[s].ty = ty

def change_t(listbox):
    s = listbox.curselection()[0]
    change_t_window = tk.Tk()
    winw = 220
    winh = 240
    change_t_window.geometry('%dx%d+%d+%d' % (winw, winh, (scrw - winw) / 2, (scrh - winh) / 2))
    tk.Label(change_t_window, text="请输入物品信息").grid(row=0, column=0, columnspan=2)
    text = ["名称:", "编号:", "销量:", "价格:", "类型:"]
    for i in range(0, 5):
        tk.Label(change_t_window, text=text[i]).grid(row=i + 1, column=0, padx=5)
    name_data = tk.Entry(change_t_window)
    id_data = tk.Entry(change_t_window)
    num_data = tk.Entry(change_t_window)
    price_data = tk.Entry(change_t_window)
    ty_data = tk.Entry(change_t_window)
    name_data.grid(row=1, column=1)
    id_data.grid(row=2, column=1)
    num_data.grid(row=3, column=1)
    price_data.grid(row=4, column=1)
    ty_data.grid(row=5, column=1)
    name_data.insert(0, goods[s].name)
    id_data.insert(0, goods[s].id)
    num_data.insert(0, goods[s].num)
    price_data.insert(0, goods[s].price)
    ty_data.insert(0, goods[s].ty)
    tk.Button(change_t_window, text="保存",
              command=lambda: change_(s, name_data.get(), id_data.get(), num_data.get(), price_data.get(), ty_data.get()
                                      )).grid(row=6, columnspan=2)
    tk.Button(change_t_window, text="退出",
              command=lambda: (change_t_window.destroy(), change_t_window.quit())).grid(row=7, columnspan=2)
    tk.Label(change_t_window, text="tips:填写完毕后点击'保存'再点击退出").grid(row=8, columnspan=2)
    change_t_window.mainloop()

def window():  # 主窗口
    win = tk.Tk()
    win.title("物品管理系统")
    winw = winh = 285
    win.geometry('%dx%d+%d+%d' % (winw, winh, (scrw - winw) / 2, (scrh - winh) / 2))
    tk.Label(win, text='欢迎来到物品管理系统', font=("微软雅黑", 15)).grid(row=0, column=0, columnspan=2)
    tk.Button(win, text="添加物品信息", font=("微软雅黑", 10), command=Add).grid(row=1, column=0, padx=25)
    tk.Button(win, text="查看物品销量", font=("微软雅黑", 10), command=Check).grid(row=1, column=1, padx=25)
    tk.Button(win, text="查询物品信息", font=("微软雅黑", 10), command=Find_window).grid(row=2, column=0, padx=25)
    tk.Button(win, text="更改物品信息", font=("微软雅黑", 10), command=Change).grid(row=2, column=1, padx=25)
    tk.Button(win, text="排列物品信息", font=("微软雅黑", 10),
              command=lambda: Output(goods)).grid(row=3, column=0, columnspan=2)
    tk.Button(win, text="退出", font=("微软雅黑", 10),
              command=lambda: (win.destroy(), win.quit())).grid(row=4, column=0, columnspan=2)
    win.mainloop()

Begin()
window()
End()
