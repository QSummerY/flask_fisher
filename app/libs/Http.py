import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        # return_json 参数是判断结果是否要转换为json格式
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
