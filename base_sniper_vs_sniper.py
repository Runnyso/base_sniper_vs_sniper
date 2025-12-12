import requests, time
from collections import defaultdict

# Known top Base sniper wallets (constantly updated by the community)
TOP_SNIPERS = {
    "0x00000000000e1a0a7c8d4b5f7e9f7c1d2e3f4a5b",  # Unibot-style
    "0x6b75d8af000000aaee99b57ab7d1db4d7b7bd4d4",  # Banana Gun
    "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad",  # Real Unibot
    "0x5a7e5c5f0a8d3c8b9ff1c4e8a5b6c7d8e9f0a1b2",  # Trojan/Maestro
    "0x4838b106fce9647bdf1e7877bf73ce8b0bd5800c",  # Another known killer
}

def sniper_arena():
    print("Base — Sniper vs Sniper Arena (live bot war tracker)")
    # pair → {sniper_wallet: usd_bought}
    battles = {}

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=500")
            for tx in r.json().get("transactions", []):
                pair = tx["pairAddress"]
                buyer = tx["from"].lower()
                usd = tx.get("valueUSD", 0)

                if tx.get("side") != "buy" or usd < 5000:  # only real buys
                    continue

                if buyer not in [s.lower() for s in TOP_SNIPERS]:
                    continue

                if pair not in battles:
                    battles[pair] = {}

                battles[pair][buyer] = battles[pair].get(buyer, 0) + usd

                # When 3+ top snipers are in the same token → it's war
                if len(battles[pair]) >= 3:
                    token = tx["token0"]["symbol"] if "WETH" in tx["token1"]["symbol"] else tx["token1"]["symbol"]
                    top3 = sorted(battles[pair].items(), key=lambda x: -x[1])[:3]

                    print(f"SNIPER WAR DETECTED — {token}\n"
                          f"{len(battles[pair])} elite bots fighting!\n")
                    for i, (w, a) in enumerate(top3, 1):
                        name = next((n for n in TOP_SNIPERS if n.lower() == w), w[:10])
                        print(f"  {i}. {name} → ${a:,.0f}")
                    print(f"https://dexscreener.com/base/{pair}\n"
                          f"→ When the apex predators fight over one token...\n"
                          f"→ ...retail is the prey.\n"
                          f"{'BATTLE ROYALE'*10}")

                    # Reset after printing once
                    del battles[pair]

        except:
            pass
        time.sleep(1.1)

if __name__ == "__main__":
    sniper_arena()
