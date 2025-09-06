# Resumo e Plano de Sprints – Sistema de Reconhecimento Facial

## 1. Resumo do Projeto
O objetivo é desenvolver um sistema de controle de acesso a um cofre de alta segurança, utilizando reconhecimento facial como método de autenticação. O sistema será construído em **Django**, com uma interface web simples para cadastro e gerenciamento de usuários. A biblioteca **DeepFace** será usada para o reconhecimento facial, garantindo maior precisão.

O sistema contará com três níveis de acesso hierárquicos, e todas as tentativas de acesso (bem-sucedidas ou não) serão registradas em um banco de dados **MySQL**.

### Principais Tecnologias:
- **Backend:** Django 4+
- **Frontend:** Django Templates + Bootstrap 5
- **Banco de Dados:** MySQL
- **Reconhecimento Facial:** DeepFace e OpenCV
- **Linguagem:** Python 3.10+

---

## 2. Sprints de Execução

### Sprint 0: Prova de Conceito (PoC)
- **Objetivo:** Validar a funcionalidade principal de reconhecimento facial de forma rápida e isolada, antes de configurar o banco de dados e outras funcionalidades complexas.
- **Tarefas:**
  1.  **Instalar dependências mínimas:** `Django`, `opencv-python`, `deepface`.
  2.  **Criar uma view de login simples:** Um formulário básico com campos para email e senha.
  3.  **Lógica de login hardcoded:** Na view, verificar se o email é `guilhermereif18@gmail.com` e a senha é `admin`.
  4.  **Criar view de reconhecimento:** Se o login for bem-sucedido, redirecionar para uma página que ativa a câmera.
  5.  **Comparação facial:** Usar `DeepFace.verify()` para comparar o rosto capturado pela câmera com a imagem de referência (`foto4.jpg`).
  6.  **Exibir resultado:** Mostrar na tela uma mensagem simples como "Rosto reconhecido" ou "Rosto não reconhecido".
- **Critério de Aceitação:** Após o login com as credenciais fixas, o sistema ativa a câmera e consegue executar a comparação facial, exibindo o resultado na tela.

### Sprint 1: Estrutura e Banco de Dados
- **Objetivo:** Configurar o ambiente de desenvolvimento e a base do projeto.
- **Tarefas:**
  1.  **Instalar dependências completas:** `mysqlclient` e outras que venham a ser necessárias.
  2.  **Criar apps:** `python manage.py startapp usuarios`, `python manage.py startapp acessos`, `python manage.py startapp painel`.
  3.  **Configurar `settings.py`:** Adicionar os novos apps (`usuarios`, `acessos`, `painel`) à lista de `INSTALLED_APPS`. Configurar a conexão com o banco de dados MySQL (database: `django_reconhecimento`, user: `root`).
  4.  **Modelar o banco:** Criar os models `Usuario` e `LogAcesso` em `usuarios/models.py` e `acessos/models.py`, respectivamente, seguindo a estrutura definida em `configuracaoTabelas.md`.
  5.  **Aplicar migrações:** `python manage.py makemigrations` e `python manage.py migrate`.
- **Critério de Aceitação:** Apps criados e registrados, e tabelas `usuario` e `log_acesso` visíveis no phpMyAdmin com a estrutura correta.

### Sprint 2: Cadastro de Usuários
- **Objetivo:** Implementar o fluxo de cadastro de usuários com upload de fotos e conexão com o banco de dados.
- **Tarefas:**
  1.  **Customizar Django Admin:** Criar uma interface no admin para gerenciar usuários (CRUD).
  2.  **Criar formulário de upload:** Permitir o upload de 1 a N fotos por usuário.
  3.  **Processamento de imagem:** No momento do cadastro, extrair o *embedding* do rosto de cada foto usando DeepFace.
  4.  **Armazenamento:** Salvar os dados do usuário, o caminho da foto e o *embedding* no banco de dados.
  5.  **Validação:** Garantir que o `cracha` seja único.
- **Critério de Aceitação:** Um administrador consegue cadastrar um novo usuário, fazer upload de uma foto, e o *embedding* facial é gerado e salvo corretamente no banco.

### Sprint 3: Lógica de Reconhecimento Facial (Integrada)
- **Objetivo:** Integrar o reconhecimento facial com o banco de dados de usuários.
- **Tarefas:**
  1.  **Refatorar a view de reconhecimento:** Modificar a view da PoC para, em vez de usar uma imagem fixa, buscar os *embeddings* de todos os usuários no banco de dados.
  2.  **Comparação 1-N:** Comparar o rosto detectado na câmera com a lista de *embeddings* do banco.
  3.  **Lógica de autenticação:** Se uma correspondência for encontrada, identificar o usuário correspondente.
  4.  **Registro de log:** Registrar cada tentativa (sucesso ou falha) na tabela `LogAcesso`.
- **Critério de Aceitação:** Sistema consegue identificar um usuário cadastrado no banco de dados em menos de 2 segundos e registrar o evento no log.

### Sprint 4: Níveis de Acesso e Painel
- **Objetivo:** Implementar as regras de negócio para os diferentes níveis de acesso e criar o painel de visualização de logs.
- **Tarefas:**
  1.  **Middleware de permissão:** Criar um middleware ou decorador em Django para verificar o `nivel_acesso` do usuário autenticado.
  2.  **Restringir acesso:** Bloquear/liberar funcionalidades com base no nível de acesso.
  3.  **Criar painel de logs:** Desenvolver uma view no app `painel` que lista os registros da tabela `LogAcesso`.
  4.  **Proteger painel de logs:** Garantir que apenas usuários de **Nível 3** possam acessar essa view.
- **Critério de Aceitação:** Usuários de Nível 1 e 2 são bloqueados de ver os logs. Usuário de Nível 3 consegue visualizar a lista de todos os acessos.

### Sprint 5: Testes e Refatoração
- **Objetivo:** Garantir a qualidade e estabilidade do sistema.
- **Tarefas:**
  1.  **Testes unitários:** Escrever testes para as funcionalidades.
  2.  **Testes de integração:** Simular o fluxo completo.
  3.  **Refatoração:** Limpar o código e otimizar a performance.
  4.  **Documentação:** Atualizar o `README.md`.
- **Critério de Aceitação:** Cobertura de testes acima de 80%. Sistema funcionando de ponta a ponta sem erros.