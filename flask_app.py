from flask import Flask,request,Response,make_response,render_template
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import logging
import datetime
from time_formatter import formatter
import plivo,plivoxml
import os


log = logging.getLogger('Jose')

callID = {}

app = Flask(__name__,template_folder='/home/JoseNaveen/mysite/static/')

@app.route('/speak', methods=['GET','POST'])
def speak():
    _from = request.args.get("From")
    _to = request.args.get("SIP-H-To")
    _callerName = request.args.get("CallerName")
    _callId = request.args.get("CallUUID")
    if _from is not None and _to is not None:
        log.info("Received Call from {} to {} with Call ID {} CallerName {}".format(_from,_to,_callId,_callerName))
        callID[_callId] = {"start_time": datetime.datetime.now(),"end_time":""}
        r_xml = Element('Response')
        s_xml = SubElement(r_xml,'Speak')
        s_xml.text = "Hello From my Web Application"
        return Response(tostring(r_xml), mimetype='text/xml')
    else:
        return None

@app.route('/hangup', methods=['GET','POST'])
def hangup():
    _cause = request.form.getlist('HangupCause')[0]
    _callId = request.form.getlist('CallUUID')[0]
    log.info("Call {} Disconnected. Reason: {}".format(_callId,_cause))
    if request.form.getlist('CallUUID')[0] is not None:
        if _callId in callID:
            callID[_callId]["end_time"] = datetime.datetime.now()
            callID[_callId]["call_duration"] = callID[_callId]["end_time"] - callID[_callId]["start_time"]
            log.info("Call {} Duration {}".format(_callId,formatter(callID[_callId]["call_duration"],"%D days %H hours %M minutes %S seconds")))
    return "Close"




@app.route('/callback/', methods=['GET', 'POST'])
def callback():
    log.info(request)
    log.info(request.args)
    return "Hello from Callback"


@app.route('/dial/',methods=['GET','POST'])
def dial():
    log.info(request)
    _from = request.args.get("From")
    _to = request.args.get("SIP-H-To")
    _callerName = request.args.get("CallerName")
    _callId = request.args.get("CallUUID")
    if _from is not None and _to is not None:
        log.info("Received Call from {} to {} with Call ID {} CallerName {}".format(_from,_to,_callId,_callerName))
        callID[_callId] = {"start_time": datetime.datetime.now(),"end_time":""}
        r_xml = Element('Response')
        d_xml = SubElement(r_xml,'Dial')
        n_xml = SubElement(d_xml,'User')
        n_xml.text = "sip:endpoint2170824100313@phone.plivo.com"
        return Response(tostring(r_xml), mimetype='text/xml')
    else:
        return None