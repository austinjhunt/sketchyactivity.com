from rest_framework.views import APIView, Response
import requests
import json
import logging

logger = logging.getLogger('sketchyactivity')

class NotifyView(APIView):
    def get(self, request):
        logger.info({
            'action': 'notify',
            'ip': request.META.get('REMOTE_ADDR','Unknown'),
        })
        try:
            webhook_url = "https://hooks.slack.com/services/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"
            # get ip address of request
            ip = request.META.get('REMOTE_ADDR','Unknown')
            text = {"text": f"Someone is viewing your site from IP {ip}!"}
            headers = {'Content-Type': 'application/json'}
            r = requests.post(
                webhook_url, data=json.dumps(text), headers=headers)
            return Response(r.json(), status=r.status_code)
        except Exception as e:
            logger.error({
                'action': 'notify',
                'error': str(e),
            })
            return Response({'error': str(e)}, status=500)