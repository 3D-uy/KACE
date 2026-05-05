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
clear
BANNER_URL="https://raw.githubusercontent.com/3D-uy/KACE/main/core/banner.py"
SUBTITLE="KACE Installer"
VERSION="v0.1.0-beta"

if [ -f "core/banner.py" ]; then
    python3 core/banner.py "$SUBTITLE" "$VERSION"
elif [ -f "$INSTALL_DIR/core/banner.py" ]; then
    python3 "$INSTALL_DIR/core/banner.py" "$SUBTITLE" "$VERSION"
else
    python3 -c "$(curl -fsSL $BANNER_URL)" "$SUBTITLE" "$VERSION" 2>/dev/null || {
        echo ""
        echo -e "  ${C}──────────────────────────────────────────${R}"
        echo -e "  ${B}${C}  $SUBTITLE $VERSION${R}"
        echo -e "  ${C}──────────────────────────────────────────${R}"
        echo ""
    }
fi

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
# ── Done ─────────────────────────────────────────────────────
echo ""
echo -e "  ${G}══════════════════════════════════════════${R}"
echo -e "  ${B}${G}  ✅ KACE installed successfully!${R}"
echo -e "  ${G}══════════════════════════════════════════${R}"
echo ""
echo -e "  ${C}Launching KACE...${R}"
sleep 1
cd "$INSTALL_DIR" && python3 kace.py
