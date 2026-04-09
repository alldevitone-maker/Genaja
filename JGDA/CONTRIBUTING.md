# Guia de Contribuição — Genaja (Engineering Standards)

Bem-vindo ao Genaja. Este projeto mantém padrões rigorosos de engenharia de software para garantir escalabilidade, segurança e interoperabilidade.

## 🏛️ Princípios de Arquitetura

1. **Desacoplamento Total**: A lógica de negócio reside exclusivamente nos `Engines` e `Services`. As views do Flet devem ser puramente declarativas (`Stateless-ish`).
2. **Registry Pattern**: Novos conectores devem herdar de `BaseConnector` e ser registrados via `ConnectorFactory`.
3. **Governança de Versão**: Todo novo módulo ou refatoração profunda deve implementar o `version_hook.py`.

## 🛠️ Workflow de Desenvolvimento

### 1. Ambiente Clean
O desenvolvimento deve ocorrer isolado de dados reais. Utilize a pasta `tests/index/` para datasets de teste.

### 2. Ciclo de Validação
Antes de qualquer submissão, é obrigatório rodar o pipeline de automação:
```bash
python scripts/automate.py --quick
```

### 3. Padrão de Commits
- Use mensagens claras e técnicas.
- Tags de versão são geradas automaticamente via `automate.py --release`.

## 🎨 Estilo de UI (Platinum Style)
- Utilize exclusivamente os tokens do `PlatinumTheme`.
- O uso de cores hexadecimais "hardcoded" nas views é proibido.
- Micro-interações (hovers, loaders) são obrigatórias em botões de processamento pesado.

---
*Este guia visa garantir que o Genaja permaneça um software de classe mundial.*
