# Contribuindo para o KACE

Obrigado por considerar uma contribuição para o KACE.
Este guia explica como adicionar novas placas, criar snapshots e enviar PRs seguros.

---

## Configuração de Desenvolvimento

```bash
git clone https://github.com/3D-uy/kace.git
cd kace
pip install -r requirements.txt
```

Execute a suíte de testes para verificar seu ambiente:

```bash
python3 tests/run_tests.py --verbose
```

Todos os 21 testes devem passar antes que qualquer contribuição seja aceita.

---

## Adicionando uma Nova Placa

Os dados das placas do KACE residem inteiramente em `data/boards.yaml`. Adicionar uma nova placa
requer **apenas uma edição no YAML** — nenhuma alteração em Python é necessária.

### Passo 1 — Adicionar a placa em `boards[]`

Encontre (ou crie) o grupo `mcu` correto e adicione o termo de busca da sua placa:

```yaml
boards:
  - mcu: stm32f103
    search_terms:
      - creality-v4.2.2
      - creality-v4.2.7
      - skr-mini-e3
      - sua-nova-placa      # ← adicione aqui
    bltouch:
      sua-nova-placa:       # ← sub-string do nome do arquivo de configuração do Klipper
        sensor_pin: "^PA7"  # Pino Z-min com pull-up se necessário
        control_pin: "PB0"  # Pino de servo/controle
```

As entradas da lista `search_terms` devem ser sub-strings do nome oficial do arquivo de
configuração do Klipper (ex: `generic-sua-nova-placa.cfg` → `sua-nova-placa`).

Se sua placa usa um MCU diferente que ainda não está listado, adicione uma nova entrada em `boards[]`
com o valor de `mcu` correto de `firmware/detector.py`.

### Passo 2 — Verificar se o padrão de firmware existe

Verifique se `mcu_firmware[]` possui um padrão para a família MCU da sua placa.
Se sua placa usa `stm32f103`, `stm32f4`, `lpc1769` ou `rp2040` — ela já está coberta. Se precisar de uma nova família de MCU, adicione uma nova entrada:

```yaml
mcu_firmware:
  - pattern: "seu-novo-mcu"   # deve estar antes de qualquer padrão pai genérico
    arch: stm32
    mach: STM32
    flash_start: "0x8000"
    set_mcu_flag: true
```

> **A ordem importa.** Padrões mais específicos devem aparecer antes dos genéricos.
> Execute `python3 tests/run_tests.py --yaml-check` para validar a precedência.

### Passo 3 — Validar o YAML

```bash
python3 tests/run_tests.py --yaml-check
```

Isso verifica o esquema, os campos obrigatórios e a ordem dos padrões. Corrija quaisquer erros antes de continuar.

### Passo 4 — Adicionar um snapshot de regressão

Crie uma string de configuração simulada em `tests/regression/test_snapshot_expansion.py`
seguindo os exemplos existentes:

```python
MOCK_SUA_PLACA = """
[stepper_x]
step_pin: PA0
...
"""

def test_sua_placa_snapshot(self):
    """Snapshot de regressão para Sua Placa (STM32Fxxx)."""
    self._run_snapshot(
        "sua-placa-esperada",
        MOCK_SUA_PLACA,
        "generic-sua-nova-placa.cfg",
        "/dev/serial/by-id/usb-Klipper_stm32fxxx_mock-if00",
    )
```

Gere o golden fixture:

```bash
python3 tests/run_tests.py --update-snapshots
```

Verifique se o snapshot parece correto e, em seguida, execute a suíte completa:

```bash
python3 tests/run_tests.py --verbose
```

### Passo 5 — Enviar seu PR

Todos os mais de 21 testes devem passar. O pipeline de CI será executado automaticamente no seu PR.

---

## Checklist do PR

Antes de abrir um PR, verifique o seguinte:

- [ ] `python3 tests/run_tests.py --verbose` → todos os testes passam
- [ ] `python3 tests/run_tests.py --yaml-check` → YAML válido
- [ ] Arquivos de snapshot commitados junto com as alterações de código (se a saída mudou)
- [ ] Seção `[Unreleased]` do `CHANGELOG.md` atualizada
- [ ] Nenhuma string em inglês hardcoded adicionada à UI (use `t()` de `core/translations.py`)
- [ ] Nenhuma chamada `sys.exit()` adicionada fora do ponto de entrada `kace.py`
- [ ] Nenhuma nova dependência externa adicionada sem discussão

---

## Estilo de Código

- Recursos do Python 3.11+ são bem-vindos.
- Siga os padrões existentes em cada módulo — nada de novas camadas de abstração.
- Todos os dados das placas vão em `data/boards.yaml`, não no Python.
- Todas as strings voltadas para o usuário passam por `t()`, não hardcoded.
- Todos os novos módulos que carregam dados opcionais devem ter um dicionário de fallback hardcoded.

---

## Congelamento de Arquitetura

A arquitetura principal é intencionalmente estável. Por favor, não proponha:

- Novas camadas de abstração em `core/` ou `firmware/`
- Mudanças de esquema no `boards.yaml` sem discussão
- Mudanças no template Jinja2 que quebrem silenciosamente os snapshots existentes

Se uma grande refatoração for necessária, abra primeiro uma issue descrevendo a motivação.

---

## Obtendo Ajuda

Abra uma issue no [GitHub](https://github.com/3D-uy/kace/issues) com:
- O modelo da sua placa
- O nome do arquivo de configuração do Klipper (`generic-xxx.cfg`)
- O chip MCU da sua placa
- O que o KACE gera atualmente vs o que você espera
