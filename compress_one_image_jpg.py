import numpy as np
from PIL import Image
import os

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
            break
        arr += sigma[index] * np.dot(u[:, index].reshape(m, 1), v[index].reshape(1, n))
        cur+=sigma[index]
        index = index+1
    arr[arr < 0] = 0
    arr[arr > 255] = 255
    return np.rint(arr).astype(int)

def compress(filename):
    rate = 1
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

filename = 'original.jpg'
result_image = compress(filename)
result_image.save('result.jpg')
print(os.stat('result.jpg').st_size)
