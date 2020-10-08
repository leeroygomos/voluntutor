from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse

import redis
import uuid
import json

# Create your views here.
def chat(request):

    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    current_user = request.user
    if(not current_user.is_authenticated):
        return render(request, 'chat.html')

    if request.is_ajax():
        data = json.load(request.body)
        if request.method == 'POST':

            message = data["message"]
            name = current_user.username
            r.xadd("chat", {
                "name": name,
                "message": message
            } )

        last_received_msg_id = data["last_received_msg_id"]    
        messages = r.xread({"chat": last_received_msg_id})
        last_received_msg_id = get_last_message_id(messages)
        message_list = extract_message_list(messages)

        json_to_return = json = {
                "last_received_msg_id": last_received_msg_id,
                "messages": message_list,}
        
        return JsonResponse(json_to_return)

    messages = r.xread({"chat": "0-0"})
    last_received_msg_id = get_last_message_id(messages)
    message_list = extract_message_list(messages)
    json_to_return = {
            "last_received_msg_id": last_received_msg_id,
            "messages": message_list,}
    
    return JsonResponse(json_to_return)
 

def get_last_message_id(messages):
    return messages[0][1][-1][0]

def extract_message_list(messages):
    messages_formatted = []
    for message in messages[0][1]:
        messages_formatted.append(message)
    return messages_formatted

#
class TwoWayChatKey:
    def __init__(self, list_of_user_ids):
        list.sort()
        key = ''
        for _id in list:
            key += _id
            key += ':'
        self.key = key