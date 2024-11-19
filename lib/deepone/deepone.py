import json
import requests
import hashlib
from datetime import datetime
import os

MATSTER_DATA_URL = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_game_ld/download_res_hash.manifest"


def getMD5(input):
    input = '47cd76e43f74bbc2e1baaf194d07e1fa' + input
    result = hashlib.md5(input.encode()) 
    return result.hexdigest() 

def get_real_path(str1):
    e=''
    i=''
    a=''
    n=''
    if str1[0]=='c' or str1[0]=='d' or str1[0]== 'e' or str1[0]=='f':
        e = str1[6:8]+'/'
        i = str1[2:4] + "/"
        a = str1[4:6] + "/"
        n = str1[0:2] + "/" 
    elif str1[0]=='8' or str1[0] =='9' or str1[0]=='a' or str1[0] =='b':
        e = str1[4:6]+ "/"
        i = str1[0:2]+ "/"
        a = str1[6:8]+ "/"
        n = str1[2:4]+ "/"
    elif int(str1[0])>=4 and int(str1[0])<=7:
        e = str1[2:4]+ "/"
        i = str1[6:8]+ "/"
        a = str1[0:2]+ "/"
    elif int(str1[0])>=0 and int(str1[0])<=3:
        e = str1[0:2]+ "/"
        i = str1[4:6]+ "/"
    return  e + i + a + n

def get_url(file_name):
    cdn_url = "https://tonofura-r-cdn-resource.deepone-online.com/deep_one/download_game_hd/"
    md5 = getMD5(file_name)
    path = get_real_path(md5)
    file_end = '.'+file_name.split(".")[-1]
    if '.atlas.txt' in file_name:
        file_end = '.atlas.txt'
    return cdn_url+path+md5+file_end


class Deepone_Utils():

    def __init__(self):
        self.MATSTER_DATA = json.loads(open("./lib/deepone/download_res_hash.manifest", 'r', encoding='UTF-8').read())

    def get_resource(self,type,path):
        resource_path = ""
        resource_list = []
        try:
            if type == '卡面':
                resource_path = "character/"+path+"/image/main.png"
                resource_list.append({
                    resource_path: get_url(resource_path)
                })

            elif type == 'MEMORIAL':
                resource_path = "character/"+path[:4]+"/image/"+path+".png"
                resource_list.append({
                    resource_path: get_url(resource_path)
                })

            elif type == '立绘':
                resource_path = "character/"+path+"/image/stand.png"
                resource_list.append({
                    resource_path: get_url(resource_path)
                })

            elif type == '寝室预览':
                resource_path = "gallery/episode/"+path+".png"
                resource_list.append({
                    resource_path: get_url(resource_path)
                })

            elif type == 'BGM':
                resource_path = "sound/bgm/"+path+".mp3"
                resource_list.append({
                    resource_path: get_url(resource_path)
                })

            elif type == '资源路径':
                resource_path = path
                resource_list.append({
                    resource_path: get_url(resource_path)
                })

            elif type == 'spine':
                # character/100101/spine/room/room.png
                resource_path = f"character/{path}/spine/room/room.png"
                # character/104110/spine
                spine_path = f"character/{path}/spine"
                for k,v in self.MATSTER_DATA["assets"].items():
                    if spine_path in k:
                        resource_list.append({
                            k: get_url(k)
                        })
            elif type == 'specialRoom':
                # specialRoom/4037001/image/sp_room_list_A.png
                resource_path = "specialRoom/"+path+"/image/sp_room_list_A.png"
                sp_room_path = "specialRoom/"+path
                for k,v in self.MATSTER_DATA["assets"].items():
                    if sp_room_path in k:
                        resource_list.append({
                            k: get_url(k)
                        })


        except:
            print("路径错误")
            return None

        resource_dict = {
            "resource_url": get_url(resource_path),
            "resource_list": resource_list
        }

        return resource_dict
    
    def download_single_file(self,url):
        print("downloading:" + url)
        
        respones = requests.get(url)
        if respones.status_code == 200:
            return respones.content
        else:
            print(respones.status_code)
            return None


    def updata_master(self):
        respones = requests.get(MATSTER_DATA_URL)
        if respones.status_code == 200:
            master_data = json.loads(respones.text)
            with open("./lib/deepone/download_res_hash.manifest", 'w', encoding='UTF-8') as file:
                json.dump(master_data, file)

            self.MATSTER_DATA = master_data
            return True
        else:
            print(respones.status_code)
            return False

    def get_meta(self):
        timestamp = os.path.getmtime("./lib/deepone/download_res_hash.manifest")

        modified_time = datetime.fromtimestamp(timestamp)

        return {
            "version": str(int(timestamp)),
            "update_time": modified_time.strftime("%Y-%m-%d %H:%M:%S")
        }



