from pathlib import Path
from dataclasses import dataclass
from aoirint_id3 import detect_id3_versions, decode_id3v1_1
from aoirint_id3.id3v1_1 import available_genres
from typing import Optional

genre_dict = dict(map(lambda genre: (genre.genre_id, genre.genre_name), available_genres))


@dataclass
class MusicMetadata:
  name: Optional[str]
  artist: Optional[str]
  album: Optional[str]
  genre: Optional[str]
  year: Optional[str]


@dataclass
class Music:
  filename: str
  metadata: MusicMetadata
  duration_millis: int


@dataclass
class Playlist:
  filename: str
  musics: list[Music]


def load_music(music_file: Path) -> Music:
  music_bytes = music_file.read_bytes()

  name: Optional[str] = None
  artist: Optional[str] = None
  album: Optional[str] = None
  genre: Optional[str] = None
  year: Optional[str] = None

  id3_versions = detect_id3_versions(data=music_bytes)
  if 'ID3v1.1' in id3_versions:
    result = decode_id3v1_1(data=music_bytes[-128:], encoding='latin-1')
    name = result.title
    artist = result.artist
    album = result.album
    genre_number = result.genre_number
    genre = genre_dict.get(genre_number)
    year = result.year

  return Music(
    filename=music_file.name,
    metadata=MusicMetadata(
      name=name,
      artist=artist,
      album=album,
      genre=genre,
      year=year,
    ),
    duration_millis=0,
  )


def load_playlist(playlist_dir: Path) -> Playlist:
  music_files = list(filter(lambda path: path.is_file(), playlist_dir.iterdir()))

  musics: list[Music] = []
  for music_file in music_files:
    musics.append(load_music(music_file=music_file))
  
  return Playlist(
    filename=playlist_dir.name,
    musics=musics,
  )


def load_playlists(playlists_dir: Path) -> list[Playlist]:
  playlist_dirs = list(filter(lambda path: path.is_dir(), playlists_dir.iterdir()))

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

  print(
    load_playlists(
      playlists_dir=playlists_dir,
    )
  )


if __name__ == '__main__':
  main()
