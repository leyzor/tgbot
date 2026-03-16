# 🤖 Telegram Selfbot

Selfbot Telegram avec gestion crypto (LTC, SOL), paiements, tags et utilitaires.

## 🚀 Setup

### 1. Récupère tes API credentials Telegram
1. Va sur https://my.telegram.org
2. Connecte-toi avec ton numéro de téléphone
3. Clique **"API development tools"**
4. Crée une app → copie **api_id** et **api_hash**

### 2. Configure config.py
```python
API_ID = 123456        # ton api_id
API_HASH = "abcdef..."  # ton api_hash
PREFIX = "."           # préfixe des commandes
```

### 3. Installe les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lance le selfbot
```bash
python main.py
```
La première fois, Telegram va te demander ton numéro de téléphone et le code SMS.
Une session `selfbot.session` sera créée — garde-la précieusement.

---

## 📋 Commandes

### 💰 CRYPTO
| Commande | Description |
|----------|-------------|
| `.ltc` | Affiche ton adresse LTC |
| `.ltc2` | Affiche ton adresse LTC #2 |
| `.sol` | Affiche ton adresse SOL |
| `.sol2` | Affiche ton adresse SOL #2 |
| `.setltc <address>` | Enregistre ton adresse LTC |
| `.setsol <address>` | Enregistre ton adresse SOL |
| `.removeltc` | Supprime ton adresse LTC |
| `.ltcprice` | Prix du LTC en temps réel |
| `.solprice` | Prix du SOL en temps réel |
| `.mybal` | Balance de ton adresse LTC |
| `.mysolbal` | Balance de ton adresse SOL |
| `.convert <amount> <eur/usd/ltc/sol>` | Convertisseur |
| `.usdt` `.setusdt` `.removeusdt` | Adresse USDT |

### 💳 PAYMENT METHODS
| Commande | Description |
|----------|-------------|
| `.paypal` `.setpaypal` `.removepaypal` | PayPal |
| `.revolut` `.setrevolut` `.removerevolut` | Revolut |
| `.pptos` | Message TOS PayPal |

### 🏷️ TAGS
| Commande | Description |
|----------|-------------|
| `.tag <n>` | Affiche un tag |
| `.tagcreate <n> <content>` | Crée un tag |
| `.removetag <n>` | Supprime un tag |
| `.tags` | Liste tous tes tags |

### 🛠️ UTILITIES
| Commande | Description |
|----------|-------------|
| `.calc <expression>` | Calculatrice |
| `.convert <amount> <devise>` | Convertisseur crypto |
| `.ping` | Pong! |
| `.help` | Liste des commandes |
