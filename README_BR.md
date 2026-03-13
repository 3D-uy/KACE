# 🚀 KACE: Klipper Automated Configuration Ecosystem

![Klipper](https://img.shields.io/badge/Klipper-Automação-orange?style=for-the-badge&logo=klipper)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)

[English (EN)](README.md) | [Español (ES)](README_ES.md)

KACE é uma ferramenta de automação de alto desempenho projetada para eliminar a complexidade manual de criar um `printer.cfg`. Ele preenche a lacuna entre o hardware bruto e uma instalação do Klipper perfeitamente ajustada.

---

## ⚡ Início Rápido (via SSH)

Para baixar este script é necessário ter o **git** instalado.  
Se você não o tem instalado ou não tem certeza, execute o seguinte comando:

```bash
sudo apt-get update && sudo apt-get install git -y
```

Execute o KACE diretamente no seu host Klipper com estes comandos otimizados:

# 1. Clonar o repositório
```bash
git clone https://github.com/3D-uy/KACE.git
cd KACE
```
# 2. Instalar dependências (com bypass para SO modernos)
```bash
pip3 install -r requirements.txt --break-system-packages
```
# 3. Iniciar o Ecossistema
```bash
python3 KACE.py
```

---

## 🛠️ Principais Recursos

| Recurso | Descrição |
| :--- | :--- |
| **GitHub Scraper** | Busca pinagens em tempo real diretamente da fonte oficial do Klipper. |
| **Assistente Inteligente** | Detecta automaticamente IDs seriais de MCU e guia você na seleção de hardware. |
| **SSH Deployer** | Envia automaticamente sua configuração gerada para o host via SSH seguro. |
| **Motor Jinja2** | Gera configurações limpas, modulares e bem comentadas. |

---

## 📦 Instalação Manual

1. **Baixar**: Clique em **"Download Project (.zip)"** no portal KACE.
2. **Upload**: Arraste a pasta `kace` para o seu Pi via MobaXterm SFTP.
3. **Executar**: Execute `python3 KACE.py` no terminal.

---

*Desenvolvido para a Comunidade Klipper.*
