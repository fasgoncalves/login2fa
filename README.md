# 🛡️ login2fa — Login Seguro com Dupla Autenticação (2FA) via NiceGUI e NTFY

![Último Commit](https://img.shields.io/github/last-commit/fasgoncalves/login2fa)
![Versão](https://img.shields.io/badge/version-1.0.0-blue)
![Licença](https://img.shields.io/github/license/fasgoncalves/login2fa)

`login2fa` é um módulo modular e elegante para Python, desenhado com o poder do [NiceGUI](https://nicegui.io/) para aplicações web modernas.  
Implementa um **sistema completo de login com 2FA** (autenticação de dois fatores), integrando:
- Cookies de sessão persistentes por 12 horas
- Notificações via [ntfy](https://ntfy.sh) com token aleatório
- Verificação por IP local (bypass do 2FA em rede interna)
- Total compatibilidade com sistemas atrás de proxy
- Design moderno, limpo e responsivo

`login2fa` é um módulo modular e elegante para Python, desenhado com o poder do [NiceGUI](https://nicegui.io/) para aplicações web modernas.  
Implementa um **sistema completo de login com 2FA** (autenticação de dois fatores), integrando:
- Cookies de sessão persistentes por 12 horas
- Notificações via [ntfy](https://ntfy.sh) com token aleatório
- Verificação por IP local (bypass do 2FA em rede interna)
- Total compatibilidade com sistemas atrás de proxy
- Design moderno, limpo e responsivo

---

## 🚀 Instalação

```bash
git clone https://github.com/seu-utilizador/login2fa.git
cd login2fa
pip install -e .
```

---

## 🧩 Como usar

### 1. Importa e configura:

```python
from login2fa import configurar_login_2fa

configurar_login_2fa({
    'db': {
        'host': 'localhost',
        'user': 'userdb',
        'password': 'passdb',
        'database': 'dbname'
    },
    'ntfy': {
        'url': 'http://192.168.x.x',
        'user': 'user',
        'pass': 'pass'
    },
    'rota_sucesso': '/painel',
    'titulo_login': 'Acesso Seguro ao Sistema'
})
```

---

### 2. Define a rota protegida:

```python
from nicegui import ui
from fastapi import Request
from fastapi.responses import RedirectResponse

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
```

---

## 🔐 Funcionalidades

✅ Autenticação com utilizador e palavra-passe (hasheada com `bcrypt`)  
✅ Envio de token 2FA via `ntfy` (push notification para o teu telemóvel)  
✅ Cookies persistentes por 12 horas  
✅ Bypass do 2FA se acederes por IP local (192.168.x.x, etc.)  
✅ Compatível com proxies (usa `X-Forwarded-For`)  
✅ Redirecionamento automático se cookie for válido  
✅ Estilo visual apelativo com NiceGUI

---

## 🧪 Exemplo incluído

Consulta o ficheiro `exemplo.py` para ver o login2fa em funcionamento completo.

---

## 🎓 Requisitos

- Python 3.9+
- MySQL
- nicegui
- ntfy servidor local ou remoto configurado

---

## 📜 Licença

MIT — livre para usares, modificares e melhorares.  
Desenvolvido com paixão por [Francisco Gonçalves](https://github.com/seu-utilizador).

---

## 🌟 Captura de Ecrã

![login2fa](https://github.com/fasgoncalves/login2fa/tree/master/assets/login2fa.png)

---

Pronto para trazer segurança, estilo e modernidade ao teu login?  
**Instala o `login2fa` e transforma o acesso às tuas apps.**
