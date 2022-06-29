import numpy as np
from PIL import Image
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog
import shutil
import os




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
    rate = 0.7
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
    try:
        for i in range(len(file_paths)):
            img = compress(file_paths[i])
            img.save('compressed' + str(i + 1) + '.jpg')
            shutil.move(os.path.abspath('compressed' + str(i + 1) + '.jpg'),des_path)
    except NameError:
        tkinter.messagebox.showinfo('錯誤', '資料未輸入完全')



#root window setting
root = tk.Tk()
root.title('圖片壓縮器')
root.geometry('250x150')

lbl_1 = tk.Label(root, text='請選擇檔案', fg='#263238', font=('Arial', 12))
lbl_1.grid(row=0,column=0)

button1 = tk.Button(root, text='選擇', command=choose_file_event)
button1.grid(row=0,column=1)

lbl_2 = tk.Label(root, text='請選擇儲存位置', fg='#263238', font=('Arial', 12))
lbl_2.grid(row=1,column=0)

button2 = tk.Button(root, text='選擇', command=choose_des_event)
button2.grid(row=1,column=1)

button3 = tk.Button(root, text='確定', command=execute_event)
button3.grid(row=2,column=0)

root.mainloop()