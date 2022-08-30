# CourseWork Tyan V. PY-59
# Backup photo from VK to Yandex Disk/

from unicodedata import name
import requests
from pprint import pprint
import yadisk
import time
from tqdm import tqdm 
    



class VK:
   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version, 'album_id': 'profile', 'extended': 1}


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
            for size in vk_size_type: # Делает список фото  максимального размера 
                for photo in reversed(photo_info):
                    if size in photo['type']:
                        photo['name'] = items['name']
                        photo['date'] = time.strftime("%Y_%m_%d", time.gmtime(items['date']))
                        list_photo.append(photo)
                        break                    
                    break
        n=0
        for max_photo in list_photo[n:]: #Сравнивает имена фото в итоговом списке, если одинаковые, добавляет дату.
            for i in list_photo[n+1:]:
                if max_photo['name'] == i['name']:
                    max_photo['name'] = (str(max_photo['date']) + "_" + str(max_photo['name']))
                    list_photo[n] = max_photo
                    break
            n += 1 
        return list_photo
    
def uppload_file_to_YaDisk(y, list_photo):
# Загрузка фотографий на Яндекс Диск
    count_photo = 5
    print()
    print(f'Всего найдено {len(list_photo)} фотографий')
    print('Будет гружено 5 максимального размера')
    print()
    count_photo_user = input('Если хотите изменить количество, введите "да". Для продолжения нажмите Enter: ')

    if str.lower(count_photo_user) == 'да': 
        count_photo_user = int(input(f'Введите количество загружаемых фото от 1 до {len(list_photo)}: ')) 
        count_photo = count_photo_user
    try:       
        y.mkdir("/" + name_folder) 
        vk_size_type = ['w','z','y','r','q','p','o','x','m','s']
        sort_size_photo = []
        for size in vk_size_type:    
            for photo in list_photo:
                if size == photo['type']:
                    sort_size_photo.append(photo)
                
        for photo in tqdm(sort_size_photo[0:count_photo]):
                path = (name_folder + '/' + photo['name'])
                y.upload_url(photo['url'], path)
                time.sleep(0.33)
        print()
        print('Загрузка завершена')
    except:
        print()
        print('Ошибка подключения или такая папка уже существует') 
    return sort_size_photo


if __name__ =="__main__":
    
    with open('tokens.txt', 'r',encoding='utf-8') as file_object: # Считывает токены из файла tokens.txt
        list_file = file_object.readlines()
        access_token =  list_file [1].strip()
        TOKEN_YA =  list_file [3].strip()
            
    user_id = input('Введите id пользователя ВКонтакте: ')
    name_folder = input('Введите название папки: ')
    # user_id = 1222
    
    vk = VK(access_token, user_id)
    list_photo = vk.users_photo()  

    y = yadisk.YaDisk(token=TOKEN_YA)
    sorted_list_foto = uppload_file_to_YaDisk(y, list_photo) # Вызывает функцию загрузки фото на ЯД

    list_info_photo = []  # Выводит данные о фото на терминал 
    for photo in sorted_list_foto:
        info_photo_dict = {}
        info_photo_dict['file_name'] = photo['name']
        info_photo_dict['type'] = photo['type']
        list_info_photo.append(info_photo_dict)
    print()
    pprint(list_info_photo)
    
