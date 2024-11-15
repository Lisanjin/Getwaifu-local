# Getwaifu-local

这个项目是之前[GetWaifu](https://github.com/Lisanjin/GetWaifu)的本地版本，懒得说明了不懂就参考原来的项目

具体的输入路径参看lib下对应游戏的资源表（deepone的是download_res_hash.manifest，孤儿的是resource.json，用记事本打开）

先点预览才会能点下载

以下说明中path代表你输入框中的输入

deepone  

| 类型     | 预览内容                                        | 下载内容                                      |
|----------|-------------------------------------------------|-----------------------------------------------|
| 卡面     | "character/"+path+"/image/main.png"             | 同预览                                        |
| MEMORIAL | "character/"+path前四位+"/image/"+path+".png"   | 同预览                                        |
| 立绘     | "character/"+path+"/image/stand.png"            | 同预览                                        |
| 寝室预览 | "gallery/episode/"+path+".png"                  | 同预览                                        |
| bgm      | "sound/bgm/"+path+".mp3"                        | 同预览                                        |
| spine    | "character/"+path+"/spine/room/room.png"        | 全部以 "character/"+path+"/spine"开头内容    |
| 资源路径 | path                                           | 同预览                                        |

孤儿的工作

| 类型     | 预览内容                                     | 下载内容                                     |
|----------|----------------------------------------------|----------------------------------------------|
| 角色卡面 | "image/character/stand/"+path+"01.png"       | 全部以 "image/character/stand/"+path开头内容 |
| 战神卡面 | "image/summon/stand/"+path+"01.png"          | 全部以 "image/summon/stand/"+path开头内容   |
| 寝室预览 | "image/episode/story/"+path+".png"           | 同预览                                       |
| bgm      | "sound/bgm/"+path+".mp3"                     | 同预览                                       |
| 资源路径 | path                                         | 同预览                                       |
