import re
import win32com.client
from aip import AipOcr
from tkinter import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
import time

# file_path=""

def get_json(file_path):
    """ APPID AK SK """
    APP_ID = '18101358'
    API_KEY = 'x0X7o4N6qZFdNOZPg1fyFqWY'
    SECRET_KEY = 'j5zHwikOh6mvK0h1dVONYI3sUbVA3QYG'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    invoice_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
    i = open(file_path, 'rb')
    img = i.read()
    message = client.basicGeneral(img)
    words = []
    for i in message.get('words_result'):
        words.append(i.get('words'))
    print(words[0])
    return words[0]

#计算器计算#
def zhengli(func):
    func = func.replace("+-","-").replace("--","+")
    return func
def addjian(func):
    func = func.strip("()")
    ret = re.findall("-?\d*\.?\d+",func)
    sum=0
    for i in ret:
        sum +=float(i)
    return str(sum)
def chengchu(func):
    func = func.strip("()")
    while("/"in func or "*" in func):
        ret = re.search('\d*\.?\d+[\*/]-?\d*\.?\d',func).group()
        digital = re.split('([\*/])',ret)         #加个括号是为了优先级的原因，保留非数字
        result = str(float(digital[0])*float(digital[2])) if digital[1] == '*' else str(float(digital[0])/float(digital[2]))
        func = func.replace(ret,result,1)
        func = zhengli(func)
        # func = float(func)
    return func

def comput(formal):
    formal = re.sub('\s','',formal)
    while(re.search('\([^()]*\)',formal)):
        print(formal)
        ret = re.findall('\([^()]*\)',formal)
        for i in ret:
            print("wu kuohao:"+i)
            result_chengchu = chengchu(i) if '*'in i or '/' in i else i#先算乘除
            result_addjian = addjian(result_chengchu) if '+'in result_chengchu or '-' in result_chengchu else result_chengchu#再算加减
            formal = formal.replace(i,result_addjian,1)
            formal = zhengli(formal)
    else:
        result_chengchu = chengchu(formal) if '*' in formal or '/' in formal else formal  # 先算乘除
        result_addjian = addjian(result_chengchu) if '+' in result_chengchu or '-' in result_chengchu else result_chengchu  # 再算加减
        return result_addjian

def fill_text():
    text = kb_input.get()
    result =comput(text)
    label_res1.config(text=">>>>>>"+text+"="+result+"<<<<<<", font=('Arial', 12))
    print(result)
    sp = win32com.client.Dispatch('SAPI.SpVoice')  # 创建播报器对象
    sp.Speak("result is"+result)  # 进行播报

def choose_picture():
    kb_input.delete(0, END)
    file_path = askopenfilename(title='Select the diagnostic instrument',
                                # filetypes=[('png', '*.png'), ('jpg', '*.jpg'),(4'All Files', '*')],
                                initialdir='.')
    window.pilImage = Image.open(file_path)
    window.tkImage = ImageTk.PhotoImage(image=window.pilImage)
    window.label.config(image=window.tkImage)
    pic_cal.config(state=ACTIVE,command=lambda :pic_calcu(file_path))

def pic_calcu(file_path):
    # 调用aip与计算器函数
    formul = get_json(file_path)
    result = comput(formul)
    #显示答案
    label_res1.config(text=">>>>>>" + formul + "=" + result + "<<<<<<", font=('Arial', 12))
    #答案语音播报
    sp = win32com.client.Dispatch('SAPI.SpVoice')  # 创建播报器对象
    sp.Speak("result is"+result)  # 进行播报



file_path = ""
window = Tk()
window.wm_title("calculator")
window.geometry("700x300")
i=0
l = Label(window, text='hello! this is a calculator', font=('Arial', 15), width=30, height=2)
l.pack()
window.config(background="#f4efef")

fm1 = Frame(window)  # 该容器放在左边排列
fm1.pack(side=LEFT, fill=BOTH, expand=YES)
fm2 = Frame(window, height=10, width=60)
fm2.pack(side=LEFT, fill=NONE, expand=False)
fm3 = Frame(window, height=30, width=30)  # 该容器放在左边排列
fm3.pack(side=RIGHT, fill=NONE, expand=False, padx=30, pady=0)
fm4 = Frame(fm3, height=30, width=30)  # 该容器放在左边排列
fm4.pack(side=BOTTOM, fill=NONE, expand=False, pady=45)

# 设置按钮从顶部开始排列，且按钮只能在垂直（X）方向填充
label_text = Label(fm1, text='text input', font=('Arial', 12), width=10, height=2)
label_text.pack(side=TOP, fill=X, expand=YES)
label_pic = Label(fm1, text='image recognition', font=('Arial', 12), width=15, height=6)
label_pic.pack(side=TOP, fill=X, expand=YES)
label_res = Label(fm1, text='calculation', font=('Arial', 12), width=10, height=3)
label_res.pack(side=TOP, fill=X, expand=YES)



# 键盘输入
kb_input = Entry(fm2, show=None, justify=LEFT, font=('Arial', 10), width=33)  # w文字输入
kb_input.pack(padx=2, pady=15, side=TOP)
window.pilImage = Image.open(".\\background.JPG")
window.tkImage = ImageTk.PhotoImage(image=window.pilImage)
window.label = Label(fm2, image=window.tkImage, width=300, height=130)  # 图片
window.label.pack(padx=2, pady=5, side=TOP)
label_res1 = Label(fm2, text=' ', width=33, height=1)  # result
label_res1.pack(padx=2, pady=5, side=TOP)
text_cal = Button(fm3, text='calculate', font=('Arial', 10), width=11, height=1, command=fill_text)
text_cal.pack(side=TOP, pady=0)
# 图片识别
pic_input = Button(fm4, text='input picture', font=('Arial', 10), width=11, height=1, command=choose_picture)
pic_input.pack(side=TOP)
pic_cal = Button(fm4, text='calculate', font=('Arial', 10), state=DISABLED, width=11, height=1, command=pic_calcu)
pic_cal.pack(side=BOTTOM, pady=10)
window.mainloop()




