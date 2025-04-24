import requests
import json
import base64
import hashlib
import os
from datetime import datetime

def get_image_url():
    token = os.getenv("Zaobao_token")
    url = "https://v3.alapi.cn/api/zaobao"
    querystring = {"token": token, "format": "json"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, headers=headers, params=querystring, timeout=10)
    image_url = response.json()['data']['image']
    return image_url

def get_base64_and_md5(image_url):
    img_data = requests.get(image_url, timeout=10).content
    b64_data = base64.b64encode(img_data).decode()
    md5_val = hashlib.md5(img_data).hexdigest()
    return b64_data, md5_val

def send_to_wechat(base64_str, md5_str, webhook_url):
    payload = {
        "msgtype": "image",
        "image": {
            "base64": base64_str,
            "md5": md5_str
        }
    }

    headers = {"Content-Type": "application/json"}
    resp = requests.post(webhook_url, headers=headers, data=json.dumps(payload), timeout=10)
    print(resp.status_code, resp.text)

if __name__ == "__main__":
    # 获取当前时间
    now = datetime.now()
    print("当前时间是：", now.strftime("%Y-%m-%d %H:%M:%S"))
    webhook = os.getenv("WECHAT_WEBHOOK")
    if not webhook:
        print("WECHAT_WEBHOOK environment variable not set.")
        exit(1)

    try:
        image_url = get_image_url()
        b64, md5_str = get_base64_and_md5(image_url)
        send_to_wechat(b64, md5_str, webhook)
    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1)
