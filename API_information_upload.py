import vk
import Face_Detection
from PIL import Image
import requests
import time


def sear(a, dic):
    flag = False
    for i in dic:
        if i == a:
            return True
    return flag


def zap(info, friends, wall, date_first_post, nickname, face_c, school, lk, rel, site, city, ocup):
    attribute = [
                 friends['count'] if sear('count', friends) else -1,
                 info[0]['counters']['followers'] if sear('followers', info[0]['counters']) else -1,
                 wall['count'] if sear('count', wall) else -1,
                 info[0]['counters']['pages'] if sear('groups', info[0]['counters']) else -1,
                 info[0]['counters']['subscriptions'] if sear('subscriptions', info[0]['counters']) else -1,
                 1 if nickname != '' else 0,
                 info[0]['counters']['photos'] if sear('photos', info[0]['counters']) else -1,
                 info[0]['counters']['audios'] if sear('audios', info[0]['counters']) else -1,
                 info[0]['counters']['gifts'] if sear('gifts', info[0]['counters']) else -1,
                 info[0]['counters']['videos'] if sear('videos', info[0]['counters']) else -1,
                 face_c,
                 school,
                 lk,
                 city,
                 ocup,
    ]
    print(attribute)
    return attribute


# print('https://oauth.vk.com/authorize?client_id=7596731&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52')
#     attribute = {'id': None, 'date_first_post': None, 'friends': None, 'recently_friends': None,
#                  'followers': None, 'wall': None, 'recently_wall': None, 'groups': None,
#                  'subscriptions': None, 'nick': None, 'photo': None, 'audio': None, 'presents': None,
#                                                                                         'video': None}
def fake_info(fake_link, key):
    q = '0123456789'
    nick = ''
    session = vk.Session(key)
    api = vk.API(session, v='5.124')
    while fake_link.find(' ') != -1:
        fake_link = fake_link[:fake_link.find(' ')]
    # Вводим ссылку на фэйк и достаем из нее id
    #     fake_link = input('Enter fake link\n')
    if fake_link.find('https://') != -1:
        fake_link = fake_link[8:]

    if (fake_link.find('/id') != -1) and (q.find(fake_link[fake_link.find('/id') + 3]) != -1):
        id_fake = fake_link[9:]
        s = s = api.users.get(user_ids=id_fake)
    else:
        nick = fake_link[7:]
        s = api.users.get(user_ids=nick)
        id_fake = s[0]['id']

    # вытягиваем информацию
    if sear('deactivated', s[0]) or not s[0]['can_access_closed']:
        return {}

    fake_user_info = api.users.get(user_id=id_fake, fields='counters, domain, schools, occupation, site, universities, relation, city')
    # список друзей
    if fake_user_info[0]['domain'][:2] == "id":
        nick = ''
    else:
        nick = fake_user_info[0]['domain']

    fake_user_friends = api.friends.get(user_id=id_fake, order='hits')
    # записи со стены
    a = time.time()
    while time.time() - a < 1:
        q = 1

    fake_user_wall = api.wall.get(owner_id=id_fake, count=100)
    # найдем дату первого поста
    lk = 0;
    if fake_user_wall['count'] > 0:
        if fake_user_wall['count'] > 100:
            date_first_post = fake_user_wall['items'][99]['date']
        else:
            date_first_post = fake_user_wall['items'][fake_user_wall['count'] - 1]['date']
        if sear('attachments', fake_user_wall['items'][0]):
            lk = int(fake_user_wall['items'][0]['attachments'][0]['type'] == 'link')
    else:
        date_first_post = 0
    # фото со стены
    face_c = 0
    fake_user_photo = api.photos.get(owner_id=id_fake, album_id='profile')
    if len(fake_user_photo["items"]) > 0:
        ava = fake_user_photo["items"][-1]["sizes"][-1]["url"]
        response = requests.get(ava, stream=True).raw
        img = Image.open(response)
        img.save('photo/' + str(fake_user_info[0]['id']) + '.jpg', 'jpeg')
        face_c = int(Face_Detection.face_count('photo/' + str(fake_user_info[0]['id']) + '.jpg') > 0)
    if sear('schools', fake_user_info[0]):
        sch = len(fake_user_info[0]['schools'])
    else:
        sch = 0
    if sear('universities', fake_user_info[0]):
        un = len(fake_user_info[0]['universities'])
    else:
        un = 0
    if sear('relations', fake_user_info[0]):
        rel = fake_user_info[0]['relations']
    else:
        rel = 0
    if sear('site', fake_user_info[0]):
        site = 1
    else:
        site = 0
    if sear('city', fake_user_info[0]):
        city = 1
    else:
        city = 0
    if sear('occupation', fake_user_info[0]):
        if fake_user_info[0]['occupation']['type'] == 'work':
            ocup = 1
        elif fake_user_info[0]['occupation']['type'] == 'school':
            ocup = 2
        else:
            ocup = 3
    else:
        ocup = 0
    return zap(fake_user_info, fake_user_friends, fake_user_wall, date_first_post, nick, face_c,
               sch + un, lk, rel, site, city, ocup)
