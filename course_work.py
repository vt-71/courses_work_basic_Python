from itertools import count
import requests
from pprint import pprint


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
        list_photo = []
        counter = 0
        vk_size_type = ['w','z','y','r','q','p','o','x','m','s']
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id}
        response = requests.get(url, params={**self.params, **params})
        for items in response.json()['response']['items']:
            items['name'] = (str(items['likes']['count']) + ".jpg")
            photo_info = items['sizes']
            # pprint(items['name'])           
            for size in vk_size_type:  
                for photo in reversed(photo_info):
                    if size in photo['type']:
                        # pprint(photo_info)
                        photo['name'] = items['name']
                        list_photo.append(photo)
                        counter += 1
                        break                    
                    break             
        return list_photo


access_token = 'vk1.a.guBSUV6VmU9kPXdsPy9w0IOT590UWSG6kxuQCSsMIYrdURdd_v8PVKoiujjQjxuQH2QjDyRPqkaSB-tU7PmSb0PbbGE-NcfDMBrTTEr3FMfF4UvQXkl8uB3e5amd5RVXheCCIiDIqY6du16au1pUbDO4kidXUQH44yEdB8LYVku89XFQ8FJaieYC7lgYtgky'
TOKEN_YA = 'y0_AQAAAAA_A4UUAADLWwAAAADLF6At6ut-A5tiQZ62UcSdetciEoASM_s'
user_id = 1222
# user_id = 510358665
# user_id = 5555332

# user_id = 7970141
vk = VK(access_token, user_id)
pprint(vk.users_photo())
# vk.users_photo()
# pprint(vk.users_info())
