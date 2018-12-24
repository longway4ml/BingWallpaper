#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
@Author: MALI
@Contact: longway.ml@gmail.com
@File: get_bingImg_table_background.py
@Time: 2018/12/21 14:28
"""
import urllib.request
import requests
import os
import win32con
import win32gui
from PIL import Image, ImageFilter


class BingImage:
    def __init__(self):
        self.bing_url = 'https://area.sinaapp.com/bingImg/'
        current_dir = os.path.abspath(os.path.dirname(__file__))
        self.save_dir_img = os.path.join(current_dir, 'bingImg')
        print(current_dir)

    def save_img(self, img_url, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        basename = os.path.basename(img_url)
        filename = os.path.join(dir_path, basename)
        if os.path.exists(filename):
            print('{} existed'.format(filename))
            return filename
        try:
            urllib.request.urlretrieve(img_url, filename)
        except IOError as e:
            print('Failed to save the file', e)
        except Exception as e:
            print('Error ：', e)

        print('Save {} successfully'.format(filename))
        return filename

    # 请求网页，跳转到最终 img 地址
    def get_img_url(self, raw_img_url):
        r = requests.get(raw_img_url)
        img_url = r.url  # 得到图片文件的网址
        print('img_url:', img_url)
        return img_url

    # 设置图片绝对路径 filepath 所指向的图片为壁纸
    def set_img_as_wallpaper(self, filepath):
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, filepath, 1 + 2)
        print("Set {} as wallpaper succeed".format(filepath))

    def create_blur_image(self, file_path, redius=2):
        """
        将图片进行高斯模糊后修改后缀另行保存
        """
        origin = Image.open(file_path)
        treated = origin.filter(ImageFilter.GaussianBlur(redius))
        img_path_blur = file_path.replace(".jpg", "_blur.jpg")
        treated.save(img_path_blur)
        return img_path_blur

    def main(self):
        img_url = self.get_img_url(self.bing_url)
        file_path = self.save_img(img_url, self.save_dir_img)  # 图片文件的的路径
        # file_path = self.create_blur_image(file_path)
        self.set_img_as_wallpaper(file_path)


if __name__ == "__main__":
    BingImage().main()
