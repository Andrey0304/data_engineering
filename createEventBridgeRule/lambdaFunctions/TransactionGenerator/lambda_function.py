import json
import logging
import transaction_generator


def lambda_hendler(event, context):
    config = json.load(open('config.json'))
    
    logging.basicConfig(**config['logger'])
    
    transaction_generator.generator(config, N=5)
    
    return 0
