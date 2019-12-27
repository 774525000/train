from train.train.train import Train
from time import sleep

def run(home_url, email, password, chaojiying_name, chaojiying_pass, chaojiying_app_id):
    Train.default(home_url, email, password)
    sleep(100)
