# PRD – Sistema de Reconhecimento Facial para Cofre

## 1. Objetivo
Criar um sistema de reconhecimento facial que funcione como controle de acesso a um cofre de alta segurança, garantindo que somente usuários autorizados possam acessá-lo. O sistema terá níveis de permissão hierárquicos e rodará em servidor local.  

---

## 2. Escopo
### Incluso
- Cadastro de usuários com: nome, e-mail, ID de crachá e foto (via upload).  
- Reconhecimento facial automático utilizando **biblioteca OpenCV (cv2)**.  
- Esquema de permissões em 3 níveis.  
- Logs de tentativas de acesso (apenas sucesso/falha).  
- Módulo de alertas simples (Bootstrap).  
- Painel administrativo para gerenciamento (apenas 1 administrador geral).  

### Excluído
- Métodos de autenticação adicionais (senha, biometria etc.).  
- Controle físico direto do cofre (trava eletrônica).  
- Integrações externas (outros sistemas de segurança).  

---

## 3. Níveis de Acesso
- **Nível 1 – Geral:** usuários cadastrados com permissão básica de acesso.  
- **Nível 2 – Diretores de Divisão:** acesso restrito, registrado em log.  
- **Nível 3 – Ministro do Meio Ambiente:** acesso exclusivo e capacidade de consultar logs.  

---

## 4. Requisitos Funcionais
1. O sistema deve permitir cadastro de usuários (nome, e-mail, ID crachá, foto).  
2. O sistema deve autenticar rostos em tempo real a partir de câmera conectada ao servidor.  
3. O sistema deve conceder ou negar acesso com base no nível de permissão.  
4. O sistema deve registrar todas as tentativas de acesso (sucesso/falha) em log.  
5. O sistema deve exibir um **alerta em Bootstrap** em caso de tentativa de acesso não autorizado.  
6. O sistema deve permitir que apenas o **usuário Nível 3** consulte os registros de log.  
7. O administrador geral deve poder adicionar, editar ou remover usuários.  

---

## 5. Requisitos Não Funcionais
- **Plataforma:** rodar em **servidor local** (Linux ou Windows).  
- **Dependências:** OpenCV (cv2) para reconhecimento facial.  
- **Segurança:** banco de dados protegido com senha; fotos armazenadas de forma organizada.  
- **Performance:** autenticação em até **2 segundos** por tentativa.  
- **Disponibilidade:** não necessita alta disponibilidade (uso em ambiente restrito).  
- **Escalabilidade:** até **500 usuários cadastrados**.  

---

## 6. Tecnologias
- **Backend:** Python (Flask ou FastAPI).  
- **IA/Visão Computacional:** OpenCV (cv2).  
- **Banco de Dados:** SQLite ou MySQL (dependendo da simplicidade necessária).  
- **Frontend/Admin:** HTML, CSS, Bootstrap para alertas e interface simples.  
- **Dispositivo:** câmera conectada a maquina.  

---

## 7. Critérios de Aceitação
- Sistema autentica corretamente pelo menos **95% dos usuários cadastrados**.  
- Sistema rejeita **100% de usuários não cadastrados**.  
- Logs armazenam todas as tentativas (sucesso/falha) com data e hora.  
- Usuário de **Nível 3** consegue acessar relatórios de log.  
- Tempo de resposta inferior a **2 segundos**.  
