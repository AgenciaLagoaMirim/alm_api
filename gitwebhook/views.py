from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib
import subprocess
import os
import logging

SECRET = '6}ry[Qp2)0d,=hL_^8doM8NB1JZ,.'
PROJECT_DIR = '/home/alm_api/alm_api'  # Diretório fixo do projeto

logger = logging.getLogger(__name__)

@csrf_exempt
def webhook(request):
    if request.method == 'POST':

        logger.info(f"Iniciando processo de atualizacao!")

        signature = 'sha1=' + hmac.new(SECRET.encode(), request.body, hashlib.sha1).hexdigest()
        if not hmac.compare_digest(signature, request.headers.get('X-Hub-Signature', '')):
            return HttpResponseForbidden('Forbidden')

        # Verifique se o diretório existe
        if not os.path.exists(PROJECT_DIR):
            logger.error(f"Invalid PROJECT_DIR: {PROJECT_DIR}")
            return HttpResponse("Invalid PROJECT_DIR", status=500)

        logger.info(f"Changing directory to: {PROJECT_DIR}")
        os.chdir(PROJECT_DIR)

        logger.info(f"Current working directory: {os.getcwd()}")

        result = subprocess.run(['git', 'pull', 'origin', 'main'], capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"Git pull failed: {result.stderr}")
            return HttpResponse(result.stderr, status=500)

        return HttpResponse(status=204)
    return HttpResponse(status=405)
