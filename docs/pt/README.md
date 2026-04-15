<p align="center">
  <img src="../assets/kace_banner.png" width="1000">
</p>

<h1 align="center">🚀 KACE — Klipper Automated Configuration Ecosystem</h1>

<p align="center">
  <img src="https://img.shields.io/badge/status-beta-orange?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/version-v0.1.0--beta-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20Raspberry%20Pi-green?style=flat-square" alt="Platform">
  <img src="https://img.shields.io/github/license/3D-uy/KACE?style=flat-square" alt="License">
  ![CI](https://github.com/3D-uy/kace/actions/workflows/test.yml/badge.svg)
</p>

<p align="center">
🌐 <strong>Idioma</strong><br>
🇺🇸 <a href="../../README.md">English</a> | 🇪🇸 <a href="../es/README.md">Español</a> | 🇧🇷 Português
</p>

> [!WARNING]
> **KACE está atualmente em Beta.** As funcionalidades principais estão funcionando, mas você pode encontrar bugs ou irregularidades.
> Sempre revise os arquivos gerados antes de usá-los. Reporte problemas usando o template [Bug Report](../../.github/ISSUE_TEMPLATE/bug_report.md).

---

## ⚡ Instale o Klipper sem dor de cabeça

O KACE automatiza todo o processo de configuração do **Klipper**, desde a detecção de hardware até a compilação de firmware e geração de configuração pronta para uso.

👉 Menos erros  
👉 Menos tempo  
👉 Mais impressão

---

## 🧠 O que é KACE de verdade?

É um **motor inteligente de configuração e firmware** que:

- 🔍 Detecta automaticamente seu hardware (MCU)
- 🧠 Interpreta seu sistema sem configurações manuais
- ⚙️ Gera um `printer.cfg` pronto para uso
- 🔥 Compila o firmware automaticamente (`klipper.bin`)
- 🧭 Te guia apenas quando necessário

---

## 🎯 Por que KACE?

Configurar o Klipper manualmente envolve:

- erros no firmware
- configs incompatíveis
- passos complexos e confusos

**O KACE elimina tudo isso:**

- ✅ Automatiza decisões técnicas complexas
- ✅ Reduz erros críticos
- ✅ Funciona com configurações reais do Klipper
- ✅ Minimiza a interação do usuário

---

## 🟡 Status do Projeto — Beta 1

> O KACE está atualmente em **beta ativo**. As funcionalidades principais estão funcionando, mas podem haver irregularidades.

| Funcionalidade | Status |
|---|---|
| Auto-detecção de MCU | ✅ Funcionando |
| GitHub Scraper | ✅ Funcionando |
| Geração de `printer.cfg` | ✅ Funcionando |
| Compilação de Firmware | ✅ Funcionando |
| Deploy via SSH | ✅ Funcionando |
| Instalação em uma linha | ✅ Funcionando |

---

## ⚡ Instalação em uma linha

```bash
bash <(curl -s https://raw.githubusercontent.com/3D-uy/KACE/main/install.sh)
```

> Isso instalará todas as dependências, clonará o repositório e configurará o comando global `kace` automaticamente.

---

## 📋 Requisitos

Antes de usar o KACE:

✔ Raspberry Pi Imager instalado no cartão SD: inclui **Klipper**, **Mainsail OS**, **Moonraker** (recomendado)  
✔ Acesso SSH à sua Raspberry Pi (Mobaxterm)  

❌ Você NÃO precisa mais:

- Compilar firmware manualmente
- Criar o arquivo printer.cfg

---

## 🧭 Fluxo de uso

O KACE automatiza todo o processo:

1. 🔍 Detecta seu MCU automaticamente
2. 📦 Busca configurações oficiais no Klipper
3. 🧠 Sugere opções compatíveis
4. ⚙️ Gera um `printer.cfg` otimizado
5. 🔥 Compila firmware automaticamente
6. 📁 Salva tudo em `~/kace/`

---

## 📦 Resultado Final

Após executar o KACE você terá:

```
~/kace/
├── printer.cfg
├── klipper.bin / klipper.uf2 / klipper.hex
```

---

## 🚀 Próximos Passos

1. Gravar firmware na sua placa (SD / USB)
2. Enviar `printer.cfg` para o Klipper
3. Reiniciar os serviços:

```bash
sudo reboot
```

---

## 🛠️ Principais Funcionalidades

| Funcionalidade | Descrição |
| --- | --- |
| 🔍 **Auto-detecção de MCU** | Identifica seu hardware automaticamente |
| 🧠 **Motor Inteligente** | Deriva configuração sem templates |
| ⚙️ **Config Generator** | Gera um `printer.cfg` limpo |
| 🔥 **Firmware Builder** | Compila firmware automaticamente |
| 🧪 **Pré-validação** | Evita erros antes de compilar |
| 🌐 **GitHub Scraper** | Usa configurações oficiais do Klipper |
| 💻 **CLI Interativa** | UX simples e guiada |

---

## 🧠 Como funciona (conceito)

O KACE usa um sistema híbrido:

- Derivação automática baseada em MCU
- Validação antes de compilar
- Interação apenas quando necessário

👉 Sem templates  
👉 Sem configurações estáticas  
👉 Sem dependência de ferramentas externas

---

## ⚠️ Aviso

O KACE é uma ferramenta open-source projetada para simplificar a configuração do Klipper.

Ao usar este software, você reconhece que o faz **por sua própria conta e risco**.  
O autor não se responsabiliza por **danos ao hardware, configurações incorretas ou comportamentos inesperados** decorrentes do uso.

👉 Sempre revise o `printer.cfg` gerado antes de usar sua impressora.  
👉 Verifique o firmware antes de gravar.

---

## 🗑️ Desinstalar

Para remover o KACE do seu sistema:

```bash
# Remover o symlink do comando global
sudo rm -f /usr/local/bin/kace

# Ou se instalado sem sudo (fallback)
rm -f ~/.local/bin/kace

# Remover o diretório do KACE
rm -rf ~/kace
```

---

## 🎬 Guias Completos

👉 Documentação completa:

* 🇺🇸 English:   <a href="../../README.md">README.md</a>
* 🇪🇸 Español:   <a href="../es/README.md">README.md</a>
* 🇧🇷 Português: *(esta página)*

👉 Instalação Pi Imager:
* 🇺🇸 English:   <a href="../en/pi_imager.md">pi_imager.md</a>
* 🇪🇸 Español:   <a href="../es/pi_imager.md">pi_imager.md</a>
* 🇧🇷 Português: <a href="pi_imager.md">pi_imager.md</a>

👉 Instalação Klipper Completa:
* 🇺🇸 English:   <a href="../en/Klipper_install.md">Klipper_install.md</a>
* 🇪🇸 Español:   <a href="../es/klipper_install.md">klipper_install.md</a>
* 🇧🇷 Português: <a href="Klipper_install.md">Klipper_install.md</a>

---

## 🙌 Contribuição e Feedback

O KACE evolui com a comunidade:

* 🐛 Reportar bugs
* 💡 Sugerir melhorias
* 🤝 Contribuir com código

👉 Toda contribuição soma.

---

## 🙏 Agradecimentos

Este projeto se apoia no trabalho incrível da comunidade do **Klipper**.

O KACE busca tornar esse ecossistema mais acessível para todos.

---

## 📜 Licença e Uso

O KACE está licenciado sob GPL-3.0 🛠️

💡 Para uso comercial, distribuição em produtos pagos ou re-branding,  
por favor, contate o autor.

🏷️ O nome "KACE" e a marca não podem ser usados em produtos comerciais  
sem a permissão do autor.

🤝 Dar créditos é apreciado e ajuda a apoiar o projeto.

---

<p align="center">

⭐ Se gostou do projeto, deixe uma estrela  
🚀 Feito para simplificar o Klipper

</p>
