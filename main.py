from PyQt6.QtWidgets import QApplication,QWidget,QDialog,QLabel,QVBoxLayout,QMainWindow,QPushButton,QMessageBox
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtCore import QByteArray
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import QThread, pyqtSignal

import time
import sys,os,requests
import concurrent.futures
import threading
from functools import partial

from ui.main_window import Ui_MainWindow

from ui.game_detail_deepone import Ui_game_detail_deepone
from ui.game_detail_minashigo import Ui_game_detail_minashigo
from ui.game_detail_tenshoku_maou import Ui_game_detail_tenshoku_maou

from ui.review_widget import Ui_review_widget
from ui.audio_review_label import Ui_audio_review_label

from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput

from lib.deepone import deepone
from lib.minashigo import minashigo
from lib.tenshoku_maou import tenshoku_maou

from qt_material import apply_stylesheet

class UpdataResourceThread(QThread):
    # 创建一个信号，通知主线程下载完成
    updata_finished = pyqtSignal(str)

    def __init__(self, utils, game_detail,parent=None):
        super().__init__(parent)
        self.utils = utils
        self.game_detail = game_detail

    def run(self):
        try:
            if self.utils.updata_master():
                
                self.game_detail.resouce_version.setText("资源表版本:" + self.utils.get_meta()["version"])
                self.game_detail.update_time.setText("上次更新时间:" + self.utils.get_meta()["update_time"])
            else:
                pass

            self.updata_finished.emit("更新完成")

        except Exception as e:
            print(e)

class DownloadThread(QThread):
    download_finished = pyqtSignal(str)

    def __init__(self, resouce_dict, selected_game, parent=None):
        super().__init__(parent)
        self.resouce_dict = resouce_dict
        self.selected_game = selected_game

    def run(self):
        try:
            file_dict = {}
            for r in self.resouce_dict['resource_list']:
                for k, v in r.items():
                    file_dict[v] = "resource/" + self.selected_game + "/" + k

            def dl_file(url, file_name):
                print(f"downloading:{file_name}")
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        directory = file_name.replace(file_name.split('/')[-1], '')
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        with open(file_name, 'wb') as file:
                            file.write(response.content)
                            print(f"{file_name}下载成功")
                    else:
                        print(f"{file_name}下载失败")
                except:
                    print(f"{file_name}下载失败")

            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(dl_file, url, filename) for url, filename in file_dict.items()]

                # 使用as_completed来等待下载完成
                for future in concurrent.futures.as_completed(futures):
                    pass
            # 所有下载任务完成后，发出信号通知主线程
            self.download_finished.emit("所有下载任务已完成！")

        except Exception as e:
            print(e)

class AutoCloseMessageBox():

    @classmethod
    def show_information(self, text, timeout=2000):
        dialog = QDialog()
        dialog.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # 隐藏标题栏
        layout = QVBoxLayout(dialog)
        label = QLabel(text)
        layout.addWidget(label)

        QTimer.singleShot(timeout, dialog.close)

        dialog.exec()
    

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.GAME_LIST = ["deepone","minashigo","tenshoku_maou"]
        self.setupUi(self)
        self.initUI()
        

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        
        self.initUI_game_button()
        self.initUI_game_detail_deepone_widget()
        self.initUI_game_detail_minashigo_widget()
        self.initUI_game_detail_tenshoku_maou_widget()

        self.initUI_review_widget()
        self.initUI_audio_review_label()

        self.selected_game = "deepone"
        self.show_game_detail(self.selected_game)

        self.review_image(open('./images/images/180404.png', 'rb').read())
            

    def initUI_review_widget(self):
        self.review_widget = QWidget(self)  # 创建 QWidget 容器
        self.ui_review_widget = Ui_review_widget()   # 创建 Ui_game_detail 实例
        self.ui_review_widget.setupUi(self.review_widget)
        
        self.review_widget.move(60, 0)

    def initUI_audio_review_label(self):
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput() 
        self.media_player.setAudioOutput(self.audio_output)

        self.audio_review_label = QWidget(self)  # 创建 QWidget 容器
        self.ui_audio_review_label = Ui_audio_review_label()   # 创建 Ui_game_detail 实例
        self.ui_audio_review_label.setupUi(self.audio_review_label)

        self.ui_audio_review_label.audio_stop_button.setIcon(QIcon("./images/icons/cil-media-stop.png"))
        self.ui_audio_review_label.audio_pause_button.setIcon(QIcon("./images/icons/cil-media-pause.png"))
        self.ui_audio_review_label.audio_play_button.setIcon(QIcon("./images/icons/cil-media-play.png"))

        self.ui_audio_review_label.audio_stop_button.clicked.connect(self.media_player.stop)
        self.ui_audio_review_label.audio_pause_button.clicked.connect(self.media_player.pause)
        self.ui_audio_review_label.audio_play_button.clicked.connect(self.media_player.play)

        self.audio_review_label.move(350, 260)

        self.audio_review_label.hide()

    def initUI_game_button(self):
        self.menu_button.setIcon(QIcon('images/icons/cil-power-standby.png'))
        self.menu_button.setIconSize(QSize(50 , 50))
        self.menu_button.clicked.connect(QApplication.quit)

        for game in self.GAME_LIST:

            game_button = self.findChild(QPushButton, game + "_button")

            if game_button:
                game_button.setIcon(QIcon('images/game_icon/game_ico_' + game + ".png"))
                game_button.setIconSize(QSize(50, 50))
                
                game_button.clicked.connect(partial(self.show_game_detail, game))
                if game_button.property("is_selected"):
                    game_button.setStyleSheet("border: 2px solid #1de9b6;")
                else:
                    game_button.setStyleSheet("border: none;")

    
    def initUI_game_detail_deepone_widget(self):
        self.game_detail_deepone_widget = QWidget(self)  # 创建 QWidget 容器
        self.ui_game_detail_deepone= Ui_game_detail_deepone()   # 创建 Ui_game_detail 实例
        self.ui_game_detail_deepone.setupUi(self.game_detail_deepone_widget)

        self.deepone_utils = deepone.Deepone_Utils()

        self.ui_game_detail_deepone.resouce_version.setText("资源表版本："+self.deepone_utils.get_meta()["version"])
        self.ui_game_detail_deepone.update_time.setText("上次更新时间："+self.deepone_utils.get_meta()["update_time"])

        self.game_detail_deepone_widget.move(1280, 0)

        self.ui_game_detail_deepone.comboBox.addItems(['卡面', 'MEMORIAL', '立绘',"寝室预览","BGM","spine","资源路径"])
        
        self.ui_game_detail_deepone.review_button.clicked.connect(self.review_deepone)
        self.ui_game_detail_deepone.download_button.clicked.connect(self.download)
        self.ui_game_detail_deepone.updateRes.clicked.connect(lambda: self.update_resource(self.deepone_utils,self.ui_game_detail_deepone))
    
    def initUI_game_detail_minashigo_widget(self):
        self.game_detail_minashigo_widget = QWidget(self)  # 创建 QWidget 容器
        self.ui_game_detail_minashigo = Ui_game_detail_minashigo()   # 创建 Ui_game_detail 实例
        self.ui_game_detail_minashigo.setupUi(self.game_detail_minashigo_widget)

        self.minashigo_utils = minashigo.Minashigo_Utils()

        self.ui_game_detail_minashigo.resouce_version.setText("资源表版本：" + self.minashigo_utils.get_meta()["version"])
        self.ui_game_detail_minashigo.update_time.setText("上次更新时间：" + self.minashigo_utils.get_meta()["update_time"])

        self.game_detail_minashigo_widget.move(1280, 0)

        self.ui_game_detail_minashigo.comboBox.addItems(['角色卡面', '战神卡面', "寝室预览","BGM","资源路径"])
        
        self.ui_game_detail_minashigo.review_button.clicked.connect(self.review_minashigo)
        self.ui_game_detail_minashigo.download_button.clicked.connect(self.download)
        self.ui_game_detail_minashigo.updateRes.clicked.connect(lambda: self.update_resource(self.minashigo_utils,self.ui_game_detail_minashigo))

    def initUI_game_detail_tenshoku_maou_widget(self):
        self.game_detail_tenshoku_maou_widget = QWidget(self)  # 创建 QWidget 容器
        self.ui_game_detail_tenshoku_maou = Ui_game_detail_tenshoku_maou()   # 创建 Ui_game_detail 实例
        self.ui_game_detail_tenshoku_maou.setupUi(self.game_detail_tenshoku_maou_widget)

        self.tenshoku_maou_utils = tenshoku_maou.Tenshoku_Maou_Utils()

        self.ui_game_detail_tenshoku_maou.resouce_version.setText("资源表版本：" + self.tenshoku_maou_utils.get_meta()["version"])
        self.ui_game_detail_tenshoku_maou.update_time.setText("上次更新时间：" + self.tenshoku_maou_utils.get_meta()["update_time"])

        self.game_detail_tenshoku_maou_widget.move(1280, 0)

        self.ui_game_detail_tenshoku_maou.comboBox.addItems(["text", "json", "sprite", "texture", "audio", "textureatlas"])

        self.ui_game_detail_tenshoku_maou.review_button.clicked.connect(self.review_tenshoku_maou)
        self.ui_game_detail_tenshoku_maou.updateRes.clicked.connect(lambda: self.update_resource(self.tenshoku_maou_utils,self.ui_game_detail_tenshoku_maou))


    def show_game_detail(self,game_name):

        for game in self.GAME_LIST:
            if game == game_name:
                self.selected_game = game
                selected_game_widget = self.findChild(QWidget, "game_detail_"+game_name)
                selected_game_button = self.findChild(QPushButton, game_name+"_button")
                x = selected_game_widget.pos().x()
                if x == 1280:
                    selected_game_widget.move(1040, 0)
                    selected_game_widget.show()
                    selected_game_button.setStyleSheet("border: 2px solid #1de9b6;")
                    selected_game_button.setProperty("is_selected", True)
                else:
                    selected_game_widget.move(1280, 0)
                    selected_game_widget.hide()
                    selected_game_button.setStyleSheet("border: none;")
                    selected_game_button.setProperty("is_selected", False)
            else:
                unselected_game_widget = self.findChild(QWidget, "game_detail_"+game)
                unselected_game_widget.move(1280, 0)
                unselected_game_widget.hide()

                unselected_game_button = self.findChild(QPushButton, game+"_button")
                unselected_game_button.setStyleSheet("border: none;")
                unselected_game_button.setProperty("is_selected", False)


    def update_resource(self,utils,game_detail):
        update_thread = UpdataResourceThread(utils,game_detail)


        update_thread.start()

        update_thread.updata_finished.connect(self.show_download_complete_message)

        update_thread.finished.connect(update_thread.quit)
        update_thread.finished.connect(update_thread.wait)

    
    def review_deepone(self):
        try:
            resouce_type = self.ui_game_detail_deepone.comboBox.currentText()
            resouce_path = self.ui_game_detail_deepone.textEdit.toPlainText()

            self.resouce_dict = self.deepone_utils.get_resource(resouce_type,resouce_path)

            content = self.deepone_utils.download_single_file(self.resouce_dict['resource_url'])

            if resouce_type == "BGM":
                self.review_audio(content)
            elif resouce_type == "立绘" or resouce_type == "卡面" or resouce_type == "MEMORIAL" or resouce_type == "寝室预览":
                self.review_image(content)
            elif resouce_type == "spine":
                self.review_image(content)
            elif resouce_type == "资源路径":
                if resouce_path.endswith(".mp3"):
                    self.review_audio(content)
                elif resouce_path.endswith(".png") or resouce_path.endswith(".jpg"):
                    self.review_image(content)
                else:
                    pass
            else:
                pass
        except Exception as e:
            print(e)
    
    def review_minashigo(self):
        try:
            resouce_type = self.ui_game_detail_minashigo.comboBox.currentText()
            resouce_path = self.ui_game_detail_minashigo.textEdit.toPlainText()

            self.resouce_dict = self.minashigo_utils.get_resource(resouce_type,resouce_path)

            content = self.minashigo_utils.download_single_file(self.resouce_dict['resource_url'])

            if resouce_type == "角色卡面":
                self.review_image(content)
            elif resouce_type == "战神卡面":
                self.review_image(content)
            elif resouce_type == "寝室预览":
                self.review_image(content)
            elif resouce_type == "BGM":
                self.review_audio(content)
            elif resouce_type == "资源路径":
                if resouce_path.endswith(".png") or resouce_path.endswith(".jpg"):
                    self.review_image(content)
                elif resouce_path.endswith(".mp3"):
                    self.review_audio(content)
                else:
                    pass
            else:
                pass
        except Exception as e:
            print(e)

    def review_tenshoku_maou(self):
        try:
            resouce_type = self.ui_game_detail_tenshoku_maou.comboBox.currentText()
            resouce_path = self.ui_game_detail_tenshoku_maou.textEdit.toPlainText()

            self.resouce_dict = self.tenshoku_maou_utils.get_resource(resouce_type,resouce_path)

            content = self.resouce_dict['content']

            if content:
                AutoCloseMessageBox.show_information("保存至："+self.resouce_dict['file_name'])

            if resouce_type in ["sprite", "texture",  "textureatlas"]:
                self.review_image(content)
            elif resouce_type == "audio":
                self.review_audio(content)

        except Exception as e:
            print(e)


    def download(self):
        if len(self.resouce_dict['resource_list']) == 1:
            file_name = list(self.resouce_dict['resource_list'][0].keys())[0]
            AutoCloseMessageBox.show_information(f"下载开始:resource/{self.selected_game}/{file_name}")
        else:
            AutoCloseMessageBox.show_information("开始批量下载，任务数："+str(len(self.resouce_dict['resource_list'])))

        download_thread = DownloadThread(self.resouce_dict, self.selected_game)
        download_thread.download_finished.connect(self.show_download_complete_message)
        download_thread.start()

        download_thread.finished.connect(download_thread.quit)
        download_thread.finished.connect(download_thread.wait)

    def show_download_complete_message(self):
        AutoCloseMessageBox.show_information("下载完成")


    def close_review(self):
        self.media_player.stop()
        self.media_player.setSource(QUrl())
        self.audio_review_label.hide()

        self.review_widget.hide()
        self.ui_review_widget.image_review_label.clear()

    def review_audio(self,content):
        print("review_audio")
        self.close_review()
        self.audio_review_label.show()

        with open("./tmp/temp", 'wb') as file:
            file.write(content)

        path = os.getcwd() 
        qurl = QUrl.fromLocalFile(path+"./tmp/temp")
        self.media_player.setSource(qurl)      

        self.media_player.play()

    def review_image(self,content):
        self.close_review()
        self.review_widget.show()

        byte_array = QByteArray(content)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)

        image_width = pixmap.width()
        image_height = pixmap.height()

        # 计算缩放比例，保持图片原比例
        label_width = self.ui_review_widget.image_review_label.width()
        label_height = self.ui_review_widget.image_review_label.height()
        scale_factor = min(label_width / image_width, label_height / image_height)

        # 计算缩放后的尺寸
        new_width = int(image_width * scale_factor)
        new_height = int(image_height * scale_factor)
        
        pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)


        self.ui_review_widget.image_review_label.setPixmap(pixmap)

        self.ui_review_widget.image_review_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui_review_widget.image_review_label.setScaledContents(False)

    
        
if __name__ == '__main__':

    app = QApplication(sys.argv)

    apply_stylesheet(app, theme='dark_teal.xml')

    window = MainWindow()

    window.show()

    sys.exit(app.exec())

# nuitka --mingw64 --standalone --onefile --show-progress --plugin-enable=pyqt6 --include-package-data=qt_material --include-qt-plugins=multimedia --windows-icon-from-ico=furau.ico --output-filename=GetWaifu.exe main.py