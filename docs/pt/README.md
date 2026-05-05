<p align="center">
  <img src="../assets/kace_banner.png" width="1000">
</p>

# 🚀 KACE — Klipper Automated Configuration Ecosystem

<p align="center">

🌐 **Idioma**  
🇺🇸 <a href="../../README.md">English</a> | 🇪🇸 <a href="../es/README.md">Español</a> | 🇧🇷 Português

</p>

---

### ⚡ Instale o Klipper da forma mais fácil — copiar, colar e pronto.

O KACE gera automaticamente um **`printer.cfg` funcional para o Klipper**, detectando o seu hardware e guiando você através de um processo de configuração inteligente.

---

## 🎯 Por que KACE?

Configurar o Klipper pode ser complexo e demorado, especialmente para novos usuários.

**O KACE simplifica tudo:**

- 🔍 Detecta automaticamente o seu MCU  
- 🧠 Sugere placas compatíveis  
- 🧭 Guia você passo a passo  
- ⚙️ Gera um `printer.cfg` pronto para uso  

---

## ⚠️ Aviso

O KACE é fornecido como uma ferramenta open-source destinada a simplificar a criação de configurações para o Klipper.

Ao utilizar este software, você reconhece que o faz **por sua conta e risco**.  
O autor não se responsabiliza por **danos ao hardware, configurações incorretas ou comportamentos inesperados** decorrentes do uso das configurações geradas.

👉 Sempre revise e verifique o arquivo `printer.cfg` antes de utilizar sua impressora.

---

## 📋 Pré-requisitos

Antes de usar o **KACE**, certifique-se de que os seguintes passos foram concluídos:

✔ Cartão SD da Raspberry Pi gravado com **Raspberry Pi Imager** usando **Mainsail OS**  
✔ Klipper, Moonraker e Mainsail em execução  
✔ **KIAUH** instalado na Raspberry Pi  
✔ Firmware compilado usando o KIAUH  
✔ Firmware gravado na placa controladora da impressora  

Após isso, o KACE cuida do restante.

---

## ⚡ Início rápido (via SSH)

Certifique-se de ter o `git` instalado:

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y
````

---

### 🚀 Executar KACE

```bash
git clone https://github.com/3D-uy/KACE.git kace
cd kace
pip3 install -r requirements.txt --break-system-packages
clear
python3 kace.py
```

---

### 📥 Próximos passos

1. Baixar o arquivo `printer.cfg` gerado
2. Enviá-lo para a interface do Klipper
3. Reiniciar os serviços:

```bash
sudo systemctl restart klipper moonraker
```

---

## 🛠️ Principais funcionalidades

| Funcionalidade                | Descrição                                        |
| :---------------------------- | :----------------------------------------------- |
| 🔎 **GitHub Scraper**         | Obtém pinouts em tempo real do Klipper           |
| 🧠 **Assistente inteligente** | Detecta o MCU e orienta na escolha do hardware   |
| 🔐 **Deploy via SSH**         | Envia automaticamente a configuração para o host |
| ⚙️ **Motor Jinja2**           | Gera configurações limpas, modulares e legíveis  |

---

## 🎬 Guia completo de instalação

👉 Guias passo a passo:

* 🇺🇸 English: `../../README.md`
* 🇪🇸 Español: `../es/README.md`
* 🇧🇷 Português: *(esta página)*

---

## 🙌 Contribuição e feedback

O KACE está em constante evolução e o seu feedback é essencial.

* 🐛 Reportar problemas
* 💡 Sugerir melhorias
* 🤝 Contribuir com ideias

👉 Cada contribuição ajuda a melhorar o projeto.

---

## 🙏 Agradecimentos

O KACE não existiria sem o incrível trabalho das comunidades de **Klipper** e **KIAUH**.

Sua dedicação, inovação e espírito open-source tornaram a impressão 3D avançada acessível para milhares de usuários ao redor do mundo.

O KACE foi criado para contribuir com esse ecossistema, tornando a configuração inicial mais simples e acessível.

---

<p align="center">

⭐ Se você gostou do projeto, considere dar uma estrela
🚀 Feito para a comunidade Klipper

</p>


