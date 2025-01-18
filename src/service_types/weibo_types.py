""" 定义微博类型 """

from typing import TypedDict


class WeiboContainerCardListInfo(TypedDict):
    """ res.data.cardlistInfo """
    since_id: int


class WeiboContainerCardMblogTitle(TypedDict):
    """ res.data.cards.mblog.title """
    text: str # 置顶


class WeiboContainerCardMblogUser(TypedDict):
    """ res.data.cards.mblog.user """
    screen_name: str
    id: int
    avatar_hd: str


class WeiboContainerCardMblogPics(TypedDict):
    """ res.data.cards.mblog.pics """
    pid: str
    url: str


class WeiboContainerCardMblog(TypedDict):
    """ res.data.cards.mblog """
    region_name: str # 发布位置
    text: str
    id: str
    bid: str
    created_at: str # 样式为Wed Jan 08 18:01:41 +0800 2025
    edit_at: str
    title: WeiboContainerCardMblogTitle
    user: WeiboContainerCardMblogUser
    pic_ids: list[str]
    pics: list[WeiboContainerCardMblogPics]


class WeiboContainerCard(TypedDict):
    """ res.data.cards """
    card_type: int # 必须等于9
    itemid: str
    mblog: WeiboContainerCardMblog


class WeiboContainerData(TypedDict):
    """ res.data """
    cardlistInfo: WeiboContainerCardListInfo
    cards: list[WeiboContainerCard]


class WeiboContainerResponse(TypedDict):
    """ 微博返回的类型 """
    ok: int
    data: WeiboContainerData
