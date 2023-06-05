from googleapiclient.discovery import build

import os


class Video:
    """Класс для просмотра информации о видео"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        try:
            self.video_id = video_id
            self.video_inf = self.get_inf()
            self.video_name = self.get_inf()['items'][0]['snippet']['title']
            self.video_url = f'https://www.youtube.com/channel/{self.video_id}'
            self.video_view = self.get_inf()['items'][0]['statistics']['viewCount']
            self.video_like = self.get_inf()['items'][0]['statistics']['likeCount']

        except IdError:
            self.video_id = video_id
            self.video_inf = None
            self.video_name = None
            self.video_url = None
            self.video_view = None
            self.video_like = None
            print('Id неверен')

    def __str__(self):
        return self.video_name

    def get_inf(self):
        video_response = self.youtube.videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.video_id).execute()
        if len(video_response['items']) == 0:
            raise IdError
        else:
            return video_response


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id


class IdError(Exception):
    pass
