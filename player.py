import sys, os, random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

music_list = []

class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setGeometry(450, 150, 480, 700)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ######### Progress Bar ###########
        self.progress_bar = QProgressBar()
        ########## Buttons ###############
        self.add_button = QToolButton()
        self.add_button.setIcon(QIcon("icons/add.png"))
        self.add_button.setIconSize(QSize(48, 48))
        self.add_button.setToolTip("Add a song")
        self.add_button.clicked.connect(self.add_song)

        self.shuffle_button = QToolButton()
        self.shuffle_button.setIcon(QIcon("icons/shuffle.png"))
        self.shuffle_button.setIconSize(QSize(48, 48))
        self.shuffle_button.setToolTip("Shuffle songs")
        self.shuffle_button.clicked.connect(self.shuffle_playlist)

        self.previous_button = QToolButton()
        self.previous_button.setIcon(QIcon("icons/previous.png"))
        self.previous_button.setIconSize(QSize(48, 48))
        self.previous_button.setToolTip("Play previous")

        self.play_button = QToolButton()
        self.play_button.setIcon(QIcon("icons/play.png"))
        self.play_button.setIconSize(QSize(64, 64))
        self.play_button.setToolTip("Play")


        self.next_button = QToolButton()
        self.next_button.setIcon(QIcon("icons/next.png"))
        self.next_button.setIconSize(QSize(48, 48))
        self.next_button.setToolTip("Play next")

        self.mute_button = QToolButton()
        self.mute_button.setIcon(QIcon("icons/mute.png"))
        self.mute_button.setIconSize(QSize(24, 24))
        self.mute_button.setToolTip("Mute")

        ########## Volume Slider ##########
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setToolTip("Volume")

        ########## Play List ##############
        self.play_list = QListWidget()


    def layouts(self):
        ########## Creating Layouts ##########
        self.main_layout = QVBoxLayout()
        self.top_main_layout = QVBoxLayout()
        self.top_group_box = QGroupBox("Music Player")
        self.top_group_box.setStyleSheet("background-color: #fcc324")
        self.top_layout = QHBoxLayout()  # For progress bar
        self.middle_layout = QHBoxLayout()  # For buttons
        self.bottom_layout = QVBoxLayout()

        ########## Adding Widgets ##############
        ########## Top Layout Widgets ##########
        self.top_layout.addWidget(self.progress_bar)

        ########## Middle Layout Widgets #######
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.add_button)
        self.middle_layout.addWidget(self.shuffle_button)
        self.middle_layout.addWidget(self.previous_button)
        self.middle_layout.addWidget(self.play_button)
        self.middle_layout.addWidget(self.next_button)
        self.middle_layout.addWidget(self.volume_slider)
        self.middle_layout.addWidget(self.mute_button)
        self.middle_layout.addStretch()

        ########## Bottom Layout Widgets #######
        self.bottom_layout.addWidget(self.play_list)

        self.top_main_layout.addLayout(self.top_layout)
        self.top_main_layout.addLayout(self.middle_layout)
        self.top_group_box.setLayout(self.top_main_layout)
        self.main_layout.addWidget(self.top_group_box, 25)
        self.main_layout.addLayout(self.bottom_layout, 75)
        self.setLayout(self.main_layout)

    def add_song(self):
        directory = QFileDialog.getOpenFileName(self, "Add Song", "")#(*.mp3 *.ogg *.wav)
        filename = os.path.basename(directory[0])
        self.play_list.addItem(filename)
        music_list.append(directory[0])

    def shuffle_playlist(self):
        random.shuffle(music_list)
        self.play_list.clear()
        for song in music_list:
            filename = os.path.basename(song)
            self.play_list.addItem(filename)

def main():
    App = QApplication(sys.argv)
    window = Player()
    sys.exit(App.exec_())

if __name__ =="__main__":
    main()
