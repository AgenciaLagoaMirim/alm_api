from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib
import subprocess
import os
import logging

SECRET = os.getenv("WEBHOOK_SECRET", "6}ry[Qp2)0d,=hL_^8doM8NB1JZ,.!")
PROJECT_DIR = "/home/alm_api/alm_api"  # Diretório fixo do projeto
VENV_PIP_PATH = (
    "/home/alm_api/alm_api/.venv/bin/pip"  # Caminho para o pip do ambiente virtual
)
VENV_PYTHON_PATH = "/home/alm_api/alm_api/.venv/bin/python"  # Caminho para o python do ambiente virtual

logger = logging.getLogger(__name__)


@csrf_exempt
def webhook(request):
    if request.method == "POST":

        logger.info("Iniciando processo de atualização...")

        # Validação da assinatura HMAC
        signature = (
            "sha1=" + hmac.new(SECRET.encode(), request.body, hashlib.sha1).hexdigest()
        )
        if not hmac.compare_digest(
            signature, request.headers.get("X-Hub-Signature", "")
        ):
            return HttpResponseForbidden("Forbidden")

        # Verifique se o diretório existe
        if not os.path.exists(PROJECT_DIR):
            logger.error(f"Invalid PROJECT_DIR: {PROJECT_DIR}")
            return HttpResponse("Invalid PROJECT_DIR", status=500)

        logger.info(f"Changing directory to: {PROJECT_DIR}")
        os.chdir(PROJECT_DIR)

        logger.info(f"Current working directory: {os.getcwd()}")
        logger.error(f"Current working directory: {os.getcwd()}")

        # Executar git pull
        result = subprocess.run(
            ["git", "pull", "origin", "main"], capture_output=True, text=True
        )

        if result.returncode != 0:
            logger.error(f"Git pull failed: {result.stderr}")
            return HttpResponse(result.stderr, status=500)

        # Instalar dependências do requirements.txt
        logger.info("Instalando dependências do requirements.txt")
        result = subprocess.run(
            [VENV_PIP_PATH, "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            logger.error(f"Instalação de dependências falhou: {result.stderr}")
            return HttpResponse(result.stderr, status=500)

        # Aplicar migrações do Django
        logger.info("Aplicando migrações do Django")
        result = subprocess.run(
            [VENV_PYTHON_PATH, "manage.py", "migrate"], capture_output=True, text=True
        )

        if result.returncode != 0:
            logger.error(f"Aplicação de migrações falhou: {result.stderr}")
            return HttpResponse(result.stderr, status=500)

        return HttpResponse(status=204)
    return HttpResponse(status=405)
