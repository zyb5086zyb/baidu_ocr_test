import requests

# 我的AK和SK
# host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MtcwIISFCHgm8y76j5faLrAX&client_secret=e3VG2Hfo6C1OY4azOPcGDiFgFkonhXmO'
# 邢哲的AK和SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=KjmIUc2wU37lqg7xGgVgACCr&client_secret=3eOxwrfFWHXTXQASmmTzTrEZI9alSuMZ'
headers = {'Content-Type': 'application/json; charset=UTF-8'}
# data = {}
resp = requests.post(url=host, headers=headers)
print(resp.json())
