import os
from dotenv import load_dotenv
from tracardi_plugin_sdk.service.plugin_runner import run_plugin
from tracardi_smtp_connector.plugin import SmtpDispatcherAction

load_dotenv()

init = {
    'server': {
        'smtp': "smtp.gmails.com",
        'port': 587,
        'username': os.getenv('LOGIN'),
        'password': os.getenv('PASSWORD'),
        'timeout': 2
    },
    'message': {
        "send_to": os.getenv('TO'),
        "send_from": os.getenv('FROM'),
        "reply_to": "jakis@main.com",
        "title": "Testowy tytuł",
        "message": "Testowa wiadomość"
    }
}


payload = {}

result = run_plugin(SmtpDispatcherAction, init, payload)
print(result)
print(result.console.__dict__)
