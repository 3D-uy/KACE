# 🚀 KLIPPER instalação fácil

![Firmware](https://img.shields.io/badge/Firmware-Klipper-orange)
![Board](https://img.shields.io/badge/Board-SKR%201.4%20%2F%201.4%20Turbo-blue)
![Raspberry](https://img.shields.io/badge/Raspberry-Pi%203B-red)
![Interface](https://img.shields.io/badge/UI-Mainsail-purple)
![Guide](https://img.shields.io/badge/Guía-Instalación%20simple-success)

# 🧠 O guia definitivo para instalar o Klipper

Este tutorial foi projetado para ser seguido junto com o vídeo.
Basta copiar cada bloco de código e colá-lo no terminal.
Você não precisa digitar comandos manualmente.

---

# 📋 REQUISITOS

* 🧠 Raspberry Pi (como exemplo usaremos uma Raspberry Pi 3B)
* 🧩 Placa exemplo: SKR 1.4 Turbo
* 💾 Cartão SD de boa qualidade para a Raspberry
* 💾 Cartão SD para carregar firmware na SKR
* 🔌 Cabo USB entre Raspberry e SKR
* 💻 PC com Windows
* 🖥️ MobaXterm instalado

## 🔗 Todos os links você encontrará abaixo

---

# 💿 PARTE 1 — Gravar o MainsailOS no cartão SD

Antes de começar, você precisa gravar o sistema operacional no cartão SD da Raspberry Pi.

Usaremos o **Raspberry Pi Imager**, a ferramenta oficial.

📥 Baixar aqui

Site oficial [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

Instalar e abrir o programa.

Depois seguir estes passos:

1. Clicar em **Modelo de Raspberry Pi**

2. Selecionar:

   ## Other specific-purpose OS

3. Depois selecionar:

   ## 3D printing

4. Escolher:

   ## Mainsail OS

5. Clicar em **Choose Storage**

6. Selecionar seu **cartão SD**

7. Pressionar **FINALIZAR**

O programa irá baixar a imagem e gravá-la automaticamente.

# 📥 Enquanto isso, baixe o seguinte programa

## 🖥️ Baixar MobaXterm

Site oficial
[https://mobaxterm.mobatek.net/download.html](https://mobaxterm.mobatek.net/download.html)

---

# ⚡ Quando terminar

1. Remover o cartão SD
2. Inseri-lo na **Raspberry Pi**
3. Ligar a Raspberry

## Aguardar aproximadamente **1 a 2 minutos** para que o sistema inicialize completamente.

# 📡 PARTE 2  Abrir o MainsailOS

### Abrir o navegador e acessar:

```
klipper.local
```

Se abrir o Mainsail → perfeito.

---

# 🔐 PARTE 3 — Conectar via SSH com MobaXterm

### 🖥️ Abrir MobaXterm → Session → SSH

Remote host:

```
klipper.local
```

Username:

```
pi
```

Password:

```
raspberry
```

## Se entrar → estamos dentro da Raspberry.

---

# ⚡ PARTE — Instalar e usar KACE (TUDO em um)

O KACE simplifica TODO o processo:

* 🔧 Compila o firmware
* ⚙️ Gera o `printer.cfg`
* 🚀 Deixa o Klipper pronto para usar

---


## ⚡ Instalação em uma linha

```bash
bash <(curl -s https://raw.githubusercontent.com/3D-uy/KACE/main/install.sh)
```

> Isso instalará todas as dependências, clonará o repositório e configurará o comando global `kace` automaticamente.

## 📦 Resultado final

Após executar o KACE você terá:

```
~/kace/
├── printer.cfg
├── klipper.bin / klipper.uf2 / klipper.hex
```

---

## 🚀 Próximos passos

1. Gravar firmware na sua placa (SD / USB)
2. Enviar `printer.cfg` para o Klipper
3. Reiniciar serviços:

```bash
sudo reboot
```

---

### 🎉 PRONTO PARA COMEÇAR

Você já tem seu firmware compilado e seu arquivo `printer.cfg` gerado automaticamente.

Agora só falta ajustá-lo às suas necessidades, calibrar sua impressora e começar a aproveitar ao máximo o Klipper.

🚀 Aproveite o processo e HAPPY PRINTING!

---

## 🙌 Contribuir e feedback

O KACE evolui com a comunidade:

* 🐛 Reportar bugs
* 💡 Sugerir melhorias
* 🤝 Contribuir com código

👉 Toda contribuição soma.

---

## 🙏 Agradecimentos

Este projeto se apoia no incrível trabalho da comunidade do **Klipper**.

O KACE busca tornar esse ecossistema mais acessível para todos.

---

<p align="center">

⭐ Se gostou deste projeto, deixe uma estrela
🚀 Feito para simplificar o Klipper

</p>


---
