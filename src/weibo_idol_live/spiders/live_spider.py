""" 抓取演出信息 """

from typing import Any, TypedDict, Iterable
from re import compile as re_compile, sub as re_sub, Pattern
from json import loads as json_loads, dumps as json_dumps
from scrapy import Spider
from scrapy.http import Request, Response
from utils.times import convert_to_timestamp, get_one_month_ago_timestamp
from utils.list_func import list_some, list_every
from utils.spider_config import SpiderConfigDict
from models.weibo_spider import WeiboSpiderConnect, WeiboSpiderModel
from service_types.weibo_types import WeiboContainerResponse, WeiboContainerCard, WeiboContainerCardMblog
from weibo_idol_live.items import WeiboIdolAddLiveItem, WeiboIdolUpdateLiveItem


class FilterCardsDict(TypedDict):
    """ filter_weibo_cards返回的值 """
    filter_cards: list[WeiboContainerCard]
    need_next: bool


# 演出关键词
performance_keywords_dict: list[list[str]] = [
    ['日期', '时间', '⏰', '开场', '🕐', 'time', '🕖', '📅', '⌛️', 'start'],
    ['地点', '地址', '入场', '📍', 'add', '🏤', '票务', '会场', '🎫'],
    ['嘉宾', '团体', '团队', '阵容', 'group', '成员', '嘉賓'],
]


class LiveSpider(Spider):
    name = 'live_spider'
    basic_url: str = 'https://m.weibo.cn/api/container/getIndex?containerid={}'
    desc_url: str = 'https://m.weibo.cn/detail/{}'
    live_spider_config: list[SpiderConfigDict] = []
    user_agent: str = ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/131.0.0.0 Mobile Safari/537.36')
    full_text_start_regexp: Pattern = re_compile(r'^ +"text": "')
    full_text_end_regexp: Pattern = re_compile(r'",$')

    def start_requests(self) -> Iterable:
        """ 开始请求 """
        for config in self.live_spider_config:
            self.logger.info('开始抓取UID：{}的信息'.format(config['uid']))
            req_url: str = self.basic_url.format(config['lfid'])
            yield Request(url=req_url, headers={
                'Referer': 'https://m.weibo.cn/u/{}'.format(config['uid']),
                'User-Agent': self.user_agent,
            }, callback=self.parse, meta={'config': config})

    def parse(self, response: Response, **kwargs: Any) -> Iterable:
        """ 解析 """
        json_result: WeiboContainerResponse = json_loads(response.text)
        config: SpiderConfigDict = response.meta['config']
        if not ('data' in json_result and 'cards' in json_result['data'] and len(json_result['data']['cards']) > 0):
            return
        # 过滤非微博发送的开篇
        filter_cards_dict: FilterCardsDict = self.filter_weibo_cards(json_result['data']['cards'])
        filter_cards: list[WeiboContainerCard] = filter_cards_dict.get('filter_cards', [])
        need_next: bool = filter_cards_dict.get('need_next', False)
        since_id: int = json_result['data']['cardlistInfo']['since_id']
        # 判断数据是否是地偶活动
        for card in filter_cards:
            if not self.determine_live_msg(card['mblog']['text']):
                continue
            # 检查微博是否有变化
            for p in self.parse_one_card(card, config):
                yield p
        # 查询下一页
        if need_next is True and since_id:
            req_url: str = self.basic_url.format(config['lfid']) + '&since_id={}'.format(since_id)
            yield Request(url=req_url, headers={
                'Referer': 'https://m.weibo.cn/u/{}'.format(config['uid']),
                'User-Agent': self.user_agent,
            }, callback=self.parse, meta={'config': config})

    def parse_one_card(self, card: WeiboContainerCard, config: SpiderConfigDict) -> Iterable:
        """ 解析单个card """
        db_result: WeiboSpiderModel | None = WeiboSpiderConnect.query_one(card['mblog']['bid'])
        created_at: int = convert_to_timestamp(card['mblog']['created_at'])
        edit_at: int | None = convert_to_timestamp(card['mblog']['edit_at']) if 'edit_at' in card['mblog'] else None
        if db_result:
            if not (created_at == db_result.created_at and edit_at == db_result.edit_at):
                # 有数据，需要更新
                update_item: WeiboIdolUpdateLiveItem = WeiboIdolUpdateLiveItem(bid=card['mblog']['bid'], payload={
                    'screen_name': card['mblog']['user']['screen_name'],
                    'avatar_hd': card['mblog']['user']['avatar_hd'],
                    'raw_text': card['mblog']['text'],
                    'pics': self.get_pics(card['mblog']),
                    'created_at': created_at,
                    'edit_at': edit_at,
                    'area': config['area'],
                })
                yield Request(url=self.desc_url.format(card['mblog']['bid']),
                              callback=self.get_full_text,
                              headers={'User-Agent': self.user_agent},
                              meta={'item': update_item})
        else:
            # 没有有数据，需要插入数据
            add_item: WeiboIdolAddLiveItem = WeiboIdolAddLiveItem(payload={
                'aid': card['mblog']['id'],
                'bid': card['mblog']['bid'],
                'uid': config['uid'],
                'screen_name': card['mblog']['user']['screen_name'],
                'avatar_hd': card['mblog']['user']['avatar_hd'],
                'raw_text': card['mblog']['text'],
                'pics': self.get_pics(card['mblog']),
                'created_at': created_at,
                'edit_at': edit_at,
                'area': config['area'],
            })
            yield Request(url=self.desc_url.format(card['mblog']['bid']),
                          callback=self.get_full_text,
                          headers={'User-Agent': self.user_agent},
                          meta={'item': add_item})

    def get_full_text(self, response: Response, **kwargs: Any) -> Iterable:
        """ 获取整个text """
        text_arr: list[str] = response.text.split('\n')
        item: WeiboIdolAddLiveItem | WeiboIdolUpdateLiveItem = response.meta['item']
        # 找到完整的text
        for text in text_arr:
            if len(self.full_text_start_regexp.findall(text)) > 0:
                new_text: str = re_sub(self.full_text_start_regexp, '', text)
                item['payload']['raw_text'] = re_sub(self.full_text_end_regexp, '', new_text)
                break
        # 提取text中的举办地区
        item['payload']['area'] = self.confirm_area(item['payload']['area'], item['payload']['raw_text'])
        yield item

    @staticmethod
    def filter_weibo_cards(cards: list[WeiboContainerCard]) -> FilterCardsDict:
        """ 过滤微博 """
        filter_cards: list[WeiboContainerCard] = []
        one_month_time: int = get_one_month_ago_timestamp()
        need_next: bool = True
        for card in cards:
            if 'card_type' in card and card['card_type'] == 9:
                card_time: int = convert_to_timestamp(
                    card['mblog']['edit_at'] if 'edit_at' in card['mblog'] else card['mblog']['created_at'])
                if card_time >= one_month_time:
                    filter_cards.append(card)
                else:
                    if 'title' in card['mblog'] and card['mblog']['title'].get('text') == '置顶':
                        pass # 置顶不处理
                    else:
                        need_next = False
                        break
        return {'filter_cards': filter_cards, 'need_next': need_next}

    @staticmethod
    def confirm_area(area: str, text: str) -> str:
        """ 确认举办地是哪个地区的 """
        area_group: list[str] = area.split(',')
        for a in area_group:
            if (a + '市') in text:
                return a
            elif a in text:
                return a
        return area

    @staticmethod
    def get_pics(mblog: WeiboContainerCardMblog) -> str | None:
        """ 提取图片 """
        if 'pics' not in mblog or len(mblog['pics']) <= 0:
            return
        pics: list[str] = []
        for x in mblog['pics']:
            pics.append(x['url'])
        return json_dumps(pics)

    @staticmethod
    def determine_live_msg(text: str) -> bool:
        """ 判断是否是地偶活动 """
        def list_every_callback(keywords_group: list[str]) -> bool:
            """ list_every回调函数 """
            return list_some(keywords_group, lambda k: k.lower() in text.lower())

        return list_every(performance_keywords_dict, list_every_callback)
