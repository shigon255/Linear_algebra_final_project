import numpy as np
from PIL import Image
from fpdf import FPDF
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import shutil
import os


class PDF(FPDF):
    def put_image(self,filename):
        self.image(filename, 30, 30, pdf_w-60, pdf_h-60)

def rebuild_img(u, sigma, v, rate):
    m = len(u)
    n = len(v)
    arr = np.zeros((m, n))
    cur = 0
    index = 0
    max_sigma = sum(sigma) * rate
    while True:
        if cur + sigma[index] >= max_sigma:
            arr += (max_sigma - cur) * np.dot(u[:, index].reshape(m, 1), v[index].reshape(1, n))
            break
        arr += sigma[index] * np.dot(u[:, index].reshape(m, 1), v[index].reshape(1, n))
        cur += sigma[index]
        index = index + 1
    arr[arr < 0] = 0
    arr[arr > 255] = 255
    return np.rint(arr).astype(int)

def compress(filename):
    rate = 0.9
    image_file = Image.open(filename)
    arr = np.array(image_file)
    # Do SVD to R, G, and B respectively
    u, sigma, v = np.linalg.svd(arr[:, :, 0])
    R = rebuild_img(u, sigma, v, rate)
    u, sigma, v = np.linalg.svd(arr[:, :, 1])
    G = rebuild_img(u, sigma, v, rate)
    u, sigma, v = np.linalg.svd(arr[:, :, 2])
    B = rebuild_img(u, sigma, v, rate)
    result = np.stack((R, G, B), 2)
    return Image.fromarray(np.uint8(result))



def choose_file_event():
    global file_paths
    file_paths = filedialog.askopenfilenames(filetypes=[('image files', ('.png', 'jpg', 'jpeg'))])

def choose_des_event():
    global des_path
    des_path = filedialog.askdirectory()

def execute_event():
    pdf = PDF(orientation='L', unit='mm', format='A4')
    try:
        for i in range(len(file_paths)):
            img = compress(file_paths[i])
            img.save('tmp' + str(i + 1) + '.jpg')
            pdf.add_page()
            pdf.put_image('tmp' + str(i + 1) + '.jpg')
            os.remove('tmp' + str(i + 1) + '.jpg')
        pdf.output(entryString.get()+'.pdf', 'F')
        shutil.move(os.path.abspath(entryString.get()+'.pdf'),des_path)
        del pdf
    except NameError:
        tkinter.messagebox.showinfo('錯誤', '資料未輸入完全')


pdf_w = 297
pdf_h = 210



#root window setting
root = tk.Tk()
root.title('圖片壓縮與PDF檔案產生器')
root.geometry('250x150')

lbl_1 = tk.Label(root, text='PDF檔案名稱', fg='#263238', font=('Arial', 12))
lbl_1.grid(row=0,column=0)

entryString = tk.StringVar()
entryString.set("compressed")
entry1 = tk.Entry(root, width=20, textvariable=entryString)
entry1.grid(row=0,column=1)

lbl_2 = tk.Label(root, text='請選擇檔案', fg='#263238', font=('Arial', 12))
lbl_2.grid(row=1,column=0)

button1 = tk.Button(root, text='選擇', command=choose_file_event)
button1.grid(row=1,column=1)

lbl_3 = tk.Label(root, text='請選擇儲存位置', fg='#263238', font=('Arial', 12))
lbl_3.grid(row=2,column=0)

button2 = tk.Button(root, text='選擇', command=choose_des_event)
button2.grid(row=2,column=1)

button3 = tk.Button(root, text='確定', command=execute_event)
button3.grid(row=3,column=0)

root.mainloop()