from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import requests
import io
import gzip
import json
import os
from datetime import datetime
import UnityPy

def extract_all_assets(env, output_dir):
    

    for obj in env.objects:
        try:
            if obj.type.name == "Sprite":
                data = obj.read()
                os.makedirs(output_dir+"Sprite/", exist_ok=True)
                path = os.path.join(output_dir+"Sprite/", f"{data.m_Name}.png")
                data.image.save(path)
            if obj.type.name == "Texture2D":
                data = obj.read()
                os.makedirs(output_dir+"Texture2D/", exist_ok=True)
                path = os.path.join(output_dir+"Texture2D/", f"{data.m_Name}.png")
                data.image.save(path)
            if obj.type.name == "MonoBehaviour":
                if obj.serialized_type.node:
                # save decoded data
                    tree = obj.read_typetree()
                    os.makedirs(output_dir+"MonoBehaviour/", exist_ok=True)
                    if tree['m_Name'] == "":
                        fp = os.path.join(output_dir + "MonoBehaviour/", f"{tree['m_Name']}_{obj.path_id}.json")
                    else:
                        fp = os.path.join(output_dir + "MonoBehaviour/", f"{tree['m_Name']}.json")
                    with open(fp, "wt", encoding = "utf8") as f:
                        json.dump(tree, f, ensure_ascii = False, indent = 4)


        except Exception as e:
            print(e)
   

def decrypt(content):
    key = b"kms1kms2kms3kms4"
    iv = b"nekonekonyannyan"

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = decryptor.update(content) + decryptor.finalize()
    decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return decrypted_data

class Otogi_Utils():

    def __init__(self):
        # 角色编号1001~2229
        # hs编号 = 2+ 角色编号 + 1/2
        # 主页立绘差分 = 角色编号 +1
        # 全身立绘 = 角色编号 + 1~6
        # decrypt hs编号
        self.hs_url = "https://web-assets.otogi-frontier.com/prodassets/GeneralWebGL/Assets/chara/still/"
        # 主页spine
        self.homestand_url = "https://web-assets.otogi-frontier.com/prodassets/GeneralWebGL/Assets/chara/homestand/"
        # 全身立绘
        self.standimagelarge_url = "https://web-assets.otogi-frontier.com/prodassets/GeneralWebGL/Assets/chara/standimagelarge/"

        self.MATSTER_DATA = json.loads(open("./lib/otogi/master_data.json", 'r', encoding='UTF-8').read())
        
    def updata_master(self):
        print("updata_master:开始")
        url = "https://web-assets.otogi-frontier.com/prodassets/MasterData/MMonsters.gz"
        res = requests.get(url)
        if res.status_code == 200:
            try:
                with gzip.GzipFile(fileobj=io.BytesIO(res.content)) as gz_file:
                    decompressed_data = gz_file.read().decode('utf-8')
                    json_data = json.loads(decompressed_data)
                    master_data = []
                    for data in json_data:
                        id = data["id"]
                        name = data["n"]
                        master_data.append({id:name})

                    with open("./lib/otogi/master_data.json", 'w', encoding='UTF-8') as file:
                        json.dump(master_data, file,ensure_ascii=False,indent=4)
                    
                    self.MATSTER_DATA = master_data
                    print("updata_master otogi:成功")
                    return True
            except Exception as e:
                print(f"解压失败: {e}")
                return False

        else:
            print(res.status_code)
            print("updata_master:失败")
            return False

    def get_meta(self):
        timestamp = os.path.getmtime("./lib/otogi/master_data.json")

        modified_time = datetime.fromtimestamp(timestamp)

        return {
            "version": str(int(timestamp)),
            "update_time": modified_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_single_resource(self, url, timeout=20):
        try:
            res = requests.get(url, timeout=timeout, stream=True)
            if res.status_code == 200:
                # 使用流式读取响应内容
                content = b""
                for chunk in res.iter_content(chunk_size=1024):
                    content += chunk
                return content
            else:
                print(f"Request failed with status code: {res.status_code}")
                return None
        except requests.exceptions.Timeout:
            print("The request timed out.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


    def get_resource(self,type,path):
        reveiw_content = None
        output_dir = ""
        try:
            if type == "主页立绘差分":
                url = self.homestand_url+path
                content = self.get_single_resource(url)
                env = UnityPy.load(content)
                output_dir = "./resource/otogi/chara/homestand/"+path+"/"
                extract_all_assets(env,output_dir)
                with open("./resource/otogi/chara/homestand/"+path+"/Sprite/_stand1.png","rb") as f:
                    reveiw_content = f.read()

            elif type == "静态立绘":
                url = self.standimagelarge_url+path
                content = self.get_single_resource(url)
                env = UnityPy.load(content)
                output_dir = "./resource/otogi/chara/standimagelarge/"+path+"/"
                extract_all_assets(env,output_dir)
                with open(f"./resource/otogi/chara/standimagelarge/{path}/Sprite/{path}.png","rb") as f:
                    reveiw_content = f.read()
                
            elif type == "hs_cg":
                url = self.hs_url+path
                content = self.get_single_resource(url)
                decrypt_content = decrypt(content)

                env = UnityPy.load(decrypt_content)
                output_dir = "./resource/otogi/chara/still/"+path+"/"
                extract_all_assets(env,output_dir)

                with open("./resource/otogi/chara/still/"+path+"/"+path,"wb") as f:
                    f.write(decrypt_content)

                largest_file = None
                max_size = 0

                for file in os.listdir("./resource/otogi/chara/still/"+path+"/Texture2D/"):
                    file_path = os.path.join("./resource/otogi/chara/still/"+path+"/Texture2D/", file)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        # 更新最大文件
                        if file_size > max_size:
                            largest_file = file_path
                            max_size = file_size
                
                if largest_file:
                    with open(largest_file,"rb") as f:
                        reveiw_content = f.read()

            return {"content": reveiw_content,
                    "file_name": output_dir}

        except:
            print("路径错误")
            return None

# o = Otogi_Utils()
# o.get_resource("hs_cg","218991")