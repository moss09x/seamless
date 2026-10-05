import slint
import xdialog
import tinytag
import just_playback

from tinytag import TinyTag
from slint import Image
from tempfile import NamedTemporaryFile
from just_playback import Playback

class AppWindow(slint.loader.ui.app_window.AppWindow):
    active_song: Playback | None
    temp_cover_file: str | None
    
    def __init__(self):
        super().__init__()

        self.active_song = None
        self.temp_cover_file = None
    
    @slint.callback
    def open_song(self):
        file_path = xdialog.open_file(
            title = "Select a song",

            filetypes = [
                ("Audio Files", "*.mp3 *.flac *.ogg *.wav"),
            ]
        )

        if not file_path:
            return

        self.playing = False

        self.active_song = Playback(file_path)

        self.active_song.play()
        self.active_song.pause()

        tag = TinyTag.get(file_path, image = True)

        self.song = tag.title or ""
        self.artist = tag.artist or ""

        cover = tag.images.front_cover

        if cover and cover.data:
            suffix = ".jpg"
            if cover.mime_type and "png" in cover.mime_type:
                suffix = ".png"

            with NamedTemporaryFile(delete = False, suffix = suffix) as tmp:
                tmp.write(cover.data)
                self.temp_cover_file = tmp.name

            self.cover = Image.load_from_path(self.temp_cover_file)

    def background_open_song(self):
        file_path = xdialog.open_file(
            title = "Select a song",

            filetypes = [
                ("Audio Files", "*.mp3 *.flac *.ogg *.wav"),
            ]
        )

        if not file_path:
            return

        self.playing = False

        self.active_song = Playback(file_path)

        self.active_song.play()
        self.active_song.pause()

        tag = TinyTag.get(file_path, image = True)

        self.song = tag.title or ""
        self.artist = tag.artist or ""

        cover = tag.images.front_cover

        if cover and cover.data:
            suffix = ".jpg"
            if cover.mime_type and "png" in cover.mime_type:
                suffix = ".png"

            with NamedTemporaryFile(delete = False, suffix = suffix) as tmp:
                tmp.write(cover.data)
                self.temp_cover_file = tmp.name

            self.cover = Image.load_from_path(self.temp_cover_file)


    @slint.callback
    def toggle_playback(self):
        if not self.active_song:
            return

        self.playing = not self.playing

        if self.playing:
            self.active_song.resume()
        else:
            self.active_song.pause()

main_window = AppWindow()

main_window.show()
main_window.run()
