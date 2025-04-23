# -*- coding: utf-8 -*-
from nicegui import ui
import mysql.connector
import bcrypt
import random
import string
import time
import requests

from fastapi import Request
from fastapi.responses import RedirectResponse, HTMLResponse
from urllib.parse import parse_qs, urlparse

auth_tokens = {}

def configurar_login_2fa(config):
    DB_CONFIG = config['db']
    NTFY_CONFIG = config['ntfy']
    ROTA_SUCESSO = config.get('rota_sucesso', '/dashboard')
    TITULO_LOGIN = config.get('titulo_login', 'Bem-vindo! Inicie sessão')

    def send_notification(topic, token):
        try:
            headers = {"Title": "Mensagem Seguranca 2FA", "Priority": "high"}
            message = "Introduza no login o token: " + token
            url = f"{NTFY_CONFIG['url'].rstrip('/')}/{topic}"
            requests.post(url, headers=headers, data=message.encode("utf-8"),
                          auth=(NTFY_CONFIG['user'], NTFY_CONFIG['pass']))
        except Exception as e:
            print(f"Error sending notification: {e}")

    def send_token_ntfy(topic, token):
        send_notification(topic, token)

    def get_user(username):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    def generate_token(length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def is_token_valid(username, token):
        if username in auth_tokens:
            stored_token, timestamp = auth_tokens[username]
            if stored_token == token and time.time() - timestamp <= 120:
                return True
        return False

    def create_user(username, password, ntfy_topic):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash, ntfy_topic) VALUES (%s, %s, %s)",
                    (username, password_hash, ntfy_topic))
        conn.commit()
        cursor.close()
        conn.close()

    @ui.page('/')
    def show_login(request: Request):
        user = request.cookies.get('user')
        print(f'COOKIES: {request.cookies}')  # DEBUG
        if user:
            return RedirectResponse(url=ROTA_SUCESSO, status_code=303)
        with ui.card().classes('w-96 shadow-xl mx-auto mt-20'):
            ui.label(TITULO_LOGIN).classes('text-xl font-bold')
            username_input = ui.input('Utilizador').classes('w-full')
            password_input = ui.input('Palavra-passe', password=True).classes('w-full')

            def login_attempt():
                client_ip = request.headers.get('x-forwarded-for', request.client.host)
                is_local = client_ip.startswith('192.168.') or client_ip.startswith('10.') or client_ip.startswith('127.') or client_ip == '::1'

                user = get_user(username_input.value)
                if user and bcrypt.checkpw(password_input.value.encode(), user['password_hash'].encode()):
                    token = generate_token()
                    auth_tokens[user['username']] = (token, time.time())
                    if not is_local:
                        send_token_ntfy(user['ntfy_topic'], token)
                        ui.notify('Token enviado para o seu ntfy')
                        ui.navigate.to(f'/token?user={user["username"]}')
                    else:
                        ui.notify('Login local detetado. Acesso direto.')
                        ui.navigate.to(f'/validar_token?user={user["username"]}&token={token}')
                else:
                    ui.notify('Credenciais inválidas', type='negative')

            ui.button('Entrar', on_click=login_attempt).classes('w-full mt-4')

    @ui.page('/token')
    def token_page(request: Request):
        query = parse_qs(urlparse(str(request.url)).query)
        username = query.get('user', [None])[0]
        if not username:
            ui.label('Erro: utilizador não especificado').classes('text-red-600')
            return

        with ui.card().classes('w-96 shadow-xl mx-auto mt-20'):
            ui.label('Introduza o código enviado').classes('text-lg')
            token_input = ui.input('Código').classes('w-full')

            def validar_token():
                ui.navigate.to(f'/validar_token?user={username}&token={token_input.value}')

            ui.button('Validar', on_click=validar_token).classes('w-full mt-4')

    @ui.page('/validar_token')
    def validar_token_page(request: Request):
        query = parse_qs(urlparse(str(request.url)).query)
        username = query.get('user', [None])[0]
        token = query.get('token', [None])[0]

        if not username or not token:
            return HTMLResponse('<h3>Dados em falta</h3>')

        if is_token_valid(username, token):
            response = RedirectResponse(url=ROTA_SUCESSO, status_code=303)
            response.set_cookie(
                key='user', value=username, max_age=43200,
                secure=True, httponly=False, path='/', samesite='Lax'
            )
            return response
        else:
            return HTMLResponse('<h3>Token inválido ou expirado</h3><a href="/">Voltar</a>')

    @ui.page('/logout')
    def logout_page(request: Request):
        query = parse_qs(urlparse(str(request.url)).query)
        username = query.get('user', [None])[0]
        if username:
            auth_tokens.pop(username, None)
        response = HTMLResponse('<meta http-equiv="refresh" content="0; url=/">')
        response.delete_cookie('user')
        return response
