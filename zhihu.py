import requests
from urllib.parse import urlencode
from requests import codes
from pyquery import PyQuery as pq
import math
import csv
import time

base_url = 'https://www.zhihu.com/api/v4/questions/282469494/answers?'
number = 8862 #当前回答数量
headers = {
    'Host': 'www.zhihu.com',
    'Refer': 'https://www.zhihu.com/question/282469494',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'X-Requested-With': 'fetch'
}
def get_page(offset): #构造请求
    params = {
        'include': """data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,
                   annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,
                   suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,
                   reshipment_settings,comment_permission,created_time,updated_time,review_info,
                   relevant_info,question,excerpt,relationship.is_authorized,
                   is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized;data[*].
                   mark_infos[*].url;data[*].author.follower_count,badge[*].topics""",
        'limit': 5,
        'offset': offset, #偏移参数
        'platform': 'desktop',
        'sort_by': 'default',
}
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if codes.ok == response.status_code:
            return response.json()
    except requests.ConnectionError or ConnectionAbortedError or ConnectionRefusedError as e:
        print('Error', e.reason)

def parse_page(json): #解析获取数据
    if json:
        items = json.get('data')
        #number = json.get('paging').get('totals')
        for index, item in enumerate(items):
            if index == 0:
                continue
            answer = {}
            answer['answer_id'] = item.get('id')
            answer['question_url'] = item.get('question').get('url')
            answer['author_id'] = item.get('author').get('id')
            answer['author_url'] = item.get('author').get('url')
            answer['answer_url'] = item.get('url')
            answer['answer_text'] = pq(item.get('content')).text()
            answer['voteup_count'] = item.get('voteup_count')
            answer['comment_count'] = item.get('comment_count')
            yield  answer

def save_to_csv(answer): #保存为CSV文件
    with open('D://data.csv', 'a+', encoding='utf-8') as csvfile:
        fieldnames = ['answer_id', 'question_url', 'author_id', 'author_url', 'answer_url', 'answer_text','voteup_count','comment_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(answer)


if __name__ == '__main__':
    for i in range(0, math.ceil(number/5)+1):
        offset = i * 5
        json = get_page(offset)
        answers = parse_page(json)
        time.sleep(5)
        for answer in answers:
            save_to_csv(answer)
        print('Done')


