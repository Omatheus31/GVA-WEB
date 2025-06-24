# GVA-WEB (Gerenciador de Validade de Alimentos)

> Um projeto acadêmico de aplicação web segura, desenvolvido para a disciplina de Segurança da Informação.

## Descrição do Projeto

O GVA-WEB é um sistema web projetado para auxiliar usuários domésticos no gerenciamento de datas de validade de seus produtos alimentícios. A aplicação permite o cadastro de itens, organização por locais de armazenamento e envia notificações proativas sobre produtos próximos ao vencimento, visando reduzir o desperdício de alimentos.

O foco principal do projeto foi a aplicação e demonstração de um ciclo de desenvolvimento seguro, implementando múltiplas camadas de segurança para proteger os dados dos usuários e a integridade da aplicação, conforme solicitado pelos requisitos da disciplina.

## Funcionalidades e Competências de Segurança

O projeto conta com um robusto arsenal de funcionalidades, com ênfase em segurança:

* **Autenticação Segura:** Sistema completo de registro e login com hashing de senhas (Bcrypt).
* **Autorização:** Controle de acesso que garante que cada usuário só possa visualizar e gerenciar seus próprios dados.
* **Recuperação de Senha Segura:** Fluxo completo com tokens de uso único e tempo de expiração, enviados por e-mail.
* **Proteção contra Bots (CAPTCHA):** Uso do Google reCAPTCHA v2 para proteger o formulário de registro.
* **Autenticação de Dois Fatores (2FA):** Camada extra de segurança no login utilizando o padrão TOTP (compatível com Google Authenticator, Authy, etc.).
* **Sistema de Auditoria:** Registro de ações importantes (logins bem-sucedidos, falhas de login, etc.) em uma tabela dedicada no banco de dados para rastreabilidade.
* **Política de Conteúdo Seguro (CSP):** Implementação de cabeçalhos CSP e outros cabeçalhos de segurança (`X-Frame-Options`, `X-Content-Type-Options`) para mitigar ataques de XSS e Clickjacking.
* **Gerenciamento de Inventário:** Funcionalidades de CRUD (Create, Read, Update, Delete) para locais de armazenamento e itens alimentícios.

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