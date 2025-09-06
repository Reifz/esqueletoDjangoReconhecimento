# Plano Técnico – Sistema de Reconhecimento Facial

## 1. Arquitetura
- **Framework Backend:** Django (sólido, escalável e integra banco de dados e templates).  
- **Frontend:** Django Templates + Bootstrap (interface web simples).  
- **Servidor:** Localhost para desenvolvimento. Futuramente, pode ser configurado em servidor dedicado.  

---

## 2. Banco de Dados
- **Banco escolhido:** MySQL (com suporte a phpMyAdmin).  
- **Entidades principais:**
  - **Usuário:** `id`, `nome`, `email`, `id_cracha`, `foto(s)`, `nivel_acesso`.  
  - **LogAcesso:** `id`, `usuario`, `resultado` , `data_hora`.  
- **Motivo:** MySQL é robusto, fácil de rodar no localhost e gerenciável via phpMyAdmin.  

---

## 3. Reconhecimento Facial
- **Biblioteca:** DeepFace (mais precisa que OpenCV puro, fácil de integrar com Django).  
- **Estratégia de armazenamento:** salvar foto original + **embedding do rosto** (vetor numérico) no banco para consultas rápidas.  
- **Fluxo:** Captura da câmera → processamento → comparação com embeddings → autenticação.  

---

## 4. Cadastro de Usuários
- **Módulo Web (Django Admin customizado + tela simples):**
  - Nome, e-mail, ID do crachá.  
  - Upload de 1 a N fotos por usuário (quanto mais fotos, melhor o treinamento do reconhecimento).  
  - Geração automática de embedding(s) no momento do cadastro.  
- **Validação:** cada ID de crachá deve ser único.  

---

## 5. Fluxo de Acesso
1. Usuário digita e-mail e senha.  
2. Se válido, abre câmera para captura do rosto.  
3. Comparação do rosto com banco de embeddings.  
4. Se correspondência encontrada → verifica nível de acesso:
   - Nível 1 → Acesso geral.  
   - Nível 2 → Acesso restrito (diretores).  
   - Nível 3 → Acesso exclusivo + acesso aos logs.  
5. Tudo é registrado na tabela **LogAcesso**.  

---

## 6. Logs
- Armazenados apenas no banco de dados.  
- Apenas usuários **Nível 3** podem visualizar logs.  
- Não há exportação de CSV/PDF nesta versão.  

---

## 7. Alertas
- Mensagens visuais em tela via **Bootstrap** (success/danger).  
- Não há alertas sonoros ou envio de e-mails nesta versão.  

---

## 8. Estrutura do Projeto (Django)
- **App `usuarios`** → cadastro e gerenciamento de usuários.  
- **App `acessos`** → fluxo de reconhecimento facial, verificação de permissões e logs.  
- **App `painel`** → dashboard restrito (logs acessíveis apenas por Nível 3).  

---

## 9. Tecnologias e Dependências
- **Python 3.10+**  
- **Django 4+**  
- **MySQL + phpMyAdmin**  
- **DeepFace** (reconhecimento facial)  
- **OpenCV** (captura de câmera)  
- **Bootstrap 5** (frontend simples)  

---

## 10. Critérios de Sucesso
- Cadastro de usuários com upload de foto funcionando.  
- Reconhecimento facial com resposta em até **2 segundos**.  
- Logs gravados corretamente no banco.  
- Diferenciação clara entre níveis de acesso 1, 2 e 3.  
- Apenas Nível 3 consegue consultar logs.  
