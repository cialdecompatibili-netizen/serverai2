# GUIDA-SVILUPPO: testi home, chi siamo, servizi IT+EN per ScalaAI 2. Rilanciabile. Nessun dato inventato (numeri, clienti, recensioni, prestazioni).
# Poi lanciare automation/allinea_hash.py. Percorsi derivati dalla posizione dello script.
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = [("api","API a consumo","Pay-as-you-go API","Credito prepagato: paghi solo quello che usi.","Prepaid credit: pay only for what you use."),
 ("chat","Chat AI","AI Chat","Chat con modelli open source, dalla prova gratuita al piano Pro.","Chat with open source models, from free trial to the Pro plan."),
 ("dedicato","Modelli dedicati","Dedicated models","Un modello solo tuo, con dati isolati.","A model of your own, with isolated data."),
 ("gpu","Potenza di calcolo","Compute power","Ore di GPU per generare o addestrare.","GPU hours to generate or train.")]
T = {"it": dict(base="__BASEURL__", shop="/negozio/", cat="/negozio/categoria/", srv="/servizi/", con="/contatti/",
  eb="Modelli AI open source a consumo", h1="I migliori modelli open source, <em>paghi solo quello che usi.</em>",
  lead="Accedi via API o chat a modelli AI open source senza gestire server. Parti dal piano più piccolo e passa a modelli dedicati e GPU quando ti servono.",
  b1="Vedi i piani", b2="Come funziona", ce="Piani", ch="Scegli da dove partire", cl="Quattro livelli: si parte dal basso e si scala solo quando serve.", ccat_pre="Vedi i piani",
  mc="Come funziona", mh="Da zero alla scala", steps=[("Prova","Parti con la chat gratuita o un piccolo credito API."),("Integra","Usa le chiavi API nelle tue app o la chat dal browser."),("Cresci","Con più richieste passi a modelli più grandi."),("Scala","Modello dedicato o ore di GPU per i carichi alti.")],
  ct="Hai un progetto?", cs="Raccontaci cosa devi fare e ti diciamo da quale piano partire.", cb="Contattaci"),
 "en": dict(base="__BASEURL__", shop="/en/shop/", cat="/en/shop/category/", srv="/en/services/", con="/en/contact/",
  eb="Open source AI models, pay as you go", h1="The best open source models, <em>pay only for what you use.</em>",
  lead="Access open source AI models by API or chat with no servers to manage. Start on the smallest plan and move to dedicated models and GPUs when you need them.",
  b1="See the plans", b2="How it works", ce="Plans", ch="Choose where to start", cl="Four levels: start small and scale only when needed.", ccat_pre="See the plans",
  mc="How it works", mh="From zero to scale", steps=[("Try","Start with the free chat or a small API credit."),("Integrate","Use API keys in your apps or chat from the browser."),("Grow","With more requests, move to larger models."),("Scale","Dedicated model or GPU hours for heavy loads.")],
  ct="Have a project?", cs="Tell us what you need and we will say which plan to start with.", cb="Contact us")}
def blocks(l):
    t = T[l]; i = 0 if l == "it" else 1
    cards = "".join('<div class="gc-pl ent-pl"><b>%s</b><p>%s</p><p><a class="gc-link" href="%s%s%s/">%s</a></p></div>' % (c[1+i], c[3+i], t["base"], t["cat"], c[0], t["ccat_pre"]) for c in CATS)
    steps = "".join('<div class="gc-pl"><span class="n">0%d</span><b>%s</b><p>%s</p></div>' % (n+1, s[0], s[1]) for n, s in enumerate(t["steps"]))
    cyc = "".join("<div><b>%s</b><span>%s</span></div>" % s for s in t["steps"])
    return [
     dict(id="hero", nome="Hero", enabled=True, html='<div class="gc"><section class="ent-hero"><div class="gc-wrap gc-hero-in"><div><p class="gc-eyebrow">%s</p><h1 class="gc-h1">%s</h1><p class="gc-lead">%s</p><div class="gc-act"><a class="gc-btn gc-btn-a" href="%s%s">%s</a><a class="gc-btn gc-btn-o" href="%s%s">%s</a></div></div><div class="ent-cycle">%s</div></div></section></div>' % (t["eb"], t["h1"], t["lead"], t["base"], t["shop"], t["b1"], t["base"], t["srv"], t["b2"], cyc)),
     dict(id="categorie", nome=t["ce"], enabled=True, html='<div class="gc"><section class="gc-sec gc-soft" id="categorie"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><div class="gc-plat ent-4">%s</div></div></section></div>' % (t["ce"], t["ch"], t["cl"], cards)),
     dict(id="metodo", nome=t["mc"], enabled=True, html='<div class="gc"><section class="gc-sec" id="metodo"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><div class="gc-plat ent-4">%s</div></div></section></div>' % (t["mc"], t["mh"], steps)),
     dict(id="contatti", nome="Contatti" if l == "it" else "Contact", enabled=True, html='<div class="gc"><section class="gc-sec gc-dark" id="contatti"><div class="gc-wrap"><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><a class="gc-btn" href="%s%s">%s</a></div></section></div>' % (t["ct"], t["cs"], t["base"], t["con"], t["cb"]))]
def azienda(l):
    if l == "it":
        a = ("Chi siamo","Modelli open source, senza server da gestire","ScalaAI dà accesso a modelli AI open source via API e chat, a consumo. Noi affittiamo la potenza di calcolo e facciamo girare i modelli, tu li usi.","Si parte dal basso e si cresce con la richiesta: dalla chat gratuita ai modelli dedicati e alle ore di GPU.","Come lavoriamo",[("Trasparenza","Scegli il modello e sai cosa usi e cosa paghi."),("Scala graduale","Parti piccolo e passi a più potenza solo quando serve."),("Open source","Usiamo modelli aperti, senza dipendere da un solo fornitore.")])
    else:
        a = ("About us","Open source models, no servers to manage","ScalaAI gives access to open source AI models by API and chat, pay as you go. We rent the compute and run the models, you use them.","We start small and grow with demand: from the free chat to dedicated models and GPU hours.","How we work",[("Transparency","You pick the model and know what you use and pay."),("Gradual scale","Start small and add power only when needed."),("Open source","We use open models, without relying on a single vendor.")])
    p = "".join('<div class="gc-pl"><span class="n">%d</span><b>%s</b><p>%s</p></div>' % (n+1, x[0], x[1]) for n, x in enumerate(a[5]))
    return [dict(id="chi", nome=a[0], enabled=True, html='<div class="gc"><section class="gc-sec" id="chi"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><p>%s</p></div></section></div>' % (a[0], a[1], a[2], a[3])),
            dict(id="principi", nome="Principi" if l == "it" else "Principles", enabled=True, html='<div class="gc"><section class="gc-sec gc-soft" id="principi"><div class="gc-wrap"><h2 class="gc-h2">%s</h2><div class="gc-plat">%s</div></div></section></div>' % (a[4], p))]
def wj(path, o):
    open(os.path.join(R, path), "w", encoding="utf-8", newline="\n").write(json.dumps(o, ensure_ascii=False, indent=2) + "\n")
wj("_data/blocks_home.json", blocks("it")); wj("_data/i18n/en/blocks_home.json", blocks("en"))
wj("_data/blocks_azienda.json", azienda("it")); wj("_data/i18n/en/blocks_azienda.json", azienda("en"))
def sub(path, pairs):
    f = os.path.join(R, path); s = open(f, encoding="utf-8").read()
    for a, b in pairs:
        s = re.sub(a, lambda m: b, s, flags=re.S)
    open(f, "w", encoding="utf-8", newline="\n").write(s)
sub("_pages/servizi.md", [(r'seo_description:.*?\n---\n.*$', 'seo_description: "Cosa offre ScalaAI e come funziona."\n---\n\nAccesso a modelli AI open source via API e chat, a consumo. Ecco i livelli.\n\n## API a consumo\nCredito prepagato per usare i modelli dalle tue app.\n\n## Chat AI\nChat con modelli open source, con prova gratuita.\n\n## Modelli dedicati\nUn modello solo tuo, con dati isolati.\n\n## Potenza di calcolo\nOre di GPU per generare o addestrare.\n\n[Vedi i piani]({{ \'/negozio/\' | relative_url }}){: .btn .btn--primary}\n')])
sub("en/servizi.md", [(r'permalink: /en/services/\n---\n.*$', 'permalink: /en/services/\n---\n\nAccess to open source AI models by API and chat, pay as you go. Here are the levels.\n\n## Pay-as-you-go API\nPrepaid credit to use the models from your apps.\n\n## AI Chat\nChat with open source models, with a free trial.\n\n## Dedicated models\nA model of your own, with isolated data.\n\n## Compute power\nGPU hours to generate or train.\n\n[See the plans]({{ \'/en/shop/\' | relative_url }}){: .btn .btn--primary}\n'), (r'description: "Our services\."', 'description: "What ScalaAI offers and how it works."')])
print("ok")
