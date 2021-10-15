#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests as rq
import os
import json
import configparser
import time
from tqdm import tqdm
from pprint import pprint
import yadisk
import pathlib
from pathlib import Path  


# In[1]:


pip install yadisk


# In[38]:


class UserService:
    def __init__(self, user_id, token, yandex_token, file_path):
        self.user_id = user_id
        self.token = token  
        self.yandex_token = yandex_token
        self.file_path = file_path

        
    def _get_photos_from_folder(self) -> list:
        file_list = os.listdir(self.file_path)
        return file_list

    
    def download_photo(self):
        URL = 'https://api.vk.com/method/photos.get'
        params = {'access_token': self.token,
            'v': '5.131',
            'album_id': 'profile',
            'owner_id': self.user_id,
            'extended': 1,
            'photo_sizes': 1
        }
        
        res = rq.get(URL, params=params)
        response1 = res.json()
        logs_list = []

        for file in tqdm(response1['response']['items']):
            time.sleep(3)
            size = file['sizes'][-1]['type']
            photo_url = file['sizes'][-1]['url']
            file_name = file['likes']['count']
            download_photo = rq.get(photo_url)
            with open(f'{self.file_path}/{file_name}.jpg', 'wb') as f:
                f.write(download_photo.content)
                
        download_log = {'file_name': file_name, 'size': size}
        logs_list.append(download_log)
            
                        
    def create_folder(self):
        y = yadisk.YaDisk(token=self.yandex_token)
        if y.exists("/Bd/") == False:
            y.mkdir("/Bd/")
        
            
    
    def upload(self):
        headers = {"Authorization" : f'OAuth {self.yandex_token}'}
        y = yadisk.YaDisk(token=self.yandex_token)
        
        for photo in tqdm(self._get_photos_from_folder()):
            time.sleep(3)
            with open(f'{self.file_path}/{photo}', 'rb') as w:
                file_upload = y.upload(w, f"/Bd/{photo}")

            
if __name__ == '__main__':
    path = Path('Desktop', "photos_vk")
    user = UserService(..., '...', '...', path)
    save_photos = user.download_photo()
    user.create_folder()
    back_up = user.upload()


# In[ ]:




