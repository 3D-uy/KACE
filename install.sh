#!/usr/bin/env bash
# ============================================================
#  KACE — Klipper Automated Configuration Ecosystem
#  Install Script v0.1.0
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
VERSION="v0.1.0"

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
echo -e "${C}[1/5]${R} Checking system dependencies..."
if command -v apt-get &>/dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y git python3-pip -qq
    echo -e "${G}  ✔ Dependencies verified (apt)${R}"
elif command -v apt &>/dev/null; then
    sudo apt update -qq
    sudo apt install -y git python3-pip -qq
    echo -e "${G}  ✔ Dependencies verified (apt)${R}"
else
    echo -e "${Y}  ⚠ apt not found. Please manually ensure git and python3-pip are installed.${R}"
fi

# ── Step 2: Clone or update KACE repository ──────────────────
# Runtime files needed on the Pi — docs/assets are excluded from sparse clone
# Root-level files (kace.py, requirements.txt, etc.) are included automatically
_SPARSE_DIRS="core firmware data templates"

# Check if sparse checkout is supported (requires Git >= 2.25)
_git_supports_sparse() {
    local ver major minor
    ver=$(git --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1)
    major=$(echo "$ver" | cut -d. -f1)
    minor=$(echo "$ver" | cut -d. -f2)
    [ "${major:-0}" -gt 2 ] || { [ "${major:-0}" -eq 2 ] && [ "${minor:-0}" -ge 25 ]; }
}

echo -e "${C}[2/5]${R} Syncing KACE repository..."
if [ -d "$INSTALL_DIR/.git" ]; then
    echo -e "  Existing installation found — updating..."
    git -C "$INSTALL_DIR" pull --depth=1 --quiet
    echo -e "${G}  ✔ Repository updated${R}"
else
    echo -e "  Cloning KACE into ${Y}${INSTALL_DIR}${R}..."
    if _git_supports_sparse; then
        # Sparse shallow clone: skips docs/images — faster on slow Pi SD cards
        git clone --depth 1 --filter=blob:none --sparse "$REPO_URL" "$INSTALL_DIR" --quiet
        git -C "$INSTALL_DIR" sparse-checkout set $_SPARSE_DIRS --quiet
        echo -e "${G}  ✔ Repository cloned (optimized — docs excluded)${R}"
    else
        # Fallback: shallow clone without sparse checkout (older Git)
        git clone --depth 1 "$REPO_URL" "$INSTALL_DIR" --quiet
        echo -e "${G}  ✔ Repository cloned (shallow)${R}"
    fi
fi

# ── Step 3: Install Python dependencies ──────────────────────
echo -e "${C}[3/5]${R} Installing Python packages..."
pip3 install -r "$INSTALL_DIR/requirements.txt" --break-system-packages -q
echo -e "${G}  ✔ Python dependencies verified${R}"

# ── Step 4: Configure executable permissions ─────────────────
echo -e "${C}[4/5]${R} Configuring permissions..."
chmod +x "$INSTALL_DIR/kace.py"
echo -e "${G}  ✔ Permissions applied${R}"

# ── Step 5: Create global symlink ────────────────────────────
echo -e "${C}[5/5]${R} Finalizing installation..."
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
echo -e "  ${C}Launching KACE...${R}"
sleep 1
cd "$INSTALL_DIR" && python3 kace.py
