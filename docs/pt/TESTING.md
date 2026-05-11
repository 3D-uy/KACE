# Guia de Testes do KACE

Este documento explica como executar a suíte de testes do KACE, o que cada modo faz, como o sistema de snapshots funciona e como o pipeline de CI é estruturado.

---

## Início Rápido

```bash
# Executar a suíte de testes completa (unitários + regressão)
python3 tests/run_tests.py

# Verbose — ver cada nome de teste e PASS/FAIL
python3 tests/run_tests.py --verbose

# Validar o esquema e a precedência do data/boards.yaml
python3 tests/run_tests.py --yaml-check

# Atualizar os golden snapshots após uma mudança de saída intencional
python3 tests/run_tests.py --update-snapshots

# Executar a varredura completa de mais de 192 configs do Klipper (requer rede + git)
python3 tests/run_tests.py --full-klipper-sweep
```

---

## Categorias de Testes

### Testes Unitários — `tests/unit/`

Testes rápidos e isolados, sem dependências externas. Cada teste simula (mock) tudo o que exigiria acesso à rede, prompts interativos ou hardware.

| Arquivo | O que testa |
|------|--------------|
| `test_derivation.py` | Lógica de derivação MCU → Kconfig, correspondência de padrões, fallback |
| `test_yaml_db.py` | Carregamento de YAML, validação da ordem dos padrões, recuperação de YAML corrompido |
| `test_scraper.py` | Injeção de pinos BLTouch a partir da correspondência de nomes de arquivos |
| `test_deployer.py` | Instalação tardia (lazy) do paramiko, tratamento de falhas de rede/offline |

### Testes de Regressão — `tests/regression/`

Testes baseados em snapshots que renderizam um `printer.cfg` completo a partir de uma configuração simulada do Klipper e o comparam byte a byte com um arquivo golden fixture.

| Arquivo | Placas cobertas |
|------|---------------|
| `test_config_generation.py` | SKR v1.4 (LPC1769) |
| `test_snapshot_expansion.py` | Creality v4.2.2, Creality v4.2.7, Octopus v1.1, SKR Pico (RP2040), SKR v1.3 (LPC1768), SKR Mini E3 sensorless |

---

## Sistema de Snapshots

Snapshots são arquivos de saída "golden" armazenados em `tests/fixtures/*.txt`. Cada arquivo contém a saída esperada do `printer.cfg` para uma placa + configuração específica.

### Como funciona a comparação

`KaceTestCase.assertSnapshot()` em `tests/kace_test_case.py`:

1. Gera um `printer.cfg` a partir de dados simulados em um arquivo temporário.
2. Lê o conteúdo do arquivo temporário.
3. Remove espaços em branco ao final de cada linha.
4. Compara o conteúdo limpo com o arquivo golden armazenado.
5. Falha com um diff claro se qualquer caractere for diferente.

A remoção de espaços em branco torna as comparações estáveis entre plataformas (Windows CRLF vs Linux LF) sem esconder diferenças reais.

### Atualizando snapshots intencionalmente

Execute com `--update-snapshots` quando fizer uma mudança **deliberada** no formato de saída:

```bash
python3 tests/run_tests.py --update-snapshots
```

Isso sobrescreve os arquivos golden. Sempre:
1. Revise o git diff de cada arquivo de fixture alterado.
2. Verifique se as mudanças são o que você pretendias.
3. Commite os snapshots atualizados junto com a alteração do código.

> **Nunca** atualize snapshots silenciosamente como parte de uma alteração não relacionada. Uma mudança de snapshot é uma mudança de contrato.

### Adicionando um novo snapshot

1. Adicione um novo método de teste em `tests/regression/test_snapshot_expansion.py` seguindo o padrão existente.
2. Execute `python3 tests/run_tests.py --update-snapshots` para gerar o fixture.
3. Execute `python3 tests/run_tests.py --verbose` para confirmar que o novo teste passa.
4. Commite tanto o teste quanto o arquivo de fixture.

---

## Verificação de Integridade do YAML

```bash
python3 tests/run_tests.py --yaml-check
```

Esta verificação independente valida o `data/boards.yaml` sem executar nenhum teste:

- Chaves de nível superior (`boards`, `mcu_firmware`) devem estar presentes.
- Cada entrada em `boards[]` deve ter `mcu`, `search_terms` e `bltouch`.
- Cada entrada em `mcu_firmware[]` deve ter `pattern` e `arch`.
- Nenhum padrão genérico pode sobrepor um padrão mais específico que apareça depois (validação de precedência).

Código de saída 0 = válido, código de saída 1 = erros encontrados com detalhes impressos.

---

## Varredura Completa do Klipper

```bash
python3 tests/run_tests.py --full-klipper-sweep
```

A varredura:
1. Clona o repositório do Klipper com `--depth 1 --sparse` (apenas config/).
2. Itera por cada `generic-*.cfg` e `printer-*.cfg`.
3. Executa `parse_config()` + `extract_profile_defaults()` em cada um.
4. Classifica o resultado:

| Código | Significado |
|------|---------|
| `PASS` | Parse completo + extração bem-sucedidos |
| `SAFE_ABORT` | Pinos de espaço reservado TODO encontrados — limitação graciosa conhecida |
| `UNSUPPORTED` | Seções experimentais/não suportadas presentes |
| `FAILURE` | Exceção Python não tratada — requer investigação |

5. Imprime uma tabela de estatísticas final.
6. Sai com código 1 se algum resultado `FAILURE` for registrado.

A varredura requer `git` no `PATH` e acesso à rede. Ela roda automaticamente em cada push para a `main` via GitHub Actions, mas é ignorada em PRs para manter a iteração dos contribuidores rápida.

---

## Visão Geral do Pipeline de CI

O workflow do GitHub Actions em `.github/workflows/ci.yml` roda em cada push para a `main` e em cada pull request.

```
push / PR
    │
    ├── lint              — python -m py_compile (checa sintaxe de todos os arquivos .py)
    │
    ├── unit-tests        — roda a suíte de testes completa (21 testes)
    │
    ├── yaml-integrity    — checagem de esquema + precedência do boards.yaml
    │
    ├── regression-tests  — comparação de snapshots (bloqueia merge em caso de diff)
    │       └── needs: [unit-tests, yaml-integrity]
    │
    └── full-klipper-sweep  (push para a main APENAS)
            └── needs: regression-tests
```

Todos os jobs usam cancelamento por `concurrency` — se você enviar vários commits rapidamente para o mesmo PR, as execuções de CI mais antigas são canceladas automaticamente.

### Regras de bloqueio

Merges para a `main` são bloqueados se qualquer um dos seguintes jobs falhar:
- `lint`
- `unit-tests`
- `yaml-integrity`
- `regression-tests`

A `full-klipper-sweep` é informativa na main (não bloqueia PRs).

---

## Design com Zero Dependências

O executor de testes usa apenas módulos da biblioteca padrão do Python:

```
unittest, sys, os, time, argparse, subprocess, tempfile, re
```

Isso significa que as testes podem rodar em um Raspberry Pi Zero 2W sem instalações de pip além do `requirements.txt` do próprio projeto. A suíte completa termina em menos de 0,5 segundos em hardware comum.
