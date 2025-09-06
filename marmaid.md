flowchart TD

    %% Início
    A[Usuário acessa sistema] --> B[E-mail + Senha]

    %% Login
    B -->|Credenciais inválidas| X[Erro: Acesso negado<br/>Log de falha]
    B -->|Credenciais corretas| C[Abre câmera para reconhecimento facial]

    %% Reconhecimento
    C -->|Rosto não reconhecido| Y[Erro: Rosto não autorizado<br/>Log de falha]
    C -->|Rosto reconhecido| D[Verificar nível de acesso]

    %% Níveis de acesso
    D -->|Nível 1| E[Acesso geral liberado<br/>Log de sucesso]
    D -->|Nível 2| F[Acesso restrito (Diretores)<br/>Log de sucesso]
    D -->|Nível 3| G[Acesso exclusivo Ministro<br/>Pode consultar logs]

    %% Logs
    E --> H[Registrar log no Banco de Dados]
    F --> H
    G --> H
    X --> H
    Y --> H

    H --> Z[Fim do processo]
