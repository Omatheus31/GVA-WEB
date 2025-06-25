# GVA-WEB (Gerenciador de Validade de Alimentos)

> Um projeto acadêmico de aplicação web segura, desenvolvido para a disciplina de Segurança da Informação.

## Descrição do Projeto

O GVA-WEB é um sistema web projetado para auxiliar usuários domésticos no gerenciamento de datas de validade de seus produtos alimentícios. A aplicação permite o cadastro de itens, organização por locais de armazenamento e envia notificações proativas sobre produtos próximos ao vencimento, visando reduzir o desperdício de alimentos.

O foco principal do projeto foi a aplicação e demonstração de um ciclo de desenvolvimento seguro, implementando múltiplas camadas de segurança para proteger os dados dos usuários e a integridade da aplicação, conforme solicitado pelos requisitos da disciplina.

##  Funcionalidades e Competências de Segurança

O projeto conta com um robusto arsenal de funcionalidades, com ênfase em segurança, implementadas em locais específicos do código:

* **Autenticação Segura com Hashing de Senhas**
    * **Descrição:** Sistema completo de registro e login. As senhas dos usuários nunca são armazenadas em texto plano, utilizando o algoritmo Bcrypt para gerar um hash seguro.
    * **Onde encontrar no código:**
        * **Modelagem:** A lógica de senha está encapsulada nos métodos `set_password()` e `check_password()` da classe `User` em `app/models.py`.
        * **Rotas:** A criação do hash (no registro) e a verificação (no login) são chamadas nas rotas `register()` e `login()` em `app/auth/routes.py`.
        * **Extensão:** O objeto `bcrypt` é inicializado em `app/extensions.py`.

* **Autorização Baseada em Papéis (Implícita)**
    * **Descrição:** Controle de acesso que garante que cada usuário só possa visualizar e gerenciar seus próprios dados (locais e alimentos).
    * **Onde encontrar no código:**
        * **Lógica Principal:** A filtragem dos dados é feita na rota `dashboard()` em `app/main/routes.py`, utilizando consultas como `Location.query.filter_by(user_id=current_user.id)`.
        * **Proteção de Rotas:** O decorador `@login_required` é usado em rotas como `/dashboard` para garantir que apenas usuários autenticados possam acessá-las.

* **Recuperação de Senha Segura**
    * **Descrição:** Fluxo completo com tokens de segurança (JWT) de uso único e tempo de expiração, enviados por e-mail para o usuário.
    * **Onde encontrar no código:**
        * **Geração de Token:** Os métodos `get_reset_password_token()` e `verify_reset_password_token()` estão na classe `User` em `app/models.py`.
        * **Envio de E-mail:** A função `send_password_reset_email()` está em `app/auth/email.py`.
        * **Rotas:** As páginas para solicitar e para efetuar a redefinição estão nas funções `reset_password_request()` e `reset_password()` em `app/auth/routes.py`.

* **Proteção contra Bots (CAPTCHA)**
    * **Descrição:** Uso do Google reCAPTCHA v2 para proteger o formulário de registro contra submissões automatizadas por robôs.
    * **Onde encontrar no código:**
        * **Configuração:** As chaves são definidas em `.env` e carregadas em `config.py`. A extensão é inicializada em `app/extensions.py` e `app/__init__.py`.
        * **Validação:** A verificação `recaptcha.verify()` é executada na rota `register()` em `app/auth/routes.py`.
        * **Renderização:** O widget é exibido no template `app/templates/auth/register.html` através da tag `{{ recaptcha }}`.

* **Autenticação de Dois Fatores (2FA)**
    * **Descrição:** Camada extra de segurança no login utilizando o padrão TOTP, compatível com apps como Google Authenticator.
    * **Onde encontrar no código:**
        * **Modelagem:** Os campos `tfa_secret` e `tfa_enabled` foram adicionados à classe `User` em `app/models.py`.
        * **Rota de Ativação:** A lógica para gerar o QR Code e ativar o 2FA está na rota `tfa_setup()` em `app/main/routes.py`.
        * **Rota de Verificação:** A rota de login foi modificada para redirecionar para `/2fa_verify`, cuja lógica está na função `tfa_verify()` em `app/auth/routes.py`.

* **Sistema de Auditoria**
    * **Descrição:** Registro de ações importantes (logins bem-sucedidos, falhas de login) em uma tabela dedicada no banco de dados para futura análise e rastreabilidade.
    * **Onde encontrar no código:**
        * **Modelo:** A classe `AuditLog` que define a estrutura da tabela de logs está em `app/models.py`.
        * **Lógica:** Uma função auxiliar `log_audit()` foi criada e é chamada na rota `login()` em `app/auth/routes.py` para registrar os eventos.

* **Política de Conteúdo Seguro (CSP) e Cabeçalhos de Segurança**
    * **Descrição:** Implementação de cabeçalhos de resposta HTTP para instruir o navegador a mitigar ataques de Cross-Site Scripting (XSS) e Clickjacking.
    * **Onde encontrar no código:**
        * **Implementação Central:** A lógica está centralizada na função `add_security_headers()`, que usa o decorador `@app.after_request`, dentro do arquivo `app/__init__.py`.


## Tecnologias Utilizadas

* **Backend:** Python, Flask
* **Banco de Dados:** PostgreSQL
* **ORM e Migrações:** Flask-SQLAlchemy, Flask-Migrate
* **Segurança e Autenticação:** Flask-Login, Flask-Bcrypt, PyJWT (para tokens), Flask-ReCaptcha, pyotp
* **Envio de E-mail:** Flask-Mail
* **Frontend:** HTML5, CSS3 (com Templates Jinja2)
* **Geração de QR Code:** qrcode[pil]

## Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e rodar a aplicação em um ambiente de desenvolvimento.

**Pré-requisitos:**
* Python 3.10+
* PostgreSQL instalado e rodando.

**Passos:**

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/Omatheus31/GVA-WEB.git
    cd GVA-WEB
    ```

2. **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o Banco de Dados PostgreSQL:**
    * Abra o pgAdmin ou use o `psql`.
    * Crie um novo banco de dados. Ex: `CREATE DATABASE gva_db;`.

5. **Configure as Variáveis de Ambiente:**
    * Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`:
        ```bash
        # Windows
        copy .env.example .env
        ```
    * Abra o arquivo `.env` e preencha **TODAS** as variáveis com as suas próprias credenciais (chave secreta, URL do banco, chaves do reCAPTCHA, credenciais de e-mail).

6. **Aplique as Migrações do Banco de Dados:**
    * Este comando criará todas as tabelas necessárias.
    ```bash
    flask db upgrade
    ```

7. **Rode a Aplicação:**
    ```bash
    flask run
    ```
    A aplicação estará disponível em `http://127.0.0.1:5000`.

## Licença

Este projeto é distribuído sob a Licença MIT.

## Autor

* **Matheus Farias Sousa**
    * GitHub: https://github.com/Omatheus31
    * LinkedIn: https://www.linkedin.com/in/matheus-farias-sousa-05873821a/