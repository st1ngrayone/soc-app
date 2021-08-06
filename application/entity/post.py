from typing import Optional
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from json import JSONDecoder, JSONEncoder

FORMAT = "%m-%d-%y %H:%M:%S"


class PostEncoder(JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Post):
            _dict = {
                "id": obj.id,
                "name": obj.name,
                "lastname": obj.lastname,
                "body": obj.body,
                "title": obj.title,
                "likes": obj.likes,
                "user_id": obj.user_id,
                "dislikes": obj.dislikes,
                "account_id_fk": obj.account_id_fk,
                "followers_count": obj.followers_count,
                "created_at": obj.created_at.strftime(FORMAT)
            }
            return _dict

        if isinstance(obj, Decimal):
            return str(obj)


class PostDecoder(JSONDecoder):

    def __init__(self):
        JSONDecoder.__init__(
            self,
            object_hook=self.dict_to_object,
        )

    def dict_to_object(self, _dict):
        _dict['created_at'] = datetime.strptime(_dict.get('created_at'), FORMAT)
        _dict['likes'] = Decimal(_dict.get('likes'))
        _dict['dislikes'] = Decimal(_dict.get('dislikes'))
        _dict['followers_count'] = Decimal(_dict.get('followers_count'))
        return _dict


@dataclass
class Post:
    user_id: int
    name: str
    lastname: str
    title: str
    body: str
    created_at: datetime
    id: Optional[int] = None
    account_id_fk: Optional[int] = None
    likes: Optional[Decimal] = 0
    dislikes: Optional[Decimal] = 0
    followers_count: Optional[Decimal] = 0
