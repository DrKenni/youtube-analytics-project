from googleapiclient.discovery import build

import os
import json


class Channel:
    """Класс для ютуб-канала"""

    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
         Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.sub_count) + int(other.sub_count)

    def __sub__(self, other):
        return int(self.sub_count) - int(other.sub_count)

    def __lt__(self, other):
        return int(self.sub_count) < int(other.sub_count)

    def __le__(self, other):
        return int(self.sub_count) <= int(other.sub_count)

    def __gt__(self, other):
        return int(self.sub_count) > int(other.sub_count)

    def __ge__(self, other):
        return int(self.sub_count) >= int(other.sub_count)

    def __eq__(self, other):
        return int(self.sub_count) == int(other.sub_count)

    @property
    def channel(self):
        return self.youtube.channels()

    @property
    def title(self):
        """Возвращает название канала"""
        return self.print_info()['items'][0]['snippet']['title']

    @property
    def url(self):
        """Возвращает сылку на канал"""
        return f'https://www.youtube.com/channel/{self.__channel_id}'

    @property
    def video_count(self):
        """Возвращает колличество видео на канале"""
        return self.print_info()['items'][0]['statistics']['videoCount']

    @property
    def view_count(self):
        """Возвращает общее колличество просмотров канала"""
        return self.print_info()['items'][0]['statistics']['viewCount']

    @property
    def description(self):
        """Возвращает описание канала"""
        return self.print_info()['items'][0]['snippet']['description']

    @property
    def sub_count(self):
        """Возвращает колличество подписчиков канала"""
        return self.print_info()['items'][0]['statistics']['subscriberCount']

    def print_info(self) -> dict:
        """Выводит в консоль информацию о канале"""
        channel = self.channel.list(
            id=self.__channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, save_file_json):
        data = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subCount': self.sub_count,
            'videoCount': self. video_count,
            'viewCount': self.view_count
        }
        with open(save_file_json, 'w') as file:
            json.dump(data, file)
