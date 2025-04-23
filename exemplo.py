# -*- coding: utf-8 -*-
from nicegui import ui
from fastapi import Request
from fastapi.responses import RedirectResponse
from login2fa import configurar_login_2fa

configurar_login_2fa({
    'db': {
        'host': 'localhost',
        'user': 'root',
        'password': 'yakarais',
        'database': 'authusers'
    },
    'ntfy': {
        'url': 'http://192.168.10.32:9000',
        'user': 'fgoncalves',
        'pass': 'vu#Al1'
    },
    'rota_sucesso': '/painel',
    'titulo_login': 'Portal de Acesso Seguro'
})

@ui.page('/painel')
def painel(request: Request):
    user = request.cookies.get('user')
    if user:
        return RedirectResponse(url='/sucesso', status_code=303)

@ui.page('/sucesso')
def sucesso(request: Request):
    user = request.cookies.get('user')
    ui.label(f'Bem-vindo, {user}!').classes('text-2xl text-green-700')
    ui.button('Logout', on_click=lambda: ui.navigate.to(f'/logout?user={user}')).classes('mt-4')

ui.run(port=8020)
