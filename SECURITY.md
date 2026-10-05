# Security Notes — Aurora TMS

## Escopo

Este repositório é um projeto educacional e de portfólio, projetado para execução local e laboratório.

## Antes de publicar

- não versionar bancos SQLite, logs, credenciais, tokens ou arquivos de ambiente;
- manter `AURORA_DATABASE_URL` fora do código quando usar outro ambiente;
- não colocar dados reais de clientes, motoristas, documentos ou cargas em uma demonstração pública;
- revisar as regras de negócio antes de usar o sistema em produção.

## Estado atual

A API não possui autenticação/autorização abrangente por perfil de usuário. Também faltam rate limiting, migrações formais, gestão de segredos e hardening de produção.

Essas limitações estão registradas como parte do roadmap técnico.
