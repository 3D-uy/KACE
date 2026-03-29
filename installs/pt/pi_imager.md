# 🍓 Configuração do Raspberry Pi Imager (Mainsail OS)

<p align="center">
  <img src="../assets/pi_imager/pi_imager_logo.png" width="300">
</p>

---

Siga este guia passo a passo para instalar o **Mainsail OS** no seu Raspberry Pi usando o Raspberry Pi Imager.

---

### 🔹 Passo 1 — Abrir o Raspberry Pi Imager
<p align="center">
  <img src="../assets/pi_imager/pi_imager_1.png" width="500">
</p>

---

### 🔹 Passo 2 — Selecionar dispositivo
Escolha o modelo do seu Raspberry Pi.
<p align="center">
  <img src="../assets/pi_imager/pi_imager_2.png" width="500">
</p>

---

### 🔹 Passo 3 — Escolher sistema operacional
Selecione:
**Other specific-purpose OS**
<p align="center">
  <img src="../assets/pi_imager/pi_imager_3.png" width="500">
</p>

---

### 🔹 Passo 4 — Categoria 3D Printing
Selecione:
**3D Printing**
<p align="center">
  <img src="../assets/pi_imager/pi_imager_4.png" width="500">
</p>

---

### 🔹 Passo 5 — Selecionar Mainsail OS
<p align="center">
  <img src="../assets/pi_imager/pi_imager_5.png" width="500">
</p>

---

### 🔹 Passo 6 — Escolher versão
Selecione:
**Mainsail OS 2.x.x (Raspberry Pi)**
<p align="center">
  <img src="../assets/pi_imager/pi_imager_6.png" width="500">
</p>

---

### 🔹 Passo 7 — Selecionar armazenamento
Escolha o cartão SD.
<p align="center">
  <img src="../assets/pi_imager/pi_imager_7.png" width="500">
</p>

---

### 🔹 Passo 8 — Nome do dispositivo (Hostname)
Defina o nome do dispositivo  
Exemplo: `klipper`
<p align="center">
  <img src="../assets/pi_imager/pi_imager_8.png" width="500">
</p>

---

### 🔹 Passo 9 — Configuração regional
Configure:
- Fuso horário  
- Região  
- Layout do teclado  
<p align="center">
  <img src="../assets/pi_imager/pi_imager_9.png" width="500">
</p>

---

### 🔹 Passo 10 — Credenciais do usuário
Defina:
- Nome de usuário  
- Senha  
<p align="center">
  <img src="../assets/pi_imager/pi_imager_010.png" width="500">
</p>

---

### 🔹 Passo 11 — Configuração WiFi
Informe:
- Nome da rede (SSID)  
- Senha  
<p align="center">
  <img src="../assets/pi_imager/pi_imager_011.png" width="500">
</p>

---

### 🔹 Passo 12 — Ativar SSH
Ative a autenticação SSH para acesso remoto.
<p align="center">
  <img src="../assets/pi_imager/pi_imager_012.png" width="500">
</p>

---

### 🔹 Passo 13 — Gravar imagem
Inicie o processo de gravação.
<p align="center">
  <img src="../assets/pi_imager/pi_imager_013.png" width="500">
</p>

---

### ⚠️ Passo 14 — Aviso
Confirme o aviso para continuar.
<p align="center">
  <img src="../assets/pi_imager/pi_imager_014.png" width="500">
</p>

---

### 🔹 Passo 15 — Download e gravação
O sistema fará o download e gravará a imagem no cartão SD.
<p align="center">
  <img src="../assets/pi_imager/pi_imager_015.png" width="500">
</p>

---

### ✅ Passo 16 — Concluído
A gravação foi finalizada com sucesso.
<p align="center">
  <img src="../assets/pi_imager/pi_imager_016.png" width="500">
</p>

---

## 🚀 Próximo passo

Agora você pode:

1. Inserir o cartão SD no seu Raspberry Pi  
2. Ligá-lo  
3. Conectar via SSH usando ferramentas como **MobaXterm**  
   ou diretamente pelo navegador  

Use o hostname que você configurou:

```bash
klipper.local

