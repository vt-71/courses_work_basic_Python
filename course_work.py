from unicodedata import name
import requests
from pprint import pprint
import yadisk
import time
# import tkinter as tk
# import tkinter.ttk as ttk
from tqdm import tqdm 
    
access_token = 'vk1.a.guBSUV6VmU9kPXdsPy9w0IOT590UWSG6kxuQCSsMIYrdURdd_v8PVKoiujjQjxuQH2QjDyRPqkaSB-tU7PmSb0PbbGE-NcfDMBrTTEr3FMfF4UvQXkl8uB3e5amd5RVXheCCIiDIqY6du16au1pUbDO4kidXUQH44yEdB8LYVku89XFQ8FJaieYC7lgYtgky'
TOKEN_YA = 'y0_AQAAAAA_A4UUAADLWwAAAADLF6At6ut-A5tiQZ62UcSdetciEoASM_s'


class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version, 'album_id': 'profile', 'extended': 1}


   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

 
   def users_photo(self):
# Метод парсит фото с ВК, переименовывает фото по лайкам.
        list_photo = []
        vk_size_type = ['w','z','y','r','q','p','o','x','m','s']
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id}
        response = requests.get(url, params={**self.params, **params})
        for items in response.json()['response']['items']:
            items['name'] = (str(items['likes']['count']) + ".jpg")
            photo_info = items['sizes']       
            for size in vk_size_type:  
                for photo in reversed(photo_info):
                    if size in photo['type']:
                        photo['name'] = items['name']
                        photo['date'] = time.strftime("%Y_%m_%d", time.gmtime(items['date']))
                        list_photo.append(photo)
                        break                    
                    break
        n=0
        for max_photo in list_photo[n:]:
            for i in list_photo[n+1:]:
                if max_photo['name'] == i['name']:
                    max_photo['name'] = (str(max_photo['date']) + "_" + str(max_photo['name']))
                    list_photo[n] = max_photo
                    break
            n += 1 
        # pprint(list_photo) 
        return list_photo

   


user_id = input('Введите id пользователя ВКонтакте: ')
name_folder = input('Введите название папки: ')
user_id = 1222
# user_id = 7970141

vk = VK(access_token, user_id)

#######################
list_photo = vk.users_photo()

y = yadisk.YaDisk(token=TOKEN_YA)
y.mkdir("/" + name_folder) 


for photo in tqdm(list_photo):
    path = (name_folder + '/' + photo['name'])
    y.upload_url(photo['url'], path)
    time.sleep(0.33)   

###############################

# vk.users_photo()


# pprint(vk.users_photo())
# pprint(vk.users_info())
