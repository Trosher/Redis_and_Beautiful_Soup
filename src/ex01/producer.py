import redis
import logging
from random import randint
from time import sleep
from json import dumps

def createConnection():
    redis_client = redis.Redis()
    redis_client.ping()
    return redis_client

def getConnection():
    redis_client = None
    try:
        redis_client = createConnection()
    except Exception:
        logging.error("Failed to establish a connection with the redis server:\n\n", exc_info=True)
    return redis_client
        
def genMessage():
    from_ = str(randint(1,9))*10
    to_ = str(randint(1,9))*10
    while to_ == from_:
        to_ = randint(1,9)
    amount_ = randint(1,10000) * (-1 if randint(0,1) == 1 else 1)
    return {"metadata": {"from": int(from_),"to": int(to_)},"amount": amount_}

def genMessageToServer(redis_client):
    error = 0
    try:
        while True:
            message = genMessage()
            redis_client.publish("money_transfers", dumps(message))
            logging.info("Message " + str(message) + " sent to server")
            sleep(5)
    except Exception:
        logging.error("Server connection lost:\n\n", exc_info=True)
        error = 2
    return error
        
def main():
    error = 0
    redis_client = getConnection()
    if not redis_client: 
        error = 1
    else:
        error = genMessageToServer(redis_client)
    return error
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="\n%(asctime)s %(levelname)s %(message)s")
    logging.info("The program terminated with a code: " + str(main()) + '\n')