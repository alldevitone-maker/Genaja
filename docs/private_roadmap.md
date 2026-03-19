Fase 0 — Congelar a base atual

Antes de mexer em feature nova, você já fez o mais importante: definir o novo nome e a nova estrutura. Agora o objetivo é congelar a v0.3.0-dev como base de reorganização.

O que fazer:

confirmar nome oficial do produto: Genaja

confirmar empresa/organização: JGDA

considerar a v0.3.0-dev como a versão da reorganização e renomeação

guardar o arquivo antigo e a estrutura antiga como referência histórica, sem continuar desenvolvendo neles

Fase 1 — Organizar a estrutura do projeto

Essa fase vem antes de qualquer melhoria funcional.

Objetivo:

deixar o projeto com estrutura limpa

garantir que tudo que é código fique no src

manter data, logs, backups e arquivos de documentação fora do src

Estrutura-alvo:

src/ para o código atual

data/ para arquivos de entrada e saída de teste

logs/ para logs

backups/ para cópias antigas

README.md para visão geral

CHANGELOG.md para histórico de versões

main.py como ponto de entrada

Fase 2 — Consolidar a refatoração

Antes de criar novas features, validar que a versão reorganizada funciona.

Objetivo:

garantir que a UI abre

garantir que leitura de Excel continua funcionando

garantir que configuração, mapeamento, sincronização e salvamento continuam corretos

confirmar que a refatoração não quebrou nada

Essa fase é importante porque não vale adicionar recurso novo em base instável.

Fase 3 — Implementar a feature do checkbox

Só depois da estrutura e da validação da base.

Seu roteiro dessa feature está bom. Eu reorganizaria assim:

3.1 Definir o comportamento funcional

Antes de pensar em interface, deixar a regra fechada:

Quando o usuário ativar a opção:

o arquivo final deve conter apenas:

a chave do SAP

as colunas de destino efetivamente mapeadas

Quando desativar:

o arquivo final permanece completo

3.2 Definir o objetivo da experiência do usuário

A feature não é só técnica. Ela serve para:

reduzir ruído no arquivo final

facilitar integração posterior

gerar saída mais limpa

dar controle ao usuário

3.3 Adicionar o controle visual

Depois da regra definida:

incluir o checkbox em local visível

deixar o texto claro

evitar que pareça uma opção técnica confusa

3.4 Integrar a lógica no momento certo do fluxo

A regra deve entrar apenas no final do processamento, pouco antes da gravação do arquivo. Assim:

você não interfere no ETL principal

não quebra cálculo intermediário

a filtragem vira uma etapa final de apresentação/saída

3.5 Tratar falhas de forma segura

Essa parte é essencial:

validar se as colunas esperadas realmente existem

evitar quebra total por coluna ausente

registrar no log o que aconteceu

manter previsibilidade

3.6 Logar a decisão do usuário

O log precisa deixar claro:

se a saída foi completa

se a saída foi reduzida

quais colunas ficaram, quando fizer sentido

3.7 Validar com cenários pequenos

Primeiro testar em casos simples:

saída completa

saída reduzida

chave preservada

nenhuma coluna essencial perdida

3.8 Registrar a mudança como versão funcional

Essa feature já merece virar uma próxima evolução da versão, algo como:

v0.3.1-dev se for só ajuste incremental

ou v0.4.0-dev se você considerar que é a primeira melhoria funcional relevante após a reorganização

Minha sugestão: v0.3.1-dev.

Quando subir para o GitHub

Não sobe agora no meio da bagunça.
Sobe quando o projeto estiver minimamente estável.

O melhor ponto é este:

estrutura organizada

imports funcionando

projeto abrindo e rodando

README básico pronto

backup antigo guardado

primeira validação da nova base concluída

Aí sim faz sentido subir.

Ou seja: GitHub entra depois da estabilização da base reorganizada, não antes.

O que colocar no GitHub na primeira subida

Na primeira publicação, subir:

a estrutura nova

o código atual funcional

README básico

CHANGELOG inicial

.gitignore adequado

sem arquivos pesados de teste desnecessários

sem planilhas sensíveis

sem logs temporários inúteis

Não usar o GitHub como depósito de tudo. Ele deve receber o projeto limpo.

Onde guardar as versões antigas

Na sua estrutura, eu guardaria assim:

backups/
├── pre-genaja/
│   └── arquivos_da_fase_antiga
├── v0.3.0-dev/
│   └── snapshot_da_base_renomeada
Como pensar nisso

pre-genaja/ = era anterior ao nome novo

v0.3.0-dev/ = primeira base com identidade nova

versões futuras podem ter snapshots pontuais, mas sem exagero

O que fazer com o backup antigo

O backup antigo não deve continuar “vivo” como fonte principal. O papel dele é:

servir de referência histórica

permitir comparação se algo quebrar

ajudar a recuperar função perdida

funcionar como segurança antes de apagar arquivos antigos

O que não fazer com ele:

continuar editando em paralelo

usar como segunda versão ativa

deixar misturado com o código novo

Em resumo: backup é arquivo morto útil, não projeto paralelo.

README e releases

Eu organizaria assim:

README.md

Coloca:

nome do projeto

objetivo

status atual

estrutura de pastas

como rodar

roadmap resumido

CHANGELOG.md

Coloca:

v0.3.0-dev → reorganização, renomeação, nova identidade

próximas versões com novas features

Releases no GitHub

Só começam a fazer mais sentido quando:

o repositório já estiver publicado

você tiver um marco estável para marcar

Então a ordem ideal é:

arrumar projeto

subir GitHub

depois criar tags/releases

Roteiro reorganizado final
Etapa 1

Congelar a base atual como v0.3.0-dev e guardar o legado em backups/.

Etapa 2

Finalizar a estrutura de pastas e garantir que só a versão nova siga em frente.

Etapa 3

Validar que a refatoração roda inteira sem quebrar fluxo.

Etapa 4

Criar README.md, CHANGELOG.md e limpar o projeto para publicação.

Etapa 5

Subir a base reorganizada para o GitHub.

Etapa 6

Implementar a feature do checkbox “manter apenas colunas selecionadas”.

Etapa 7

Validar a feature com testes simples e registrar a próxima versão.

Etapa 8

Seguir para novas features, menus e configurações mais avançadas.

Minha recomendação de próxima ação: primeiro fechar a Etapa 1 e a Etapa 2 de vez, antes de pensar no checkbox.