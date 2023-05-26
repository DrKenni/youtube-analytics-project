from googleapiclient.discovery import build
from datetime import timedelta

import isodate
import os


class PlayList:
    """Класс для просмотра информации по плейлисту"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.title = self.get_inf()['items'][0][
            'snippet']['localized']['title']
        self.playlist_videos = self.youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50).execute()
        self.video_ids = [video['contentDetails']['videoId']
                          for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(self.video_ids)).execute()

    def get_inf(self):
        playlist_videos = self.youtube.playlists().list(part='snippet',
                                                        id=self.playlist_id,
                                                        ).execute()
        return playlist_videos

    @property
    def total_duration(self):
        """Возвращает общее кол-во длительности видео в плейлисте"""
        result = timedelta()

        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            result += duration

        return result

    def show_best_video(self):
        """Возвращает самое популярное видео из плейлиста по кол-ву лайков"""
        best_like_video = 0

        for video in self.video_ids:
            reqest_vid = self.youtube.videos().list(
                part='statistics',
                id=video).execute()
            like_count = reqest_vid['items'][0]['statistics']['likeCount']

            if int(like_count) > best_like_video:
                best_like_video = int(like_count)
                best_url = f"https://youtu.be/{reqest_vid['items'][0]['id']}"

        return best_url
