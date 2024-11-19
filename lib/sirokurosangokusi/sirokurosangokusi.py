import requests
import os
import json
from datetime import datetime
import hashlib

class Sirokurosangokusi_Utils():
    def __init__(self):
        self.MATSTER_DATA = json.loads(open("./lib/sirokurosangokusi/resource.json", 'r', encoding='UTF-8').read())
        self.resource_path = "./resource/sirokurosangokusi/"
        self.cdn_url = "https://cdn-production.nobunagasangoku.com/client/res/"
        self.session = requests.Session()
        self.headers = {"Referer": "https://web-r-production.nobunagasangoku.com/"}

    def download_single_file(self,url):
        print("downloading:" + url)

        respones = self.session.get(url,headers=self.headers)
        if respones.status_code == 200:
            
            return respones.content
        else:
            print(respones.status_code)
            return None
    
    def get_resource(self,type,path:str):
        resource_path = ""
        resource_url = ""
        resource_list = []
        try:
            if type == "hs_anime":
                # # https://cdn-production.nobunagasangoku.com/client/res/animation/h/1100100_H01/h_1100100_H01_128.jpg
                resource_path = "animation/h/"+path
                for resource in self.MATSTER_DATA:
                    if resource.startswith(resource_path) and "SP/sp" not in resource:
                        resource_list.append({
                            resource : self.cdn_url+resource
                        })
                resource_url = self.cdn_url+"animation/h/"+path+"/h_"+path+"_001.jpg"
            
            elif type == "hs_cg":
                # # https://cdn-production.nobunagasangoku.com/client/res/image/cg/cg_1100100_H01_02.jpg
                resource_path = "image/cg/cg_"+path
                for resource in self.MATSTER_DATA:
                    if resource.startswith(resource_path):
                        resource_list.append({
                            resource : self.cdn_url+resource
                        })
                resource_url = self.cdn_url+"image/cg/cg_"+path+"_01.jpg"

            elif type == "hs_voice":
                #  path 1100100_H01
                # https://cdn-production.nobunagasangoku.com/client/res/sound/voice/1100100/voice_1100100_H01_01.m4a
                resource_path = "sound/voice/"+path.split("_")[0]+"/voice_"+path
                for resource in self.MATSTER_DATA:
                    if resource.startswith(resource_path):
                        resource_list.append({
                            resource : self.cdn_url+resource
                        })
                resource_url = self.cdn_url+"sound/voice/"+path.split("_")[0]+"/voice_"+path+"_01.m4a"
            
            elif type == "bgm":
                # # https://cdn-production.nobunagasangoku.com/client/res/sound/bgm/bgm_4010016.m4a
                resource_path = "sound/bgm/"+path+".m4a"
                resource_list.append({
                            resource_path : self.cdn_url+resource_path
                        })
                resource_url = self.cdn_url+"sound/bgm/"+path+".m4a"

            elif type == "头像":
                # https://cdn-production.nobunagasangoku.com/client/res/image/unit/character/tm/c_tm_1100100.png
                resource_path = "image/unit/character/tm/c_tm_"+path+".png"
                resource_list.append({
                            resource_path : self.cdn_url+resource_path
                        })
                resource_url = self.cdn_url+"image/unit/character/tm/c_tm_"+path+".png"

            elif type == "立绘":
                # https://cdn-production.nobunagasangoku.com/client/res/image/unit/character/st/c_st_1100100_00.png
                resource_path = "image/unit/character/st/c_st_"+path+"_00.png"
                resource_list.append({
                            resource_path : self.cdn_url+resource_path
                        })
                resource_url = self.cdn_url+"image/unit/character/st/c_st_"+path+"_00.png"

            elif type == "立绘大":
                # https://cdn-production.nobunagasangoku.com/client/res/image/unit/character/ff/c_ff_1100100.png
                resource_path = "image/unit/character/ff/c_ff_"+path+".png"
                resource_list.append({
                            resource_path : self.cdn_url+resource_path
                        })
                resource_url = self.cdn_url+"image/unit/character/ff/c_ff_"+path+".png"

            elif type == "表情差分":
                # https://cdn-production.nobunagasangoku.com/client/res/image/unit/character/fc/c_fc_1100100.png
                resource_path = "image/unit/character/fc/c_fc_"+path+".png"
                resource_list.append({
                            resource_path : self.cdn_url+resource_path
                        })
                resource_url = self.cdn_url+"image/unit/character/fc/c_fc_"+path+".png"

            elif type == "资源路径":
                resource_path = path
                resource_list.append({
                            resource_path : self.cdn_url+resource_path
                })
                resource_url = self.cdn_url+resource_path
            else:
                print("type error")
                return None
            resource_dict = {
                "resource_url": resource_url,
                "resource_list": resource_list
            }
            return resource_dict
        except Exception as e:
            print(e)
            return None


    def updata_master(self):
        respones = self.session.get(self.cdn_url+"resource.txt",headers=self.headers)
        if respones.status_code == 200:
            resource = respones.text.split("\n")
            for i in range(len(resource)):
                if resource[i].startswith("./"):
                    resource[i] = resource[i][2:]
            with open("./lib/sirokurosangokusi/resource.json","w",encoding="utf-8") as f:
                json.dump(resource,f,indent=4)
            return True
        else:
            print(respones.status_code)
            return False
        
    def get_meta(self):
        timestamp = os.path.getmtime("./lib/sirokurosangokusi/resource.json")

        modified_time = datetime.fromtimestamp(timestamp)

        return {
            "version":  hashlib.md5(open("./lib/sirokurosangokusi/resource.json", 'rb').read()).hexdigest()[-10:],
            "update_time": modified_time.strftime("%Y-%m-%d %H:%M:%S")
        }


# s  = Sirokurosangokusi_Utils()
