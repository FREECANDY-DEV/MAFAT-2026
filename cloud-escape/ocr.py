import boto3
session = boto3.Session(
    aws_access_key_id="ASIARYWSMSYIMLIFTXQE",
    aws_secret_access_key="2pFYytUGEJ61BMm0LEWESi0d71uWsf2TjoGpwObR",
    aws_session_token="IQoJb3JpZ2luX2VjELb//////////wEaDGlsLWNlbnRyYWwtMSJGMEQCIDpaG+c2mutY4AeFGfNj7oLjQMeRIsmd0NuI37jMbzhrAiA0PNs5JJEosI8VsHZvtRtKgyq1OZfrfHIoOzZBoAugeyq1AggjEAAaDDEyMTc3NDA1Mjg4MCIMUFWh9GRVwObVUas1KpICQXRQ0m3on3qF93Q0rOaryZIVQNYEgWm6UKvUzYd+i/s6gHXodfCt1JKYpsPNqQ4gwrxvCKiP8Tr2f3tZ7Wox+TH2TTxNjYyzsDw3iedbCJp+5NXZ8xEerIpmIeyMKFM4s//Cn4k3i70ysMD3cgFkYX3A4EvOeP1bE0JukWRwJEGftHlKpmtYjijVGtGCu2bc58w9LTIRSsAztboEt4muWQ2xlNa5IYEXaciHoU3VnpkU537ZlGqpnO3MVyXukDhmj6wVhS231TXp1LS9FW9YirdqA1LU6JwCgGERQiC6FZte6VqeQW7/UvbgcIkTvUiYqHL/vzY6+TsoTNuYiqjJ0wrL4mp3FmMT5VSV6vyKEtD4FDDkhszTBjqeAd5NRHgUIjh1w6DyNpim5EeZx7ULUCpbxkUEwpyZRXQHtukm7sOeGsP4HSgp3/DvLu2pS+YhLlWx8ag+KoLE1WVynoEpjvNbG6NXlUK0eCsS81BdGTy0kHRdJCV36nZQLEdoDCPxjAZn4Nd0kihI9HU0k7EFKvtuQCtTf7B8hIydoVFQu/WMw3AAQRjYQyHDy58kBUo9u65TTgHWqZSg",
    region_name="us-east-1"
)
rek = session.client('rekognition')
with open('junior.png', 'rb') as f:
    img = f.read()

try:
    res = rek.detect_text(Image={'Bytes': img})
    for text in res['TextDetections']:
        if text['Type'] == 'LINE':
            print(text['DetectedText'])
except Exception as e:
    print(e)
