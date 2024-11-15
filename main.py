from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QMainWindow,QPushButton,QMessageBox
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtCore import QByteArray
from PyQt6.QtCore import QUrl

from PyQt6 import uic
import sys,os,requests
import concurrent.futures
import threading

from ui.main_window import Ui_MainWindow
from ui.game_detail_deepone import Ui_game_detail_deepone
from ui.game_detail_minashigo import Ui_game_detail_minashigo
from ui.review_widget import Ui_review_widget
from ui.aduio_review_label import Ui_aduio_review_label

from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput

from lib.deepone import deepone
from lib.minashigo import minashigo

from qt_material import apply_stylesheet

GAME_LIST = ["deepone","minashigo"]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        
        self.initUI_game_button()
        self.initUI_game_detail_deepone_widget()
        self.initUI_game_detail_minashigo_widget()
        self.initUI_review_widget()
        self.initUI_aduio_review_label()

        self.selected_game = "deepone"
        self.show_game_detail(self.selected_game)

        self.review_image(open('./images/images/180404.png', 'rb').read())
            

    def initUI_review_widget(self):
        self.review_widget = QWidget(self)  # 创建 QWidget 容器
        self.ui_review_widget = Ui_review_widget()   # 创建 Ui_game_detail 实例
        self.ui_review_widget.setupUi(self.review_widget)
        
        self.review_widget.move(60, 0)

    def initUI_aduio_review_label(self):
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput() 
        self.media_player.setAudioOutput(self.audio_output)

        self.aduio_review_label = QWidget(self)  # 创建 QWidget 容器
        self.ui_aduio_review_label = Ui_aduio_review_label()   # 创建 Ui_game_detail 实例
        self.ui_aduio_review_label.setupUi(self.aduio_review_label)

        self.ui_aduio_review_label.aduio_stop_button.setIcon(QIcon("./images/icons/cil-media-stop.png"))
        self.ui_aduio_review_label.aduio_pause_button.setIcon(QIcon("./images/icons/cil-media-pause.png"))
        self.ui_aduio_review_label.aduio_play_button.setIcon(QIcon("./images/icons/cil-media-play.png"))

        self.ui_aduio_review_label.aduio_stop_button.clicked.connect(self.media_player.stop)
        self.ui_aduio_review_label.aduio_pause_button.clicked.connect(self.media_player.pause)
        self.ui_aduio_review_label.aduio_play_button.clicked.connect(self.media_player.play)

        self.aduio_review_label.move(350, 260)

        self.aduio_review_label.hide()

    def initUI_game_button(self):
        # for game in GAME_LIST:
        #     print(game)
        #     game_button = self.findChild(QPushButton, game+"_button")
        #     game_button.setIcon(QIcon('images/icons/game_ico_'+game+".png"))
        #     game_button.setIconSize(game_button.size())
        #     game_button.clicked.connect(lambda: self.show_game_detail(game))
        self.menu_button.setIcon(QIcon('images/icons/cil-power-standby.png'))
        self.menu_button.setIconSize(QSize(50 , 50))
        self.menu_button.clicked.connect(QApplication.quit)

        self.deepone_button.setIcon(QIcon('images/icons/game_ico_deepone.png'))
        self.deepone_button.setIconSize(QSize(50 , 50))
        self.deepone_button.clicked.connect(lambda: self.show_game_detail("deepone"))
        if self.deepone_button.property("is_selected"):
            self.deepone_button.setStyleSheet("border: 2px solid #1de9b6;")
        else:
            self.deepone_button.setStyleSheet("border: none;")

        self.minashigo_button.setIcon(QIcon('images/icons/game_ico_minashigo.png'))
        self.minashigo_button.setIconSize(QSize(50 , 50))
        self.minashigo_button.clicked.connect(lambda: self.show_game_detail("minashigo"))
        if self.minashigo_button.property("is_selected"):
            self.minashigo_button.setStyleSheet("border: 2px solid #1de9b6;")
        else:
            self.minashigo_button.setStyleSheet("border: none;")

    
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
        self.ui_game_detail_deepone.updateRes.clicked.connect(self.update_deepone_resource)
    
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
        self.ui_game_detail_minashigo.updateRes.clicked.connect(self.update_minashigo_resource)


    def show_game_detail(self,game_name):

        for game in GAME_LIST:
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

    
    def update_deepone_resource(self):
        if self.deepone_utils.updata_master():
            QMessageBox.information(self, "提示", "更新成功")
            self.ui_game_detail_deepone.resouce_version.setText("资源表版本："+self.deepone_utils.get_meta()["version"])
            self.ui_game_detail_deepone.update_time.setText("上次更新时间："+self.deepone_utils.get_meta()["update_time"])
        else:
            QMessageBox.information(self, "提示", "更新失败")
    
    def update_minashigo_resource(self):
        if self.minashigo_utils.updata_master():
            QMessageBox.information(self, "提示", "更新成功")
            self.ui_game_detail_minashigo.resouce_version.setText("资源表版本:" + self.minashigo_utils.get_meta()["version"])
            self.ui_game_detail_minashigo.update_time.setText("上次更新时间:" + self.minashigo_utils.get_meta()["update_time"])
        else:
            QMessageBox.information(self, "提示", "更新失败")

    def review_deepone(self):
        try:
            resouce_type = self.ui_game_detail_deepone.comboBox.currentText()
            resouce_path = self.ui_game_detail_deepone.textEdit.toPlainText()

            self.resouce_dict = self.deepone_utils.get_resource(resouce_type,resouce_path)

            content = self.deepone_utils.download_single_file(self.resouce_dict['resource_url'])
            # content = None

            if resouce_type == "BGM":
                self.review_aduio(content)
            elif resouce_type == "立绘" or resouce_type == "卡面" or resouce_type == "MEMORIAL" or resouce_type == "寝室预览":
                self.review_image(content)
            elif resouce_type == "spine":
                self.review_image(content)
            elif resouce_type == "资源路径":
                if resouce_path.endswith(".mp3"):
                    self.review_aduio(content)
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
            # content = None

            if resouce_type == "角色卡面":
                self.review_image(content)
            elif resouce_type == "战神卡面":
                self.review_image(content)
            elif resouce_type == "寝室预览":
                self.review_image(content)
            elif resouce_type == "BGM":
                self.review_aduio(content)
            elif resouce_type == "资源路径":
                if resouce_path.endswith(".png") or resouce_path.endswith(".jpg"):
                    self.review_image(content)
                elif resouce_path.endswith(".mp3"):
                    self.review_aduio(content)
                else:
                    pass
            else:
                pass
        except Exception as e:
            print(e)

    def download(self):
        # resouce_type = self.ui_game_detail_deepone.comboBox.currentText()
        # resouce_path = self.ui_game_detail_deepone.textEdit.toPlainText()

        # self.resouce_dict = self.deepone_utils.get_resource(resouce_type,resouce_path)

        download_thread = threading.Thread(target=self.download_thread)
        download_thread.start()

    def download_thread(self):
        
        try:
            file_dict = {}
            for r in self.resouce_dict['resource_list']:
                for k,v in r.items():
                    file_dict[v] = "resource/"+self.selected_game+"/"+k


            def dl_file(url,file_name):
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
        except Exception as e:
            print(e)


    def close_review(self):
        self.media_player.stop()
        self.aduio_review_label.hide()
        self.review_widget.hide()
        self.ui_review_widget.image_review_label.clear()

    def review_aduio(self,content):
        print("review_aduio")
        self.close_review()
        self.aduio_review_label.show()

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