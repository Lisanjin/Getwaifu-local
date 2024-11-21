# Getwaifu-local

这个项目是之前[GetWaifu](https://github.com/Lisanjin/GetWaifu)的本地版本，懒得说明了不懂就参考原来的项目

具体的输入路径参看lib下对应游戏的资源表,用记事本打开

| | |
|-|-|
deepone|download_res_hash.manifest
孤儿|resource.json
转职魔王 |config.json/names.json
白黑三国志|resource.json



先点预览才会能点下载

以下说明中path代表你输入框中的输入

DeepOne  

| 类型     | 预览内容                                        | 下载内容                                      |示例                      |
|----------|-------------------------------------------------|-----------------------------------------------|-----------------------------------------------|
| 卡面     | "character/"+path+"/image/main.png"             | 同预览                                        |character/**100105**/image/main.png                  |
| MEMORIAL | "character/"+path前四位+"/image/"+path+".png"   | 同预览                                        |character/6002/image/**600212**.png                   |
| 立绘     | "character/"+path+"/image/stand.png"            | 同预览                                        |character/**100105**/image/stand.png                  |
| 寝室预览 | "gallery/episode/"+path+".png"                  | 同预览                                        |gallery/episode/**10010505**.png                      |
| bgm      | "sound/bgm/"+path+".mp3"                        | 同预览                                        |sound/bgm/**bgm001**.mp3       sound/bgm/**ins_cha12**.mp3 |
| spine    | "character/"+path+"/spine/room/room.png"        | 全部以 "character/"+path+"/spine"开头内容    |character/**100105**/spine                              |
| specialRoom| "specialRoom/"+path+"/image/sp_room_list_A.png"|全部以 "specialRoom/"+path 开头内容          |specialRoom/**4037001**/                                |
| 资源路径 | path                                           | 同预览                                        | |

孤儿的工作

| 类型     | 预览内容                                     | 下载内容                                     |示例                      |
|----------|----------------------------------------------|----------------------------------------------|-----------------------------------------------|
| 角色卡面 | "image/character/stand/"+path+"01.png"       | 全部以 "image/character/stand/"+path开头内容 |image/character/stand/**100601**01.png                |
| 战神卡面 | "image/summon/stand/"+path+"01.png"          | 全部以 "image/summon/stand/"+path开头内容   |image/summon/stand/**300101**01.png                    |
| 寝室预览 | "image/episode/story/"+path+".png"           | 同预览                                       |image/episode/story/**110010101**.png                 |
| bgm      | "sound/bgm/"+path+".mp3"                     | 同预览                                       |sound/bgm/**bgm010**.mp3                           |
| spine    | "spine/summon/"+path+"/"+path+".png"        | 全部以 "spine/summon/"+path 开头内容         |spine/summon/**302701**/**302701**.png                     |
| 资源路径 | path                                         | 同预览                                       |                                                 |

转职魔王
| 类型     | 预览内容                                     | 下载内容                                     |示例                      |
|----------|----------------------------------------------|----------------------------------------------|-----------------------------------------------|
|text 、json|无                                            |path                                          |**adv11001_1.json**                                |
|audio      |path                                           |path                                          |**33001_E01AA007.mp3**                          |
|sprite     |path                                           |path、对应textureatlas.basis、对应textureatlas.png|**splash_logo_dmm.png**                        |
|texture、textureatlas|path                                 |path、对应.basis                                |**unit_enemy20000604.png**    |

白黑三国志
| 类型     | 预览内容                                     | 下载内容                                     |示例                      |
|----------|----------------------------------------------|----------------------------------------------|-----------------------------------------------|
|立绘       |"image/unit/character/st/c_st_"+path+"_00.png"|同预览                                      |image/unit/character/st/c_st_**1100100**_00.png|
|立绘大     |"image/unit/character/ff/c_ff_"+path+".png"    |同预览                                      |image/unit/character/ff/c_ff_**1100100**.png     |
|表情差分     |"image/unit/character/fc/c_fc_"+path+".png"    |同预览                                      |image/unit/character/fc/c_fc_**1100100**.png     |
|头像          |"image/unit/character/tm/c_tm_"+path+".png" |同预览                                      |image/unit/character/tm/c_tm_1100100.png          |
|bgm          |"sound/bgm/"+path+".m4a"                     |同预览                                      |sound/bgm/bgm_4010016.m4a                         |
|hs_anime      |"animation/h/"+path+"/h_"+path+"_001.jpg"   |所有"animation/h/"+path开头内容，不包含sp      |animation/h/**1100100_H01**/h_**1100100_H01**_128.jpg|
|hs_cg          |"image/cg/cg_"+path+"_01.jpg"              |所有"image/cg/cg_"+path开头内容                |image/cg/cg_**1100100_H01**_02.jpg             |
|hs_voice       |"sound/voice/"+path.split("_")[0]+"/voice_"+path+"_01.m4a"|所有"sound/voice/"+path.split("_")[0]+"/voice_"+path开头内容 |sound/voice/1100100/voice_**1100100_H01**_01.m4a|