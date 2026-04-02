#!/usr/bin/env bash
# ============================================================
#  KACE — Klipper Automated Configuration Ecosystem
#  Install Script v0.1.0-beta
#  Usage: bash <(curl -s https://raw.githubusercontent.com/3D-uy/KACE/main/install.sh)
# ============================================================

set -e

# ── Colors ───────────────────────────────────────────────────
G="\033[92m"   # Green
Y="\033[93m"   # Yellow
C="\033[96m"   # Cyan
R="\033[0m"    # Reset
B="\033[1m"    # Bold
E="\033[91m"   # Red (error)

REPO_URL="https://github.com/3D-uy/KACE.git"
INSTALL_DIR="$HOME/kace"
KACE_BIN="/usr/local/bin/kace"

# ── Banner ───────────────────────────────────────────────────
echo ""
echo -e "  ${G}██╗  ██╗${Y}  ${G}█████╗${Y}  ${G}██████╗${Y} ${G}███████╗${R}"
echo -e "  ${G}██║ ██╔╝${G}██╔══██╗${G}██╔════╝${G}██╔════╝${R}"
echo -e "  ${G}█████╔╝ ${G}███████║${G}██║${G}     █████╗${R}"
echo -e "  ${G}██╔═██╗ ${G}██╔══██║${G}██║${G}     ██╔══╝${R}"
echo -e "  ${G}██║  ██╗${G}██║  ██║${Y}╚${G}██████╗${G}███████╗${R}"
echo -e "  ${Y}╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝${R}"
echo ""
echo -e "  ${C}──────────────────────────────────────────${R}"
echo -e "  ${B}${C}  KACE Installer v0.1.0-beta${R}"
echo -e "  ${C}──────────────────────────────────────────${R}"
echo ""

# ── Step 1: System dependencies ──────────────────────────────
echo -e "${C}[1/5]${R} Updating system packages..."
if command -v apt-get &>/dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y git python3-pip -qq
    echo -e "${G}  ✔ Dependencies installed (apt)${R}"
elif command -v apt &>/dev/null; then
    sudo apt update -qq
    sudo apt install -y git python3-pip -qq
    echo -e "${G}  ✔ Dependencies installed (apt)${R}"
else
    echo -e "${Y}  ⚠ apt not found. Please manually ensure git and python3-pip are installed.${R}"
fi

# ── Step 2: Clone or update KACE repository ──────────────────
echo -e "${C}[2/5]${R} Setting up KACE repository..."
if [ -d "$INSTALL_DIR/.git" ]; then
    echo -e "  Existing installation found at ${Y}${INSTALL_DIR}${R} — updating..."
    git -C "$INSTALL_DIR" pull --quiet
    echo -e "${G}  ✔ Repository updated${R}"
else
    echo -e "  Cloning KACE into ${Y}${INSTALL_DIR}${R}..."
    git clone "$REPO_URL" "$INSTALL_DIR" --quiet
    echo -e "${G}  ✔ Repository cloned${R}"
fi

# ── Step 3: Install Python dependencies ──────────────────────
echo -e "${C}[3/5]${R} Installing Python dependencies..."
pip3 install -r "$INSTALL_DIR/requirements.txt" --break-system-packages -q
echo -e "${G}  ✔ Python dependencies installed${R}"

# ── Step 4: Make kace.py executable ──────────────────────────
echo -e "${C}[4/5]${R} Setting permissions..."
chmod +x "$INSTALL_DIR/kace.py"
echo -e "${G}  ✔ kace.py is now executable${R}"

# ── Step 5: Create global symlink ────────────────────────────
echo -e "${C}[5/5]${R} Creating global ${Y}kace${R} command..."
if command -v sudo &>/dev/null; then
    sudo ln -sf "$INSTALL_DIR/kace.py" "$KACE_BIN"
    echo -e "${G}  ✔ Global command created: ${B}kace${R}${G} → ${KACE_BIN}${R}"
else
    # Fallback: add to user's PATH via ~/.local/bin
    FALLBACK_BIN="$HOME/.local/bin"
    mkdir -p "$FALLBACK_BIN"
    ln -sf "$INSTALL_DIR/kace.py" "$FALLBACK_BIN/kace"
    echo -e "${Y}  ⚠ sudo not available. Created fallback symlink at ${FALLBACK_BIN}/kace${R}"
    echo -e "${Y}  ⚠ Make sure ${FALLBACK_BIN} is in your PATH:${R}"
    echo -e "${Y}     export PATH=\"\$HOME/.local/bin:\$PATH\"${R}"
fi

# ── Done ─────────────────────────────────────────────────────
echo ""
echo -e "  ${G}══════════════════════════════════════════${R}"
echo -e "  ${B}${G}  ✅ KACE installed successfully!${R}"
echo -e "  ${G}══════════════════════════════════════════${R}"
echo ""
echo -e "  ${B}Run KACE:${R}"
echo -e "    ${C}kace${R}"
echo ""
echo -e "  ${B}Or manually:${R}"
echo -e "    ${C}python3 ~/kace/kace.py${R}"
echo ""
