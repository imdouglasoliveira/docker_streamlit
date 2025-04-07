# Docker Streamlit Deploy Docker Swarm VPS

## Visão Geral

Este repositório contém uma solução padronizada para o deploy de aplicações conteinerizadas utilizando Docker e Python. A estrutura foi projetada para facilitar a reutilização em múltiplos projetos, permitindo que apenas alguns ajustes (como renomear e alterar configurações específicas) sejam necessários para adaptar a solução ao novo contexto.

## Estrutura do Repositório

- **deploy.py**: Automatiza o processo de deploy, realizando as seguintes etapas:
  - Verificação do ambiente (espaço em disco e limpeza de recursos Docker).
  - Atualização do código (Git reset e pull).
  - Atualização de configurações (flags de produção e versionamento).
  - Registro do timestamp do deploy (em `last_deploy.txt`).
  - Construção da imagem Docker e deploy do serviço via Docker Stack.
  
- **docker-compose.yaml**: Arquivo de configuração do Docker Compose, que define:
  - A imagem do serviço.
  - Redes e volumes necessários.
  - Regras de deploy e labels para integração com ferramentas de roteamento (ex.: Traefik).
  
- **config/config.py**: Arquivo onde estão definidas as configurações do ambiente (ex.: flag de produção, versão do projeto).
- **last_deploy.txt**: Arquivo que registra a data e hora do último deploy realizado.

## Pré-requisitos

- **Docker e Docker Swarm**: Necessário para orquestração dos containers.
- **Python 3.7+**: Para executar o script de deploy.
- **Git**: Para atualização do código.
- **Traefik (opcional)**: Se for utilizado para roteamento reverso com TLS.

## Instalação e Configuração

1. **Clone o Repositório:**
   ```bash
   git clone <URL_do_repositório>
   cd <nome_do_repositório>

## Considerações Finais

Esta padronização permite que você utilize a mesma base para diversos projetos, bastando:
- **Renomear** arquivos específicos;
- **Ajustar** as configurações e parâmetros conforme o ambiente ou particularidades do novo projeto.

A estrutura e os scripts fornecidos garantem que o processo de deploy seja automatizado, consistente e fácil de manter, economizando tempo em novos projetos e garantindo maior confiabilidade no deploy.
