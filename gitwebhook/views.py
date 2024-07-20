import hmac
import hashlib
import subprocess
import os
import logging
import json
from time import sleep
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from threading import Lock

SECRET = os.getenv("WEBHOOK_SECRET", "")
PROJECT_DIR = "/home/alm_api/alm_api"  # Diretório fixo do projeto
VENV_PIP_PATH = (
    "/home/alm_api/alm_api/.venv/bin/pip"  # Caminho para o pip do ambiente virtual
)
VENV_PYTHON_PATH = "/home/alm_api/alm_api/.venv/bin/python"  # Caminho para o python do ambiente virtual

logger = logging.getLogger(__name__)
lock = Lock()


@csrf_exempt
def webhook(request):
    try:
        if request.method == "POST":
            logger.info("Iniciando processo de atualização...")

            # Validação da assinatura HMAC
            signature = (
                "sha1="
                + hmac.new(SECRET.encode(), request.body, hashlib.sha1).hexdigest()
            )
            if not hmac.compare_digest(
                signature, request.headers.get("X-Hub-Signature", "")
            ):
                logger.error("Assinatura HMAC inválida.")
                return HttpResponseForbidden("Forbidden")

            # Verifique se o diretório existe
            if not os.path.exists(PROJECT_DIR):
                logger.error(f"Invalid PROJECT_DIR: {PROJECT_DIR}")
                return HttpResponse("Invalid PROJECT_DIR", status=500)

            # Obter lock para evitar condições de corrida
            with lock:
                logger.info(f"Changing directory to: {PROJECT_DIR}")
                os.chdir(PROJECT_DIR)
                logger.info(f"Current working directory: {os.getcwd()}")

                # Função auxiliar para executar comandos com retry
                def run_command(command, retries=3, delay=5):
                    for attempt in range(retries):
                        result = subprocess.run(command, capture_output=True, text=True)
                        if result.returncode == 0:
                            return result
                        logger.error(
                            f"Command failed (attempt {attempt + 1}/{retries}): {result.stderr}"
                        )
                        sleep(delay)
                    return result

                # Executar git pull com retry
                logger.info("Executando git pull")
                result = run_command(["git", "pull", "origin", "main"])
                if result.returncode != 0:
                    return HttpResponse(result.stderr, status=500)

                # Instalar dependências do requirements.txt com retry
                logger.info("Instalando dependências do requirements.txt")
                result = run_command(
                    [VENV_PIP_PATH, "install", "-r", "requirements.txt"]
                )
                if result.returncode != 0:
                    return HttpResponse(result.stderr, status=500)

                # Aplicar migrações do Django com retry
                logger.info("Aplicando migrações do Django")
                result = run_command([VENV_PYTHON_PATH, "manage.py", "migrate"])
                if result.returncode != 0:
                    return HttpResponse(result.stderr, status=500)

            return HttpResponse(status=204)
        return HttpResponse(status=405)
    except Exception as e:
        logger.error(f"Erro não tratado: {e}", exc_info=True)
        return HttpResponse("Erro interno do servidor", status=500)
