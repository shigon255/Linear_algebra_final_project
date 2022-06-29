import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

def sigma_rate(sigma):
    total = sum(sigma)
    x = []
    y = []
    count = 0
    for i in range(sigma.size):
        count = count + sigma[i]
        y.append(count / total)
        x.append(i + 1)
    plt.xlabel('Number of selected singular values')
    plt.ylabel('sum of selected singular values/sum of all singular values')
    plt.plot(x, y)
    plt.show()

def rebuild_img(u, sigma, v, rate):
    m = len(u)
    n = len(v)
    arr = np.zeros((m, n))
    cur = 0
    index = 0
    max_sigma = sum(sigma)*rate
    while True:
        if cur + sigma[index] >= max_sigma:
            arr += (max_sigma-cur)*np.dot(u[:, index].reshape(m,1),v[index].reshape(1,n))
            print('index:'+str(rate*10))
            print(index)
            break
        arr += sigma[index] * np.dot(u[:, index].reshape(m, 1), v[index].reshape(1, n))
        cur+=sigma[index]
        index = index+1
    arr[arr < 0] = 0
    arr[arr > 255] = 255
    return np.rint(arr).astype(int)
def compress(filename,rate):
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

def rebuild_100(u, sigma, v,):
    images = []
    singular_num = []
    m = len(u)
    n = len(v)
    arr = np.zeros((m, n))
    cur = 0
    index = 0
    for i in range(1,100):
        print(i)
        while cur <= sum(sigma)*i/100:
            arr += sigma[index] * np.dot(u[:, index].reshape(m, 1), v[index].reshape(1, n))
            cur += sigma[index]
            index = index + 1
        tarr = arr
        tarr[tarr < 0] = 0
        tarr[tarr > 255] = 255
        images.append(np.rint(tarr).astype(int))
        singular_num.append(index)
    return images, singular_num



def main1():
    filename = 'flower.jpg'
    img = Image.open(filename)
    a = np.array(img)
    u, sigma, v = np.linalg.svd(a[:, :, 0])
    sigma_rate(sigma)

def main2():
    filesize = []
    index = []
    total = os.stat('test.jpg').st_size
    filename = 'test.jpg'
    for i in range(1,10):
        result_image = compress(filename,i/10)
        result_image.save('result'+str(i)+'.jpg')
        index.append(i/10)
        print(os.stat('result'+str(i)+'.jpg').st_size)
        filesize.append(os.stat('result'+str(i)+'.jpg').st_size/total)
        print(i)
    index.append(1.0)
    filesize.append(1)
    print(index)
    print(filesize)
    plt.xlabel('Rate of sum of singular values')
    plt.ylabel('File size')
    plt.legend()
    plt.plot(index, filesize)
    plt.show()

def main3():
    filesize_rate = []
    singular_sum_rate = []
    singular_nums = []
    images = []
    total = os.stat('flower.jpg').st_size
    filename = 'flower.jpg'
    image_file = Image.open(filename)
    arr = np.array(image_file)
    # Do SVD to R, G, and B respectively
    u, sigma, v = np.linalg.svd(arr[:, :, 0])
    image, singular_num = rebuild_100(u, sigma, v)
    images.append(image)
    singular_nums.append(singular_num)

    u, sigma, v = np.linalg.svd(arr[:, :, 1])
    image, singular_num = rebuild_100(u, sigma, v)
    images.append(image)
    singular_nums.append(singular_num)

    u, sigma, v = np.linalg.svd(arr[:, :, 2])
    image, singular_num = rebuild_100(u, sigma, v)
    images.append(image)
    singular_nums.append(singular_num)
    for i in range(1,100):
        print(i)
        result_image = Image.fromarray(np.uint8(np.stack((images[0][i-1], images[1][i-1], images[2][i-1]), 2)))
        result_image.save('result' + str(i) + '.jpg')
        singular_sum_rate.append(i / 100)
        filesize_rate.append(os.stat('result' + str(i) + '.jpg').st_size / total)
    plt.xlabel('Rate of sum of singular values')
    plt.ylabel('Rate of file size')
    plt.legend()
    plt.plot(singular_sum_rate, filesize_rate)
    plt.show()


if __name__ == '__main__':
    main1() #sigma rate
    #main2() #compress 10 image then compare size
    #main3() #100 images
