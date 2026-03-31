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

# 🔄 PARTE 4 — Atualizar o sistema (MUITO IMPORTANTE)

O MainsailOS já vem com Klipper, Moonraker e Mainsail instalados.
A primeira coisa que devemos fazer é atualizar tudo.

### PASSO 1

No MobaXterm (conectado via SSH), copiar e colar:

```
sudo apt update
sudo apt upgrade -y
```

### PASSO 2

Instalar python:

```
sudo apt install python3-pip -y
```

### PASSO 3

Atualizar o Klipper:

```
cd ~/klipper
git pull
```

### PASSO 4

Reiniciar a Raspberry:

```
sudo reboot
```

# Aguardar 1 ou 2 minutos antes de continuar.

## Pressionar R para reiniciar o terminal, ele pedirá novamente o usuário e a senha.

user:

```
pi
```

password:

```
raspberry
```

---

# 🧰 PARTE 5 — Instalação do KIAUH

## Instalação do KIAUH

Site oficial: ([https://github.com/dw-0/kiauh](https://github.com/dw-0/kiauh))

## Passo 1

Para baixar este script é necessário ter o **git** instalado.
Se não tiver instalado ou não tiver certeza, execute o seguinte comando:

```
sudo apt-get update && sudo apt-get install git -y
```

## Passo 2

Depois que o **git** estiver instalado, use o seguinte comando para baixar o KIAUH no seu diretório *home*:

```
cd ~ && git clone https://github.com/dw-0/kiauh.git
```

## Passo 3

Por fim, inicie o KIAUH executando o seguinte comando:

```
./kiauh/kiauh.sh
```

---

# ⚙️ PARTE 6 — Compilar firmware usando KIAUH

No menu selecionar:

## 4 → Advanced

## 1 → Build

Selecionar a opção para configurar:

## Micro-controller Architecture:

### LPC176x

#----------------------------------------------------------#

## Processor model:

### LPC1768 (SKR 1.4)

### LPC1769 (SKR 1.4 TURBO)

#----------------------------------------------------------#

## Bootloader offset:

### 16KiB bootloader

#----------------------------------------------------------#

## Communication interface:

### USB

#----------------------------------------------------------#

### Pressione **Q** para sair e ele perguntará se deseja salvar.

### Pressione **Y** para aceitar e continuar com a criação do firmware.

#----------------------------------------------------------#

O firmware será gerado em:

```
/home/pi/klipper/out/klipper.bin
```

---

# 💾 PARTE 7 — Flashear a SKR no MobaXterm:

1. Ir para:

```
/home/pi/klipper/out/
```

2. Baixar klipper.bin
3. Renomear para:

## firmware.bin (para placas SKR)

4. Copiar o arquivo firmware.bin para o SD da SKR
5. Inserir o SD na SKR
6. Ligar a impressora

## Se o arquivo no SD mudar para FIRMWARE.CUR → foi flasheado corretamente.

---

# 🧠 PARTE 8 — Instalar KACE

([https://github.com/3D-uy/kace](https://github.com/3D-uy/kace))

### Conectar USB entre Raspberry e SKR

### Ligar a impressora

No terminal:

## ⚡ Início Rápido (via SSH)

Para baixar este script, é necessário ter o **git** instalado.
Se não tiver ou não tiver certeza, execute:

```bash
sudo apt-get update && sudo apt-get install git -y
sudo apt install python3-pip -y
```

Execute o KACE diretamente no seu host Klipper com estes comandos otimizados:

## # 1.

* Clonar o repositório
* Instalar dependências (com bypass para SO modernos)
* Iniciar o ecossistema

```bash
git clone https://github.com/3D-uy/KACE.git kace
cd kace
pip3 install -r requirements.txt --break-system-packages
clear
python3 kace.py
```

## # 2.

* Baixe o arquivo printer.cfg recém criado e envie para o Klipper

## # 3.

* Reinicie o sistema via SSH

```
sudo reboot
```

## Reinicie a impressora e a Raspberry

### Agora o MainsailOS já deve estar rodando na sua Raspberry e o arquivo

### printer.cfg você deve encontrá-lo na seção MACHINE.

# 🎉 HAPPY PRINTING!

Sua impressora agora deve estar rodando Klipper e você já pode fazer os ajustes necessários e começar com as macros.
