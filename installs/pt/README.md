<p align="center">
  <img src="../../assets/kace_banner.png" width="1000">
</p>

# 🚀 KACE: Klipper Automated Configuration Ecosystem

![Klipper](https://img.shields.io/badge/Klipper-Automação-orange?style=for-the-badge&logo=klipper)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)

[English (EN)](README.md) | [Español (ES)](README_ES.md)


### O KACE gera automaticamente um printer.cfg do Klipper funcional
### detectando seu hardware e guiando você pela configuração.


## 🟢 Por que o KACE?

Configurar o Klipper pode ser complexo para novos usuários.

O KACE simplifica o processo ao:
- Detectar seu MCU automaticamente
- Sugerir placas compatíveis
- Guiar você pela configuração
- Gerar um printer.cfg pronto para uso

---

## ⚠️ Aviso Legal

O KACE é fornecido como uma ferramenta de código aberto destinada a simplificar a criação de uma configuração do Klipper.

Ao usar este software, você reconhece que o faz **por sua própria conta e risco**.  
O autor não assume **nenhuma responsabilidade por possíveis danos ao hardware, má configuração ou comportamento inesperado** resultante da configuração gerada.

Sempre revise e verifique o `printer.cfg` gerado antes de usar sua impressora.


## 📋 Pré-requisitos

Antes de usar o **KACE**, certifique-se de que as seguintes etapas já foram concluídas:

✔ O cartão SD da Raspberry Pi foi gravado usando o **Raspberry Pi Imager** com **MainsailOS**

✔ Klipper, Moonraker e Mainsail estão rodando na Raspberry Pi

✔ O **KIAUH** foi instalado na Raspberry Pi

✔ O firmware da impressora foi compilado usando o KIAUH  

✔ O firmware compilado foi gravado na placa de controle da sua impressora

Após concluir essas etapas, você pode usar o **KACE** para gerar um `printer.cfg` limpo e estruturado.

---

## ⚡ Início Rápido (via SSH)

Para baixar este script, é necessário ter o **git** instalado.  
Se você não o tem instalado ou não tem certeza, execute o seguinte comando:

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y
```

Execute o KACE diretamente no seu host Klipper com estes comandos otimizados:

## # 1. 
  - Clonar o repositório
  - Instalar dependências (com bypass para SO modernos)
  - Iniciar o Ecossistema
```bash
git clone https://github.com/3D-uy/KACE.git
cd KACE
pip3 install -r requirements.txt --break-system-packages
clear
python3 kace.py
```

## # 2.

  - Baixe o arquivo printer.cfg recém-criado e envie para o Klipper.

## # 3. 

  - Reinicie o sistema via SSH
  
```
sudo reboot
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

## 🙏 Agradecimentos

O KACE não existiria sem o incrível trabalho das comunidades do **Klipper** e **KIAUH**.

Sua dedicação, inovação e espírito de código aberto tornaram a impressão 3D avançada acessível a milhares de usuários em todo o mundo.

O KACE foi criado para retribuir a este ecossistema, tornando a configuração inicial mais fácil e acessível para novos usuários do Klipper.

*Desenvolvido para a Comunidade Klipper.*
