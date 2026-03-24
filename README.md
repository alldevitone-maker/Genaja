# Genaja - Sincronização Inteligente de Dados

[🇺🇸 English](README.en.md) | [🇧🇷 Português](README.md)

Bem-vindo ao **Genaja**, a sua ferramenta definitiva para cruzar e limpar planilhas empresariais de forma 100% autônoma e à prova de falhas.

## 🚀 O que o Genaja faz?
O Genaja substitui horas de trabalho manual no Excel (PROCVs complexos e tratamento de lixo em relatórios) por um processo de apenas 3 passos:
1. **Mapeamento Ágil:** Conecta duas planilhas diferentes baseadas em um código comum (Chave Primária).
2. **Transferência Inteligente:** Cria automaticamente as colunas que estão faltando em um relatório a partir do outro.
3. **Faxina & Comparador:** O sistema atua como um canivete suíço para tabelas:
    - Um poderoso limpador que remove furos (quantidades nulas e não utilizadas), corrige pontuações, remove espaços extras invisíveis e coloca textos alinhados.
    - E um Módulo extra de Comparação que avaliza em 1 milissegundo de forma exata todos os produtos/linhas que ficaram de fora, existindo em uma base sem ter surgido na outra.

## 🛠️ Como Iniciar
Se você já possui o Python instalado e deseja utilizar diretamente do repositório:
1. Abra seu terminal na pasta do projeto e instale a dependência matricial:
   ```bash
   pip install pandas openpyxl
   ```
2. Execute a Interface Gráfica com um único clique (ou comando):
   ```bash
   python src/main.py
   ```

## 📖 Histórico de Atualizações (O Valor em Tempo Real do Genaja)

> **Versão Atual:** `v0.4.7` (The Premium Update & Big Data O(1))  
> **Status do Projeto:** Ativo - Evolução Constante de Módulos

**v0.4.7 (The Premium Update & Big Data O(1))**
A interface corporativa alcançou o nível Premium. O sistema agora conta com um motor de **Tooltips Flutuantes** (Dicas visuais) detalhando funções complexas de negócio para novos analistas. Toda a tela recebeu um **Global Canvas Scroll** para exibir o HUB corretamente em laptops de 14 polegadas. Introduzimos os quadros "Experimentais" vermelhos com suporte bruto a Big Data (`JSON`, `CSV`, `SQL`). Além disso, o motor de junção do Pandas foi reescrito para proteger (Safe-Merge) colunas com nomes idênticos contra corrupção invisível (Arquivos Vazios). E como bônus, implementado um Botão de **Reiniciar App** via Sistema Operacional para limpar a memória RAM imediatamente ao cometer erros de mapeamento da Chave.

**v0.4.6 (O Retorno do Hub Unificado Flex & Opcionalidade)**
Refatoração de arquitetura unindo o Genaja em uma super-tela (Hub Único) sem perder as dezenas de funcionalidades (Auditor/GAPS) construídas nas versões passadas. O botão de **Chave A1 Protegida** tornou-se ativável por Checkbox ("Ativar"), destravando fluxos automáticos para usuários que não querem a obrigatoriedade da fixação posicional em relatórios.

**v0.4.4 (Internationalization & i18n)**
Alcance global desbloqueado. Adicionadas as documentações de arquitetura, manuais de negócio e um histórico dinâmico de rastreio totalmente em inglês e português, utilizando links cruzados para abraçar contribuições externas.

**v0.4.3 (Experiência do Usuário & Docs)**
A "vitrine" do aplicativo foi reformulada. A linguagem enraizada em jargões complexos deu lugar a uma explicação focada nas reais facilidades para a empresa. Um arquivo exclusivo avançado foi escondido apenas para eventuais analistas de TI. E toda a experiência passou a focar na facilidade.

**v0.4.2 (O Comparador Pro)**
Implementado o poderoso Hub de Abas na ferramenta. Entra no ar o "Mapeamento em Sentido Contrário", localizando itens presentes em relatórios de sistema externo que deixaram de baixar/existir misteriosamente para a sua base corporativa real, gerando extração super filtrada à ponta de um botão.

**v0.4.1 (Corretivo de Blindagem em Bases Textuais de Alta Similaridade Numérica)**
Evitado cenários drásticos onde colunas como códigos internos preenchidos por zeros fossem sumariamente varridos de relatórios de predição, engessando ainda mais as travas que te blindam de exportar lixos, mantendo dados inegociáveis.

**v0.4.0 (A Era do Auto-Clique)**
Retirada manual das caixas de anotação na ferramenta para seleções de transferência nativas e inteligentes na tela. Inserido o filtro cruzado que remove lixos apenas se estritamente inútil para todas as ramificações analíticas que você escolheu. 

*(A documentação de arquitetura detalhada para analistas e TI localiza-se na pasta isolada `docs/`)*