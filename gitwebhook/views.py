from django.shortcuts import render

# Create your views here.


# gitwebhook/views.py

from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib
import subprocess

SECRET = '6}ry[Qp2)0d,=hL_^8doM8NB1JZ,.'

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        signature = 'sha1=' + hmac.new(SECRET.encode(), request.body, hashlib.sha1).hexdigest()
        if not hmac.compare_digest(signature, request.headers.get('X-Hub-Signature', '')):
            return HttpResponseForbidden('Forbidden')

        # Comando Git para puxar as atualizações
        subprocess.Popen(['git', 'pull', 'origin', 'main'])

        # Comando para reiniciar o servidor, se necessário
        # subprocess.Popen(['systemctl', 'restart', 'gunicorn'])

        return HttpResponse(status=204)
    return HttpResponse(status=405)
