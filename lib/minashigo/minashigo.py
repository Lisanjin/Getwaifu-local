import json,os
from datetime import datetime
import base64
from hashlib import sha256
import hashlib
import requests
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes

Buffer = bytes | bytearray | memoryview

def get_resource_md5(filepath,quality,MANIFEST):
    return MANIFEST["assets"][filepath][quality]["md5"]

def get_resource_path(filepath,quality,MANIFEST):
    md5 = get_resource_md5(filepath,quality,MANIFEST)
    return get_adv_resource_path(filepath,md5)

def best_quality(asset_md5_dir):
    quality_list = []
    for quality,asset_md5 in asset_md5_dir.items():
        quality_list.append(int(quality))
    return str(max(quality_list))

def get_adv_resource_path(path: str, md5_hex: str) -> str:
    def get_path(h):
        parts = []
        if h[0] in '0123':
            parts.extend([h[0:2], h[4:6]])
        elif h[0] in '4567':
            parts.extend([h[2:4], h[6:8], h[0:2]])
        elif h[0] in '89ab':
            parts.extend([h[4:6], h[0:2], h[6:8], h[2:4]])
        else:  # 'cedf'
            parts.extend([h[6:8], h[2:4], h[4:6], h[0:2]])
        return '/'.join(parts)

    e = hash_md5(path.encode()).hex()
    d = path.rindex('.')
    i, ext = path[:d], path[d:]
    p = get_path(hash_md5(i.encode()).hex())
    return f'{e}/{p}/{md5_hex}{ext}'

def hash_md5(plaintext: Buffer):
    return hashlib.md5(plaintext).digest()

def hash_sha256(plaintext: Buffer):
    return hashlib.sha256(plaintext).digest()

def decrypt_resource(plaintext: str | bytes):
    sha256 = hash_sha256(b'#mnsg#manifest')
    password = base64.b64encode(sha256)[:32]
    return aes_ctr_decrypt(plaintext, password)

def kdf(password: bytes, salt: bytes):
    derived = b''
    while len(derived) < 48:
        hasher = hashlib.md5()
        hasher.update(derived[-16:] + password + salt)
        derived += hasher.digest()
    return derived[0:32], derived[32:]  # key, iv

def aes_ctr_decrypt(plaintext: str | bytes, password: bytes):
    '''
    :param plaintext: base64 encoded plaintext
    :param password: password for kdf
    :return: decrypted plaintext
    '''
    data = base64.b64decode(plaintext)
    salt, plaintext = data[8:16], data[16:]
    key, iv = kdf(password, salt)
    ctr = Counter.new(AES.block_size * 8, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return unpad(cipher.decrypt(plaintext), AES.block_size)

class Minashigo_Utils():

    def __init__(self):
        self.MATSTER_DATA = json.loads(open("./lib/minashigo/resource.json", 'r', encoding='UTF-8').read())

    def updata_master(self):
        def get_version():
            url = "https://minasigo-no-shigoto-web-r-server.orphans-order.com/mnsg/user/getVersion"
            res = requests.get(url)
            return json.loads(res.text)
        
        version = get_version()
        # 获取版本号
        RESOURCE_VERSION = version["version"]["resourceVersion"]
        MATSTER_DATA_URL = 'https://minasigo-no-shigoto-pd-c-res.orphans-order.com/'+RESOURCE_VERSION+'/' + 'resource.json'

        respones = requests.get(MATSTER_DATA_URL)
        if respones.status_code == 200:
            decrypted_data = decrypt_resource(respones.text).decode()

                    
            with open("./lib/minashigo/resource.json", 'w', encoding='UTF-8') as file:
                file.write(decrypted_data)

            self.MATSTER_DATA = json.loads(decrypted_data)
            return True
        else:
            print(respones.status_code)
            return False
        
    def download_single_file(self,url):
        print("downloading:" + url)
        
        respones = requests.get(url)
        if respones.status_code == 200:
            return respones.content
        else:
            print(respones.status_code)
            return None
    
    def get_resource(self,type,path):
        resource_path = ""
        resource_list = []
        try:
            if type == '角色卡面':
                # image/character/stand/10010101.png
                resource_path = "image/character/stand/"+path+"01.png"

                for k,v in self.MATSTER_DATA["assets"].items():
                    if "image/character/stand/"+path in k:
                        resource_list.append({
                            k: self.get_url(k)
                        })

            elif type == '战神卡面':
                # image/summon/stand/30010101.png
                resource_path = "image/summon/stand/"+path+"01.png"

                for k,v in self.MATSTER_DATA["assets"].items():
                    if "image/summon/stand/"+path in k:
                        resource_list.append({
                            k: self.get_url(k)
                        })

            elif type == '寝室预览':
                # image/episode/story/2010010111.png
                resource_path = "image/episode/story/"+path+".png"
                resource_list.append({
                    resource_path: self.get_url(resource_path)
                })
            elif type == '战神Spine':
                # spine/summon/304501/314501.png
                
                spine_path = "spine/summon/"+path+"/"
                for k,v in self.MATSTER_DATA["assets"].items():
                    if spine_path in k:
                        if k.endswith(".png"):
                            resource_path = k
                        resource_list.append({
                            k: self.get_url(k)
                        })
                
            elif type == 'BGM':
                # sound/bgm/bgm_002.mp3
                resource_path = "sound/bgm/"+path+".mp3"
                resource_list.append({
                    resource_path: self.get_url(resource_path)
                })

            elif type == '资源路径':
                resource_path = path
                resource_list.append({
                    resource_path: self.get_url(resource_path)
                })

        except:
            print("路径错误")
            return None

        resource_dict = {
            "resource_url": self.get_url(resource_path),
            "resource_list": resource_list
        }
        print(resource_dict)

        return resource_dict
    
    def get_url(self, file_name):
        RESOURCE_HOSTURL = 'https://minasigo-no-shigoto-pd-c-res.orphans-order.com/'+self.MATSTER_DATA["version"]+'/'

        for asset_path,asset_md5_dir in self.MATSTER_DATA["assets"].items():

            # if "image/episode/story/2" in asset_path:
            if file_name == asset_path:
                quality = best_quality(asset_md5_dir)
                dl_path = RESOURCE_HOSTURL + get_resource_path(asset_path,quality,self.MATSTER_DATA)
                return dl_path
    
    def get_meta(self):

        timestamp = os.path.getmtime("./lib/minashigo/resource.json")

        modified_time = datetime.fromtimestamp(timestamp)

        return {
            "version": self.MATSTER_DATA["version"],
            "update_time": modified_time.strftime("%Y-%m-%d %H:%M:%S")
        }


# m = Minashigo_Utils()
# print(m.get_url("spine/character/200101/200101.atlas.txt"))
