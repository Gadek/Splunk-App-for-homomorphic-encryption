import splunklib.client as client
from dotenv import load_dotenv
import os
import datetime
import time

def feed_index(service):
    """Feed the named index in a specific manner."""

    indexname = "main"
    # get index handle
    try:
        index = service.indexes[indexname]
    except KeyError:
        print("Index %s not found" % indexname)
        return

    count = 0
    lastevent = ""
    try:
        for i in range(0, 10):
            for j in range(0, 5000):
                lastevent = "%s: event bunch %d, number %d\n" % \
                             (datetime.datetime.now().isoformat(), i, j)

                index.submit(lastevent + "\n")
                count = count + 1

            print("submitted %d events, sleeping 1 second" % count)
            time.sleep(1)
    except KeyboardInterrupt:
        print("^C detected, last event written:")
        print(lastevent)

def main():
    load_dotenv()

    host = os.getenv('host')
    port = os.getenv('port')
    username = os.getenv('username')
    password = os.getenv('password')

    service = client.connect(host=host, port=port, username=username, password=password)
    assert isinstance(service, client.Service)

    feed_index(service)


if __name__ == "__main__":
    main()
