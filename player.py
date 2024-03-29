import sys, os, random, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QTimer
from pygame import mixer
from mutagen.mp3 import MP3
import style

music_list = []
mixer.init()
muted = False
count = 0
song_length = 0
index = 0


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
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(style.progressbar_style())

        ########## Labels ################
        self.song_timer_label = QLabel("0:00")
        self.song_length_label = QLabel("/ 0:00")

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
        self.previous_button.clicked.connect(self.play_previous)

        self.play_button = QToolButton()
        self.play_button.setIcon(QIcon("icons/play.png"))
        self.play_button.setIconSize(QSize(64, 64))
        self.play_button.setToolTip("Play")
        self.play_button.clicked.connect(self.play_songs)

        self.next_button = QToolButton()
        self.next_button.setIcon(QIcon("icons/next.png"))
        self.next_button.setIconSize(QSize(48, 48))
        self.next_button.setToolTip("Play next")
        self.next_button.clicked.connect(self.play_next)

        self.mute_button = QToolButton()
        self.mute_button.setIcon(QIcon("icons/mute.png"))
        self.mute_button.setIconSize(QSize(24, 24))
        self.mute_button.setToolTip("Mute")
        self.mute_button.clicked.connect(self.mute_volume)

        ########## Volume Slider ##########
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setToolTip("Volume")
        self.volume_slider.setValue(70)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        mixer.music.set_volume(0.7)  # Set volume
        self.volume_slider.valueChanged.connect(self.change_volume)

        ########## Play List ##############
        self.play_list = QListWidget()
        self.play_list.doubleClicked.connect(self.play_songs)
        self.play_list.setStyleSheet(style.play_list_style())

        ########## Timer ##################
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_progressbar)

    def layouts(self):
        ########## Creating Layouts ##########
        self.main_layout = QVBoxLayout()
        self.top_main_layout = QVBoxLayout()
        self.top_group_box = QGroupBox()
        self.top_group_box.setStyleSheet(style.groupbox_style())
        self.top_layout = QHBoxLayout()  # For progress bar
        self.middle_layout = QHBoxLayout()  # For buttons
        self.bottom_layout = QVBoxLayout()

        ########## Adding Widgets ##############
        ########## Top Layout Widgets ##########
        self.top_layout.addWidget(self.progress_bar)
        self.top_layout.addWidget(self.song_timer_label)
        self.top_layout.addWidget(self.song_length_label)

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

    def play_songs(self):
        global song_length
        global count
        global index
        count = 0
        index = self.play_list.currentRow()
        try:
            mixer.music.load(str(music_list[index]))
            mixer.music.play()
            self.timer.start()
            song = MP3(str(music_list[index]))
            song_length = song.info.length
            song_length = round(song_length)
            min, sec = divmod(song_length, 60)
            self.song_length_label.setText("/ " + str(min) + ":" + str(sec))
            self.progress_bar.setValue(0)
            self.progress_bar.setMaximum(song_length)
        except:
            pass

    def play_previous(self):
        global song_length
        global count
        global index
        count = 0
        num_songs = self.play_list.count()
        if index == 0:
            index = num_songs
        index -= 1

        try:
            mixer.music.load(str(music_list[index]))
            mixer.music.play()
            self.timer.start()
            song = MP3(str(music_list[index]))
            song_length = song.info.length
            song_length = round(song_length)
            min, sec = divmod(song_length, 60)
            self.song_length_label.setText("/ " + str(min) + ":" + str(sec))
            self.progress_bar.setValue(0)
            self.progress_bar.setMaximum(song_length)
        except:
            pass

    def play_next(self):
        global song_length
        global count
        global index
        count = 0
        num_songs = self.play_list.count()
        index += 1
        if index == num_songs:
            index = 0

        try:
            mixer.music.load(str(music_list[index]))
            mixer.music.play()
            self.timer.start()
            song = MP3(str(music_list[index]))
            song_length = song.info.length
            song_length = round(song_length)
            min, sec = divmod(song_length, 60)
            self.song_length_label.setText("/ " + str(min) + ":" + str(sec))
            self.progress_bar.setValue(0)
            self.progress_bar.setMaximum(song_length)
        except:
            pass

    def change_volume(self):
        volume = self.volume_slider.value()
        mixer.music.set_volume(volume / 100)

    def mute_volume(self):
        global muted
        if not muted:
            mixer.music.set_volume(0.0)
            muted = True
            self.mute_button.setIcon(QIcon("icons/unmuted.png"))
            self.mute_button.setToolTip("Unmute")
            self.volume_slider.setValue(0)
        else:
            mixer.music.set_volume(0.7)
            muted = False
            self.mute_button.setIcon(QIcon("icons/mute.png"))
            self.mute_button.setToolTip("Mute")
            self.volume_slider.setValue(70)

    def update_progressbar(self):
        global count
        global song_length
        count += 1
        self.progress_bar.setValue(count)
        self.song_timer_label.setText(time.strftime("%M:%S", time.gmtime(count)))
        if count == song_length:
            self.timer.stop()


def main():
    App = QApplication(sys.argv)
    window = Player()
    sys.exit(App.exec_())


if __name__ =="__main__":
    main()
