from pathlib import Path
from dataclasses import dataclass


@dataclass
class MusicMetadata:
  name: str
  artist: str
  album: str
  genre: str
  year: str


@dataclass
class Music:
  filename: str
  metadata: MusicMetadata
  duration_millis: int


@dataclass
class Playlist:
  filename: str
  musics: list[Music]


def load_metadata(music_file: Path) -> MusicMetadata:
  raise Exception('Unimplemented')


def load_music(music_file: Path) -> Music:
  raise Exception('Unimplemented')


def load_playlist(playlist_dir: Path) -> Playlist:
  music_files = list(map(lambda path: path.is_file(), playlist_dir.iterdir()))

  musics = list[Music]
  for music_file in music_files:
    musics.append(load_music(music_file=music_file))
  
  return Playlist(
    filename=playlist_dir.name,
    musics=musics,
  )


def load_playlists(playlists_dir: Path) -> list[Playlist]:
  playlist_dirs = list(map(lambda path: path.is_dir(), playlists_dir.iterdir()))

  if len(playlist_dirs) == 0:
      default_playlist_dir = playlists_dir / 'default'
      default_playlist_dir.mkdir(parents=True, exist_ok=True)
      playlist_dirs.append(default_playlist_dir)

  playlists: list[Playlist] = []
  for playlist_dir in playlist_dirs:
    playlists.append(load_playlist(playlist_dir=playlist_dir))

  return playlists


def main():
  playlists_dir = Path('playlists')
  playlists_dir.mkdir(parents=True, exist_ok=True)

  load_playlists(
    playlists_dir=playlists_dir,
  )


if __name__ == '__main__':
  main()
