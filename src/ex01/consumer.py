import argparse
import redis
import logging
from time import sleep
from json import loads

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

def editingMessage(message, allElement):
    for chekNum in allElement:
        if message["metadata"]["to"] == int(chekNum) and message["amount"] > 0:
            message["metadata"]["to"], message["metadata"]["from"] = message["metadata"]["from"], message["metadata"]["to"]
            break

def getMessges(redis_client, args):
    error = 0
    try:
        ps = redis_client.pubsub()
        ps.subscribe("money_transfers")
        allElement = None
        if args.evel_gay:
            allElement = args.evel_gay.split(',')
        for message in ps.listen():
            if type(message['data']) is not int :  
                dictMessage = loads(message['data'])
                if args.evel_gay:
                    editingMessage(dictMessage, allElement)
                print(dictMessage)

    except Exception:
        logging.error("Server connection lost:\n\n", exc_info=True)
        error = 2
    return error

def getArgs(parser):
    parser.add_argument('-e', '--evel_gay', type=str, \
                        help="Indicates the numbers of the bad guys \
                              Argument format: 1234567890,1987654321")
    return parser.parse_args()

def chekArgs(args):
    error = 0
    if args.evel_gay:
        allElement = args.evel_gay.split(',')
        for element in allElement:
            if not element.isdigit() or len(element) != 10:
                error = 3
                logging.error("The passed argument was received in an invalid format\n\n")
                break
    return error

def main():
    error = 0
    parser = argparse.ArgumentParser(description='Reading messages from the server')
    args = getArgs(parser)
    error = chekArgs(args)
    if not error:
        redis_client = getConnection()
        if not redis_client: 
            error = 1
        else:
            error = getMessges(redis_client, args)
    return error

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="\n%(asctime)s %(levelname)s %(message)s")
    logging.info("The program terminated with a code: " + str(main()) + '\n')