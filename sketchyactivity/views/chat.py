from django.views.decorators.csrf import csrf_exempt
import requests
from django.shortcuts import redirect, render
from . import responses
import json
from .util import rp,render_to_json_response

@csrf_exempt
def slack_msging_endpoint(request):
    # get the user id.
    if request.method == "POST" : # api call from slack
        """
        request.POST = {
            'token': ['GniqX5w41BdkPoaFbefNV1wE'],
            'team_id': ['TN3C0CHBN'],
            'team_domain': ['sketchyactivity'],
            'channel_id': ['CMU91TEV8'],
            'channel_name': ['website-messaging'],
            'user_id': ['UMSC0SARZ'],
            'user_name': ['huntaj'],
            'command': ['/snd'],
            'text': ['1 hi'],
            'response_url': ['https://hooks.slack.com/commands/TN3C0CHBN/749204736337/U08DRq3LtUvZBdoWtw9T09WN'],
            'trigger_id': ['744145688451.751408425396.3a96fb8b035cc516c3cf8977580417e7']
        }
        """
        data = dict(request.POST)
        print(data)
        text = data['text'][0]
        print("Text:",text)
        uid = text.split()[0]
        message = text[text.index(" ")+1:]
        print("Sending message: ", message)
        # Post to /messaging/uid with message.
        payload = {'text': message, 'slack': ''}
        r = requests.post(f"http://sketchyactivity.com/messaging/{uid}",data=payload)

    else:
        if request.user.is_authenticated: # redirect to /userid
            return redirect(f"/messaging/{request.user.id}")
        else:
            return redirect("/")



@csrf_exempt
def messaging(request,userid):
    if request.user.is_authenticated or 'slack' in request.POST:
        if request.method == "POST":
            # if client sending a message out
            try:
                sender = request.user.first_name + " " + request.user.last_name
                message = rp(request, "message") # will fail in post from slack since posting from slack does not offer this dictionary key
                responses[str(userid)] = ""
                # add this user's id as a key to responses dictionary if not already there.
                messaging_endpoint = "https://hooks.slack.com/services/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"
                payload = {
                    "text": message,
                    "attachments": [
                        {
                            "text": "*From " + sender + " with UID " + str(request.user.id) + "*",
                            "fallback": "You are unable to respond. ",
                            "callback_id": "respond_to_msg",
                            "color": "#3AA3E3",
                            "attachment_type": "default",

                        }
                    ]
                }
                payload = json.dumps(payload)

                headers = {'Content-Type': 'application/json'}

                r = requests.post(messaging_endpoint, data=payload, headers=headers)
                # send user initials back.
                inits = request.user.first_name[0] + request.user.last_name[0]
                data = {'inits': inits}
                return render_to_json_response(data)

            except: # must be a post response from slack (that is, slack -> django endpoint -> post to this URL after extracting UID and msg

                print("Setting new message response for this user!")
                data = dict(request.POST)
                print("data: ")
                print(data)
                message = data['text']
                print("Message")
                # make this the most recent response to this user in responses dictionary.
                responses[str(userid)] = message

        if request.is_ajax() : # long polling for backend slack responses
            if str(userid) not in responses:
                print("user id not in responses. emptying.")
                responses[str(userid)] = ""
            message = responses[str(userid)]
            print("Message:",message)
            responses[str(userid)] = ""
            data = {'message': message}
            return render_to_json_response(data)
        return render(
            request=request,
            template_name='messaging.html',
            context={}
        )
    else: # not authenticated
        return redirect("/")
