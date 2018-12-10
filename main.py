from prometheus_client import start_http_server, Summary, Counter
import random
import time
import dns.resolver
import os

success = Counter('dns_success', 'Description of counter')
error = Counter('dns_error', 'Description of counter')

def process_request(t, names):
    time.sleep(t)

    parts = names.split(",")
    for name in parts:
        try:
            answers = dns.resolver.query(name)
            if answers.rrset.items.__len__() > 0:
                success.inc()
                for item in answers.rrset.items:
                    print ("name: " + name + " ip:" + item.address)
            else:
                print ("name: " + name + " Not able to resolve")
                error.inc()
        except:
            print ("name: " + name + " Not able to resolve")
            error.inc()

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(int(os.environ["INTERVAL"]), os.environ["DNSNAMES"])
