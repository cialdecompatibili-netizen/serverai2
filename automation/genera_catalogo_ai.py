# GUIDA-SVILUPPO: genera _data/catalogo.json, shop-categorie.json e le pagine _negozio/ + en/negozio/ per ScalaAI 2.
# Modello: accesso a LLM open source a consumo, si parte da poca potenza e si scala. Rilanciabile, sovrascrive solo ai-*/cat-*.
# Percorsi derivati dalla posizione dello script (niente hard coded). Prezzi in centesimi, modificarli solo in PIANI.
import json, os, re, glob
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = [  # id, it, en, icona
 ("api", "API a consumo", "Pay-as-you-go API", "\u26A1"),
 ("chat", "Chat AI", "AI Chat", "\U0001F4AC"),
 ("dedicato", "Modelli dedicati", "Dedicated models", "\U0001F5A5"),
 ("gpu", "Potenza di calcolo", "Compute power", "\U0001F680"),
]
PIANI = [  # cat, it, en, prezzo cent, desc it, desc en
 (0,"Credito API Start","API Credit Start",1000,"Credito prepagato per i modelli open source piccoli e medi. Paghi solo quello che usi.","Prepaid credit for small and medium open source models. Pay only for what you use."),
 (0,"Credito API Pro","API Credit Pro",5000,"Credito prepagato con accesso a tutti i modelli, anche i grandi.","Prepaid credit with access to every model, including the large ones."),
 (1,"Chat Free Trial","Chat Free Trial",0,"Prova la chat con i modelli piccoli, senza carta.","Try the chat with small models, no card needed."),
 (1,"Chat Plus mensile","Chat Plus monthly",1500,"Chat illimitata ragionevole con modelli medi e storico conversazioni.","Fair-use chat with medium models and conversation history."),
 (1,"Chat Pro mensile","Chat Pro monthly",3500,"Modelli grandi, priorita' di risposta e documenti allegati.","Large models, priority responses and file attachments."),
 (2,"Modello dedicato Small","Dedicated Small model",9900,"Un modello open source solo tuo su CPU o GPU piccola, mensile.","Your own open source model on CPU or small GPU, monthly."),
 (2,"Modello dedicato Medium","Dedicated Medium model",39900,"Modello medio su GPU dedicata, latenza bassa e dati isolati, mensile.","Medium model on a dedicated GPU, low latency and isolated data, monthly."),
 (3,"GPU a ore Base","GPU hourly Base",2900,"Pacchetto ore di GPU per generare o addestrare. Scegli tu il modello.","GPU hours bundle to generate or train. You choose the model."),
 (3,"GPU a ore Scale","GPU hourly Scale",19900,"Pacchetto ore su GPU potenti, per carichi alti e picchi di richieste.","Hours bundle on powerful GPUs for heavy loads and request spikes."),
]
def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:48]
cats = [{"nome": c[1], "id": c[0], "icona": c[3], "tr": {"en": {"nome": c[2]}}} for c in CATS]
prods, pages = [], []
for cat, it, en, pr, di, de in PIANI:
    c = CATS[cat]; pid = "ai-" + slug(it)
    prods.append({"tipo": "servizio", "id": pid, "nome": it, "categoria": c[0], "prezzo_centesimi": pr,
      "descrizione": di, "descrizione_completa": di + "\nAttivazione dopo la conferma. Si parte dal basso e si scala quando serve.",
      "immagine": "", "icona": c[3], "visibile": True,
      "tr": {"en": {"nome": en, "descrizione": de, "descrizione_completa": de + "\nActivation after confirmation. Start small and scale when you need to."}}})
    pages.append((pid, it, en))
d = json.load(open(os.path.join(R, "_data", "catalogo.json"), encoding="utf-8"))
d["categorie"], d["prodotti"] = cats, prods
def wj(name, obj):
    json.dump(obj, open(os.path.join(R, "_data", name), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
wj("catalogo.json", d)
wj("shop-categorie.json", [{"nome": c[0], "slug": c[0]} for c in CATS])
for f in glob.glob(os.path.join(R, "_negozio", "*.md")) + glob.glob(os.path.join(R, "en", "negozio", "**", "*.md"), recursive=True):
    if re.match(r"(ai|cat)-|(prodotto|categoria)-esempio", os.path.basename(f)): os.remove(f)
def w(path, t):
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path, "w", encoding="utf-8", newline="\n").write(t)
for pid, it, en in pages:
    w(os.path.join(R, "_negozio", pid + ".md"), '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /negozio/%s/\ndescription: "%s - ScalaAI."\nref: shop-prod-%s\n---\n' % (it, pid, pid, it, pid))
    w(os.path.join(R, "en", "negozio", pid + ".md"), '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /en/shop/%s/\ndescription: "%s - ScalaAI."\nlang: en\nlocale: en\nref: shop-prod-%s\n---\n' % (en, pid, pid, en, pid))
for c in CATS:
    w(os.path.join(R, "_negozio", "cat-" + c[0] + ".md"), '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /negozio/categoria/%s/\ndescription: "%s."\nref: shop-cat-%s\n---\n' % (c[1], c[0], c[0], c[1], c[0]))
    w(os.path.join(R, "en", "negozio", "categoria", "cat-" + c[0] + ".md"), '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /en/shop/category/%s/\ndescription: "%s."\nlang: en\nlocale: en\nref: shop-cat-%s\n---\n' % (c[2], c[0], c[0], c[2], c[0]))
print("ok", len(prods), "piani", len(cats), "categorie")
