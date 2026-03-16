import asyncio, json, urllib.request

# Fix Python 3.14 event loop issue
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from telethon import TelegramClient, events
from config import API_ID, API_HASH, PREFIX
import database as db

client = TelegramClient("selfbot", API_ID, API_HASH, loop=loop)

# ── Helper ───────────────────────────────────────────────────
async def edit(event, text):
    await event.edit(text, parse_mode="md")

def fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read())
    except: return None

def post_json(url, data):
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except: return None

def get_ltc_price():
    d = fetch_json("https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd,eur")
    return d["litecoin"] if d else None

def get_sol_price():
    d = fetch_json("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd,eur")
    return d["solana"] if d else None

def get_ltc_balance(address):
    d = fetch_json(f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance")
    if not d or "error" in d: return None
    return {"balance": d["balance"]/1e8, "n_tx": d["n_tx"]}

def get_sol_balance(address):
    d = post_json("https://api.mainnet-beta.solana.com", {"jsonrpc":"2.0","id":1,"method":"getBalance","params":[address]})
    if not d or not d.get("result"): return None
    return {"balance": d["result"]["value"]/1e9}

def get_all_prices():
    return fetch_json("https://api.coingecko.com/api/v3/simple/price?ids=litecoin,solana&vs_currencies=usd,eur")

def get_args(event):
    parts = event.text.split(maxsplit=1)
    return parts[1] if len(parts) > 1 else None

def get_args2(event):
    parts = event.text.split(maxsplit=2)
    return (parts[1], parts[2]) if len(parts) > 2 else (None, None)

# ═══════════════════════════════════════════════════════════════
# CRYPTO
# ═══════════════════════════════════════════════════════════════

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ltc$"))
async def ltc(event):
    addr = db.get("ltcAddress")
    if not addr: return await edit(event, "❌ No LTC address. Use `.setltc <address>`")
    await edit(event, f"⚡ **LTC Address**\n`{addr}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ltc2$"))
async def ltc2(event):
    addr = db.get("ltcAddress2")
    if not addr: return await edit(event, "❌ No LTC address #2. Use `.setltc2 <address>`")
    await edit(event, f"⚡ **LTC Address #2**\n`{addr}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}sol$"))
async def sol(event):
    addr = db.get("solAddress")
    if not addr: return await edit(event, "❌ No SOL address. Use `.setsol <address>`")
    await edit(event, f"◎ **SOL Address**\n`{addr}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}sol2$"))
async def sol2(event):
    addr = db.get("solAddress2")
    if not addr: return await edit(event, "❌ No SOL address #2. Use `.setsol2 <address>`")
    await edit(event, f"◎ **SOL Address #2**\n`{addr}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}setltc "))
async def setltc(event):
    args = get_args(event)
    db.set_field("ltcAddress", args)
    await edit(event, f"✅ **LTC Address saved:**\n`{args}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}setltc2 "))
async def setltc2(event):
    args = get_args(event)
    db.set_field("ltcAddress2", args)
    await edit(event, f"✅ **LTC Address #2 saved:**\n`{args}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}setsol "))
async def setsol(event):
    args = get_args(event)
    db.set_field("solAddress", args)
    await edit(event, f"✅ **SOL Address saved:**\n`{args}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}setsol2 "))
async def setsol2(event):
    args = get_args(event)
    db.set_field("solAddress2", args)
    await edit(event, f"✅ **SOL Address #2 saved:**\n`{args}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}removeltc$"))
async def removeltc(event): db.remove_field("ltcAddress"); await edit(event, "✅ LTC address removed.")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}removeltc2$"))
async def removeltc2(event): db.remove_field("ltcAddress2"); await edit(event, "✅ LTC address #2 removed.")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}removesol$"))
async def removesol(event): db.remove_field("solAddress"); await edit(event, "✅ SOL address removed.")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}removesol2$"))
async def removesol2(event): db.remove_field("solAddress2"); await edit(event, "✅ SOL address #2 removed.")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ltcprice$"))
async def ltcprice(event):
    await edit(event, "⏳ Fetching...")
    price = get_ltc_price()
    if not price: return await edit(event, "❌ Could not fetch LTC price.")
    await edit(event, f"⚡ **Litecoin Price**\n💵 USD: `${price['usd']:.2f}`\n💶 EUR: `€{price['eur']:.2f}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}solprice$"))
async def solprice(event):
    await edit(event, "⏳ Fetching...")
    price = get_sol_price()
    if not price: return await edit(event, "❌ Could not fetch SOL price.")
    await edit(event, f"◎ **Solana Price**\n💵 USD: `${price['usd']:.2f}`\n💶 EUR: `€{price['eur']:.2f}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}mybal$"))
async def mybal(event):
    await edit(event, "⏳ Fetching...")
    addr = db.get("ltcAddress")
    if not addr: return await edit(event, "❌ No LTC address. Use `.setltc <address>`")
    data = get_ltc_balance(addr)
    if not data: return await edit(event, "❌ Could not fetch balance.")
    price = get_ltc_price()
    usd = f" (~${data['balance']*price['usd']:.2f})" if price else ""
    await edit(event, f"⚡ **My LTC Balance**\n`{addr}`\n\n💰 `{data['balance']:.8f} LTC`{usd}\n📊 Tx: `{data['n_tx']}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}mysolbal$"))
async def mysolbal(event):
    await edit(event, "⏳ Fetching...")
    addr = db.get("solAddress")
    if not addr: return await edit(event, "❌ No SOL address. Use `.setsol <address>`")
    data = get_sol_balance(addr)
    if not data: return await edit(event, "❌ Could not fetch balance.")
    price = get_sol_price()
    usd = f" (~${data['balance']*price['usd']:.2f})" if price else ""
    await edit(event, f"◎ **My SOL Balance**\n`{addr}`\n\n💰 `{data['balance']:.6f} SOL`{usd}")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}convert "))
async def convert(event):
    args = event.text.split()
    if len(args) < 3: return await edit(event, "❌ Usage: `.convert <amount> <eur/usd/ltc/sol>`")
    await edit(event, "⏳ Fetching...")
    try: amount = float(args[1])
    except: return await edit(event, "❌ Invalid amount.")
    from_cur = args[2].lower()
    prices = get_all_prices()
    if not prices: return await edit(event, "❌ Could not fetch prices.")
    ltc_usd = prices["litecoin"]["usd"]; ltc_eur = prices["litecoin"]["eur"]
    sol_usd = prices["solana"]["usd"]; sol_eur = prices["solana"]["eur"]
    if from_cur == "eur":
        lines = [f"→ EUR · €{amount:.2f}", f"→ USD · ${amount*(ltc_usd/ltc_eur):.2f}", f"→ LTC · {amount/ltc_eur:.6f}", f"→ SOL · {amount/sol_eur:.6f}"]
    elif from_cur == "usd":
        lines = [f"→ USD · ${amount:.2f}", f"→ EUR · €{amount*(ltc_eur/ltc_usd):.2f}", f"→ LTC · {amount/ltc_usd:.6f}", f"→ SOL · {amount/sol_usd:.6f}"]
    elif from_cur == "ltc":
        lines = [f"→ LTC · {amount:.6f}", f"→ USD · ${amount*ltc_usd:.2f}", f"→ EUR · €{amount*ltc_eur:.2f}", f"→ SOL · {amount*ltc_usd/sol_usd:.6f}"]
    elif from_cur == "sol":
        lines = [f"→ SOL · {amount:.6f}", f"→ USD · ${amount*sol_usd:.2f}", f"→ EUR · €{amount*sol_eur:.2f}", f"→ LTC · {amount*sol_usd/ltc_usd:.6f}"]
    else: return await edit(event, "❌ Use: `eur`, `usd`, `ltc` or `sol`")
    await edit(event, "💱 **Conversion · Result**\n" + "\n".join(lines))

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}usdt$"))
async def usdt(event):
    val = db.get("usdt")
    if not val: return await edit(event, "❌ No USDT. Use `.setusdt <address>`")
    await edit(event, f"💵 **USDT**\n`{val}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}setusdt "))
async def setusdt(event):
    args = get_args(event); db.set_field("usdt", args); await edit(event, f"✅ USDT saved: `{args}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}removeusdt$"))
async def removeusdt(event): db.remove_field("usdt"); await edit(event, "✅ USDT removed.")

# ═══════════════════════════════════════════════════════════════
# PAYMENT METHODS
# ═══════════════════════════════════════════════════════════════

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}paypal$"))
async def paypal(event):
    val = db.get("paypal")
    if not val: return await edit(event, "❌ No PayPal. Use `.setpaypal <value>`")
    await edit(event, f"💳 **PayPal**\n`{val}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}setpaypal "))
async def setpaypal(event):
    args = get_args(event); db.set_field("paypal", args); await edit(event, f"✅ PayPal saved: `{args}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}removepaypal$"))
async def removepaypal(event): db.remove_field("paypal"); await edit(event, "✅ PayPal removed.")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}revolut$"))
async def revolut(event):
    val = db.get("revolut")
    if not val: return await edit(event, "❌ No Revolut. Use `.setrevolut <value>`")
    await edit(event, f"💳 **Revolut**\n`{val}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}setrevolut "))
async def setrevolut(event):
    args = get_args(event); db.set_field("revolut", args); await edit(event, f"✅ Revolut saved: `{args}`")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}removerevolut$"))
async def removerevolut(event): db.remove_field("revolut"); await edit(event, "✅ Revolut removed.")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}pptos$"))
async def pptos(event):
    await edit(event,
        "📋 **PAYPAL TOS**\n\n"
        "> All payments must be sent as **Friends & Family** only.\n\n"
        "⚠️ **NO refund** if sent as Goods & Services.\n\n"
        "📌 Use `.paypal` to get my PayPal address."
    )

# ═══════════════════════════════════════════════════════════════
# TAGS
# ═══════════════════════════════════════════════════════════════

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}tag "))
async def tag(event):
    name = get_args(event)
    content = db.get_tag(name)
    if not content: return await edit(event, f"❌ Tag `{name}` not found.")
    await edit(event, content)

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}tagcreate "))
async def tagcreate(event):
    name, content = get_args2(event)
    if not name or not content: return await edit(event, "❌ Usage: `.tagcreate <n> <content>`")
    db.set_tag(name, content); await edit(event, f"✅ Tag `{name}` created.")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}removetag "))
async def removetag(event):
    name = get_args(event)
    ok = db.remove_tag(name)
    await edit(event, f"✅ Tag `{name}` removed." if ok else f"❌ Tag `{name}` not found.")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}tags$"))
async def tags(event):
    t = db.list_tags()
    if not t: return await edit(event, "❌ No tags saved.")
    await edit(event, "🏷️ **Your tags:**\n" + "\n".join(f"• `{x}`" for x in t))

# ═══════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}calc "))
async def calc(event):
    expr = get_args(event)
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        await edit(event, f"🧮 `{expr}` = `{result}`")
    except: await edit(event, "❌ Invalid expression.")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ping$"))
async def ping(event): await edit(event, "🏓 **Pong!**")

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}help$"))
async def help_cmd(event):
    await edit(event, """📖 **SELFBOT COMMANDS**

💰 **CRYPTO**
`.ltc` `.ltc2` `.sol` `.sol2`
`.setltc` `.setltc2` `.setsol` `.setsol2`
`.removeltc` `.removeltc2` `.removesol` `.removesol2`
`.ltcprice` `.solprice` `.mybal` `.mysolbal`
`.convert <amount> <eur/usd/ltc/sol>`
`.usdt` `.setusdt` `.removeusdt`

💳 **PAYMENTS**
`.paypal` `.setpaypal` `.removepaypal`
`.revolut` `.setrevolut` `.removerevolut`
`.pptos`

🏷️ **TAGS**
`.tag <n>` `.tagcreate <n> <content>`
`.removetag <n>` `.tags`

🛠️ **UTILS**
`.calc <expr>` `.convert` `.ping` `.help`
""")

async def main():
    await client.start()
    print("🚀 Selfbot is running! Type .help to see commands.")
    await client.run_until_disconnected()

loop.run_until_complete(main())
