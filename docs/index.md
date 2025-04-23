# 📘 Documentação do login2fa

Bem-vindo à documentação oficial do **login2fa**, o módulo de autenticação com dupla verificação via NiceGUI e NTFY.

---

## 🚀 Instalação

```bash
pip install login2fa
```

Ou clone o repositório e instala localmente:

```bash
git clone https://github.com/fasgoncalves/login2fa.git
cd login2fa
pip install -e .
```

---

## ⚙️ Configuração

```python
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
    'titulo_login': 'Acesso Seguro ao Sistema'
})
```

---

## 🧪 Exemplo de utilização

```python
@ui.page('/painel')
def painel(request: Request):
    user = request.cookies.get('user')
    if user:
        return RedirectResponse(url='/sucesso', status_code=303)

@ui.page('/sucesso')
def sucesso(request: Request):
    user = request.cookies.get('user')
    ui.label(f'Bem-vindo, {user}!')
```

---

## 🔐 Funcionalidades

- Login e palavra-passe (hash com bcrypt)
- Token 2FA via notificação `ntfy`
- Cookies de sessão válidos por 12h
- Bypass automático em rede local
- Compatível com proxies e GitHub OAuth (opcional)

---

## 🌍 Recursos

- [📦 PyPI: login2fa](https://pypi.org/project/login2fa/)
- [💻 GitHub](https://github.com/fasgoncalves/login2fa)
- [📄 README.md](../README.md)

---

Feito com 🧠, 🐍 e um rugido de liberdade por Francisco Gonçalves.

