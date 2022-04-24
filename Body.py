import API_information_upload
import Prediction
import numpy as np

# Ввод api ключа
print(
    "I need your api key. Go to this link, copy url and send me\nhttps://oauth.vk.com/authorize?client_id=7596731&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52")
api = input()
api = api[api.find("=") + 1:api.find("=") + 86]
key = 1
while key == 1:
    # Ввод id
    id_ = input("Enter id\n")
    # Получение признаков
    inf = np.array(API_information_upload.fake_info(id_, api))
    # Классификация
    pred = Prediction.get_pred1(inf)
    # Вывод
    c = ['Original', 'fake']
    print(c[pred[0]])
    key = int(input("Repeat - 1\nExit - 0\n"))
