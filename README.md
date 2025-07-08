# GVA-WEB (Gerenciador de Validade de Alimentos)

> Um projeto acadêmico de aplicação web segura, desenvolvido para a disciplina de Segurança da Informação, com o objetivo de criar uma ferramenta funcional e demonstrar a implementação de um ciclo de desenvolvimento seguro.

## 📝 Descrição do Projeto

O GVA-WEB é um sistema web projetado para auxiliar usuários domésticos no gerenciamento de datas de validade de seus produtos alimentícios. A aplicação permite o cadastro de itens, organização por locais de armazenamento e executa um script para notificar proativamente os usuários sobre produtos próximos ao vencimento, visando reduzir o desperdício de alimentos.

O foco principal do projeto foi a aplicação e demonstração de múltiplas camadas de segurança para proteger os dados dos usuários e a integridade da aplicação, conforme solicitado pelos requisitos da disciplina.

## ✨ Funcionalidades e Competências de Segurança

O projeto conta com um robusto arsenal de funcionalidades, com ênfase em segurança:

  * **Registro Seguro e Confirmação de E-mail:** Sistema de registro protegido por **CAPTCHA** e complexidade de senha, que exige a ativação da conta via link de confirmação enviado por e-mail.
  * **Autenticação Segura e 2FA:** Login com senhas "hasheadas" (Bcrypt) e uma camada opcional de **Autenticação de Dois Fatores (2FA)** usando o padrão TOTP.
  * **Gerenciamento de Conta pelo Usuário:** O usuário logado pode **alterar sua própria senha** (requer a senha atual) e **excluir sua própria conta** de forma permanente (requer confirmação com senha).
  * **Recuperação de Senha Segura:** Fluxo completo com tokens JWT de uso único e tempo de expiração, enviados por e-mail.
  * **Autorização Baseada em Papel (Admin/Usuário):** Controle de acesso que garante que cada usuário só acesse seus próprios dados. O papel de `admin` tem acesso a um painel restrito.
  * **Gerenciamento de Usuários (Admin):** O administrador pode visualizar, editar (promover a admin) e excluir contas de usuário através do painel de administração.
  * **Sistema de Auditoria:** Registro de eventos críticos (logins, falhas, alterações de senha, etc.) em uma tabela dedicada, com uma interface de visualização para administradores.
  * **Política de Conteúdo Seguro (CSP) e Cabeçalhos HTTP:** Implementação de cabeçalhos de segurança para mitigar ataques de Cross-Site Scripting (XSS) e Clickjacking.
  * **Notificações Proativas de Validade:** Um script customizado (`flask send-expiry-alerts`) verifica e envia e-mails de alerta sobre alimentos próximos do vencimento.

## 🛠️ Tecnologias Utilizadas

  * **Backend:** Python, Flask
  * **Banco de Dados:** PostgreSQL
  * **ORM e Migrações:** Flask-SQLAlchemy, Flask-Migrate
  * **Segurança e Autenticação:** Flask-Login, Flask-Bcrypt, PyJWT, Flask-ReCaptcha, pyotp, Flask-Mail
  * **Frontend:** HTML5, CSS3 (com Templates Jinja2)
  * **Geração de QR Code:** qrcode[pil]
  * **Fusos Horários:** pytz

## 🚀 Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e rodar a aplicação em um ambiente de desenvolvimento.

**Pré-requisitos:**

  * Python 3.10+
  * PostgreSQL instalado e rodando.
  * Git instalado.

**Passos:**

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/Omatheus31/GVA-WEB.git
    cd GVA-WEB
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados PostgreSQL:**

      * Abra o pgAdmin ou use o `psql`.
      * Crie um novo banco de dados. Ex: `CREATE DATABASE gva_db;`.

5.  **Configure as Variáveis de Ambiente:**

      * Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`:
        ```bash
        # Windows
        copy .env.example .env
        ```
      * Abra o arquivo `.env` e preencha **TODAS** as variáveis com suas próprias credenciais (gere uma `SECRET_KEY` nova, coloque a URL do seu banco, suas chaves do reCAPTCHA e suas credenciais de e-mail com Senha de App).

6.  **Aplique as Migrações do Banco de Dados:**

      * Este comando criará todas as tabelas necessárias.

    <!-- end list -->

    ```bash
    flask db upgrade
    ```

7.  **Crie o Primeiro Usuário Administrador (Opcional):**

      * Registre uma conta normalmente pela interface web.
      * Abra o terminal (com o `venv` ativo) e execute `flask shell`.
      * Dentro do shell, execute os seguintes comandos para promover seu usuário:
        ```python
        from app.models import User
        from app.extensions import db
        # Substitua 'seu_username' pelo nome do usuário que você criou
        user = User.query.filter_by(username='seu_username').first()
        if user:
            user.is_admin = True
            user.is_confirmed = True # Confirma o admin automaticamente
            db.session.commit()
            print(f"Usuário {user.username} promovido a admin e confirmado com sucesso!")
        exit()
        ```

8.  **Rode a Aplicação em Modo Seguro (HTTPS):**

    ```bash
    flask run --cert=adhoc
    ```

      * A aplicação estará disponível em **`https://127.0.0.1:5000`**.
      * **Aviso:** Seu navegador exibirá um alerta de segurança. Isso é **normal e esperado**. Clique em "Avançado" e depois em "Ir para 127.0.0.1 (não seguro)" para acessar o site.

9.  **Executando Tarefas Adicionais:**

      * Para enviar os e-mails de alerta de validade, execute o seguinte comando em um terminal separado:
        ```bash
        flask send-expiry-alerts
        ```

## 📄 Licença

Este projeto é distribuído sob a Licença MIT.

## 👨‍💻 Autor

  * **Matheus Farias Sousa**
      * GitHub: [https://github.com/Omatheus31](https://github.com/Omatheus31)
      * LinkedIn: [https://www.linkedin.com/in/matheus-farias-sousa-05873821a/](https://www.linkedin.com/in/matheus-farias-sousa-05873821a/)