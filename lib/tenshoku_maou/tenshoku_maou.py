import subprocess
import shutil
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image


class Tenshoku_Maou_Utils():

    def __init__(self):
        self.cdn_url = self.get_cdn()
        self.MATSTER_DATA = json.loads(open("./lib/tenshoku_maou/config.json", 'r', encoding='UTF-8').read())
        if self.MATSTER_DATA["version"] != self.cdn_url.split("/")[-2]:
            self.updata_master()

        self.asset_type = ["text", "json", "wasm", "sprite", "font", "material", "texture", "audio", "textureatlas", "template", "script"]
        self.basisu_path = "./lib/tenshoku_maou/basisu.exe"
        self.resource_path = "./resource/tenshoku_maou/"
        os.makedirs(self.resource_path, exist_ok=True)

    def unpack(self, input_path :str):
        file_name = input_path.split("/")[-1].replace(".basis", "")
        try:
            result = subprocess.run(
                [self.basisu_path, "-format_only", "1", "-no_ktx", input_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            print("输出:", result.stdout)
            print("错误:", "无" if result.stderr == "" else result.stderr)

            shutil.move( os.path.join(f"{file_name}_unpacked_rgba_ETC2_RGBA_0000.png"), self.resource_path + file_name + ".png")

            os.remove(os.path.join(f"{file_name}_unpacked_rgb_ETC2_RGBA_0000.png"))
            os.remove(os.path.join(f"{file_name}_unpacked_a_ETC2_RGBA_0000.png"))

        except subprocess.CalledProcessError as e:
            print("命令执行失败:", e)
            print("输出:", e.stdout)
            print("错误:", e.stderr)
        except Exception as e:
            print(e)
    
    def get_cdn(self):
        print("开始获取tenshoku_maou cdn")

        respones = requests.get("https://app-dot-king-20240410.an.r.appspot.com/5791070751293440/game/adult")
        if respones.status_code == 200:
            soup = BeautifulSoup(respones.text, 'html.parser')
            manifest_href = soup.find("link", {'rel': 'manifest'})['href']
            cdn_url = manifest_href.replace("manifest.json", "")

            print("获取成功",cdn_url)
        return cdn_url

    def updata_master(self):
        print("updata_master")
        print(self.cdn_url+"config.json")
        respones = requests.get(self.cdn_url+"config.json")
        if respones.status_code == 200:
            master_data = json.loads(respones.text)
            master_data["version"] = self.cdn_url.split("/")[-2]

            with open("./lib/tenshoku_maou/config.json", 'w', encoding='UTF-8') as file:
                json.dump(master_data, file)
            
            with open("./lib/tenshoku_maou/names.json", 'w', encoding='UTF-8') as file:
                names = []
                for asset_id, asset in master_data["assets"].items():
                    names.append(asset["name"])
                json.dump(names, file, indent=4)

            self.MATSTER_DATA = master_data
            return True
        else:
            print(respones.status_code)
            return False
        
    def get_asset_type(self,path):
        print(path)
        for asset_id, asset in self.MATSTER_DATA["assets"].items():
            if path == asset["name"]:
                if asset["type"] in self.asset_type:
                    return asset["type"]
                else:
                    print("未知类型：",asset["type"])
                    return None
        print("未找到资源")
        return None

    def get_sprite(self,path):
        father = None
        for asset_id, asset in self.MATSTER_DATA["assets"].items():
            if path == asset["name"] :
                father_id = str(asset["data"]["textureAtlasAsset"])
                father = self.MATSTER_DATA["assets"][father_id]
                break
        
        url = father["file"]["variants"]["basis"]["url"]
        frames = father["data"]["frames"]
        for id,frame in frames.items():
            if frame["name"] == path:
                rect = frame["rect"]
                border = frame["border"]

                break

        respones = requests.get(self.cdn_url+url)

        if respones.status_code == 200:
            with open(self.resource_path + url.split("/")[-1], 'wb') as file:
                file.write(respones.content)

            self.unpack(self.resource_path + url.split("/")[-1])
        else:
            print(respones.status_code)
        
        textureAsset = Image.open(self.resource_path + url.split("/")[-1].replace(".basis", ".png"))
        x = rect[0]
        y = textureAsset.height - rect[1] - rect[3]
        w = rect[2]
        h = rect[3]

        sprite = textureAsset.crop((x,y,x+w,y+h))
        sprite.save(self.resource_path + path)

        with open(self.resource_path + path, 'rb') as file:
            content = file.read()

        return content

    def get_texture(self,path):
        for asset_id, asset in self.MATSTER_DATA["assets"].items():
            if path == asset["name"]:
                url = self.cdn_url + asset["file"]["variants"]["basis"]["url"]
                respones = requests.get(url)
                if respones.status_code == 200:
                    with open(self.resource_path + asset["file"]["variants"]["basis"]["filename"], 'wb') as file:
                        file.write(respones.content)

                    self.unpack(self.resource_path + asset["file"]["variants"]["basis"]["filename"])

                    with open(self.resource_path + asset["file"]["filename"], 'rb') as file:
                        content = file.read()
                    return content
                else:
                    print(respones.status_code)
        return None

    def get_simple_resource(self,path):
        for asset_id, asset in self.MATSTER_DATA["assets"].items():
            if path == asset["name"]:
                url = self.cdn_url + asset["file"]["url"]
                respones = requests.get(url)
                if respones.status_code == 200:
                    with open(self.resource_path + asset["file"]["filename"], 'wb') as file:
                        file.write(respones.content)

                    return respones.content
                else:
                    print(respones.status_code)
                
        return None
    
    def get_resource(self,type,path):

        asset_type = self.get_asset_type(path)
        if asset_type in ["text", "json","audio"]:
            content = self.get_simple_resource(path)
        elif asset_type == "sprite":
            content = self.get_sprite(path)
        elif asset_type in ["textureatlas","texture"]:
            content = self.get_texture(path)
        else:
            print("不支持的资源类型",asset_type)
            return None

        return {"type":asset_type,
                "content":content,
                "file_name":path.replace(".basis",".png"),
                }


    def get_meta(self):
        timestamp = os.path.getmtime("./lib/tenshoku_maou/config.json")

        modified_time = datetime.fromtimestamp(timestamp)

        return {
            "version": self.MATSTER_DATA["version"].split("-")[-1],
            "update_time": modified_time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def list_types(self,type):
        a = []
        for asset_id, asset in self.MATSTER_DATA["assets"].items():
            if asset["type"] == type:
                a.append({
                    "name": asset["name"],
                    "file": asset["file"]
                    # "textureAtlasAsset" : str(asset["data"]["textureAtlasAsset"])
                })
        
        with open(f"./lib/tenshoku_maou/types_{type}.json", 'w', encoding='UTF-8') as file:
            json.dump(a, file,indent=4)


# t= Tenshoku_Maou_Utils()
# t.get_sprite("splash_logo_dmm.png")
# t.get_sprite("stage_base_thumb_mask.png")
# t.list_types("textureatlas")
# t.types()
# t.get_resource("tenshoku_maou","./resource/tenshoku_maou/")
