from train.train.train import Train
from time import sleep

def run(home_url, email, password, chaojiying_name, chaojiying_pass, chaojiying_app_id, pic_type):
    Train.default(home_url, email, password, chaojiying_name, chaojiying_pass, chaojiying_app_id, pic_type)
    sleep(100)
