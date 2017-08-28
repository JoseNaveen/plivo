import plivo, plivoxml
import logging
from ast import literal_eval
import time
log = logging.getLogger('Caller')
log.setLevel(logging.DEBUG)
myhandler = logging.StreamHandler()  # writes to stderr
myformatter = logging.Formatter(fmt='%(levelname)s: %(message)s')
myhandler.setFormatter(myformatter)
log.addHandler(myhandler)


def call_number(p):



    params = {
    #'to': 'sip:endpoint2170824100313@phone.plivo.com',    # The phone numer to which the call will be placed
    'to' : 'sip:endpoint1170824100250@phone.plivo.com', # The phone number to be used as the caller id
    'from' : '1111111111',
    #'from' : '+919686125684',
    #'answer_url' : "https://s3.amazonaws.com/static.plivo.com/answer.xml",
    'answer_url' : "http://josenaveen.pythonanywhere.com/dial",
    #'answer_url' : 'http://josenaveen.pythonanywhere.com/speak',
    'hangup_url' : 'http://josenaveen.pythonanywhere.com/hangup',
    'hangup_method': 'POST',
    'answer_method' : "GET", # The method used to call the answer_url

    # Example for asynchronous request
    # callback_url is the URL to which the API response is sent.
    #'callback_url': "http://josenaveen.pythonanywhere.com/callback/",
    #'callback_method': "GET" # The method used to notify the callback_url.
    }

    # Make an outbound call and print the response
    response = p.make_call(params)
    return str(response)






if __name__ == '__main__':
    auth_id = "MAMTKZZMNIMJJHNZI1NT"
    auth_token = "NjYzNTBkNTI2MjY1MzQzZDA5OGYyOTVlYjQ1MjFi"
    p = plivo.RestAPI(auth_id, auth_token)
    log.info("Calling....")
    r = call_number(p)
    #log.info(r)
    resp = literal_eval(r)
    if resp[0] < 300:
        log.info("call successfully placed")
    else:
        log.info("call failed")
    live_calls = literal_eval(str(p.get_live_calls()))
    for i in live_calls[1]['calls']:
        call_params = {'call_uuid': str(i)}
        cdr = literal_eval(str(p.get_cdr(call_params)))
        log.info(call_params)
        #log.info(cdr)
        while True:
            time.sleep(2)
            log.info("Inside While")
            log.info("Getting CDR")
            call_params = {'call_uuid': str(i)}
            cdr = literal_eval(str(p.get_cdr(call_params)))
            if cdr[0] > 300:
                pass
            else:
                log.info("Call From {} To {}".format(cdr[1]['from_number'],cdr[1]['to_number']))
                log.info("Call {} Disconnected. Call Duration {}".format(cdr[1]['call_uuid'],cdr[1]['call_duration']))
                live_calls = literal_eval(str(p.get_live_calls()))
                if len(live_calls[1]['calls']) == 0:
                    log.info("No Active Calls")
                    break
                break





