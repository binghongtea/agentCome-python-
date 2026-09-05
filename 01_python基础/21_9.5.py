import requests

url = 'https://v1.hitokoto.cn/'

params = {
    'c': 'a',
    'encode': 'json'
}

try:
    print(f'正在发送GET请求到：{url},参数:{params}')
    response = requests.get(url, params=params)
    status_code = response.status_code
    if status_code == 200:
        print('请求成功')
        data = response.json()
        print(data)
        hitokoto = data['hitokoto']
        from_who = data['from_who'] if data['from_who'] else '未知'
        print(f"随机名言: {hitokoto} - {from_who}")
    elif status_code == 404:
        print(f"请求的资源未找到！状态码: {status_code}")
    elif status_code == 500:
        print(f"服务器内部错误！状态码: {status_code}")
    else:
        print(f"发生未知错误，状态码: {status_code}")
except requests.RequestException as e:
    print(f"请求过程中出现错误: {e}")
