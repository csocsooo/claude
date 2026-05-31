#!/usr/bin/env python3
"""AURA Romania 30-day TikTok tracker — Gary Vee 2026 atomization model.

Daily structure: 7 content units → 16 post instances (cross-post).
- 3× video pillar clips (TikTok + IG Reels + YT Shorts + FB Reels = 4 posts each) = 12
- 2× Snapchat raw POV = 2
- 1× LinkedIn text quote = 1
- 1× X clip + thread = 1
Total: 16 posts/day across 7 platforms (Gary Vee 2026 ajánlás).

Production:
- Heti 1 pillar shoot (Sunday 13:00-16:00) → 14 video clips/hét
- Napi 1 fresh P1 news shoot (06:30, ~10 min)
- Snapchat raw napközben, in-the-moment
- LinkedIn + X szövegek vasárnap előírva 7-7 db.
"""
import csv
from datetime import date, timedelta

START = date(2026, 5, 18)  # Monday
WEEKDAY_HU = ["H", "K", "Sze", "Cs", "P", "Szo", "V"]

# 7 daily content units (= 16 post instances after cross-post)
UNITS = [
    # (unit_code, time, type_label, platforms, default_pre_record)
    ("U1", "07:00", "VID-AM",   "TikTok + IG Reels + YT Shorts + FB Reels", "Nem"),
    ("U2", "09:00", "SNAP-AM",  "Snapchat Spotlight",                       "Nem"),
    ("U3", "11:00", "LI-TXT",   "LinkedIn",                                  "Igen"),
    ("U4", "13:00", "VID-PM",   "TikTok + IG Reels + YT Shorts + FB Reels", "Igen"),
    ("U5", "16:00", "SNAP-PM",  "Snapchat Spotlight",                       "Nem"),
    ("U6", "18:00", "X-CLIP",   "X (Twitter)",                               "Igen"),
    ("U7", "20:00", "VID-EVE",  "TikTok + IG Reels + YT Shorts + FB Reels", "Igen"),
]

# ---------------- Content libraries ----------------

# VID-AM (30, P1 news with weekday flavor)
VID_AM_BY_WEEKDAY = {
    0: ("P1", "Hétfői hír-dump — weekend recap", "Weekend recap: 3 lucruri care s-au mișcat în crypto."),
    1: ("P1", "Aznapi top hír", "Știrea zilei din crypto — 30 de secunde."),
    2: ("P1", "Wednesday BNR / EU regulation", "Ce a zis regulatorul azi — pe înțelesul tău."),
    3: ("P1", "Heti félidős market check", "La jumătatea săptămânii: cine câștigă, cine pierde."),
    4: ("P1", "Friday news dump — 5 hír", "5 lucruri din crypto, în 60 de secunde."),
    5: ("P1", "Weekend market wrap", "Weekend recap + 1 alt-coin de urmărit."),
    6: ("P1", "Heti előrejelzés — 3 esemény", "3 lucruri de urmărit săptămâna care vine."),
}

# VID-PM (30, P2 edu + P5 scam + P6 prompt mix) — pillar clips
VID_PM_TOPICS = [
    ("P2", "Crypto 101 Ep.1 — blockchain mama nyelvén", "Crypto 101 Ep.1: blockchain pe înțelesul mamei."),
    ("P2", "Crypto 101 Ep.2 — exchange + AURA", "Ce e un exchange și prin ce diferă AURA."),
    ("P2", "Crypto 101 Ep.3 — self-custody", "Self-custody — și de ce contează."),
    ("P2", "Crypto 101 Ep.4 — KYC magyarázva", "KYC — de ce dai poza cu buletinul (te protejează)."),
    ("P2", "Crypto 101 Ep.5 — gas fees", "Gas fees explicate cu autostrada."),
    ("P5", "Pig butchering scam RO", "De ce românii sunt ținta «porc la tăiere»."),
    ("P2", "3 piros zászló kezdőknek", "Dacă auzi una din astea 3 — FUGI."),
    ("P5", "Fake AURA / fake support DM", "NOI NU vă scriem niciodată primii pe DM."),
    ("P2", "BTC vs ETH 45 mp", "Diferența între BTC și ETH, fără jargon."),
    ("P5", "Telegram VIP signal scam", "«Grup VIP» și signal — cum recunoști capcana."),
    ("P2", "Crypto adózás RO 2026", "Cum se plătește impozitul pe crypto în România."),
    ("P5", "Rug pull RO/CEE eset", "Un rug pull real — cum a funcționat."),
    ("P2", "Wallet bunica portofeljével", "Ce e un wallet — explicat cu portofelul de la bunica."),
    ("P2", "Crypto 101 Ep.6 — DeFi simply", "DeFi în 60 de secunde — fără hype."),
    ("P5", "Fake AURA app Play Store", "Aplicația falsă AURA — cum o recunoști."),
    ("P2", "Crypto 101 Ep.7 — stablecoins", "Stablecoin — și de ce contează pentru români."),
    ("P5", "Romance scam + crypto", "Romance scam + crypto — cum funcționează."),
    ("P2", "Crypto 101 Ep.8 — NFT debunk", "NFT — ce e real și ce a fost hype."),
    ("P5", "Recovery scam", "Recovery scam — al doilea atac după primul."),
    ("P2", "Stablecoin diaszpórának", "Diaspora HOW-TO: trimite bani acasă cu stablecoin."),
    ("P5", "Phishing email exchange", "Email de la «exchange» — cum vezi că e phishing."),
    ("P2", "Crypto 101 Ep.9 — DAO basics", "Ce e un DAO și de ce s-ar putea să-ți pese."),
    ("P5", "Fake giveaway (Elon style)", "«Trimite 1 ETH, primești 2» — niciodată."),
    ("P2", "Crypto 101 Ep.10 — EU MiCA", "EU MiCA — ce înseamnă pentru tine în 2026."),
    ("P2", "Hogyan olvass BTC chartot 60 mp", "Cum citesc un grafic — fără TA jóslás."),
    ("P5", "Ponzi scheme — Bitconnect 2.0", "Bitconnect 2.0 — semnele unei scheme Ponzi."),
    ("P2", "DCA vs lump sum", "DCA vs lump sum — care a funcționat în 5 ani."),
    ("P5", "SIM swap + 2FA SMS", "SIM swap — de ce 2FA SMS nu e suficient."),
    ("P2", "5 pontos checklist — safe exchange", "Cum verifici dacă un exchange e safe."),
    ("P2", "Top 3 lecții din 30 zile", "Top 3 lecții din prima lună pe AURA."),
]

# VID-EVE (30, P3 POV + P4 trend + P6 community)
VID_EVE_TOPICS = [
    ("P3", "POV: szülőknek bitcoint vettem", "POV: tocmai ai zis părinților că ai cumpărat BTC."),
    ("P3", "POV: te vagy az aki érti seed phrase", "POV: ești singurul din grup care înțelege seed phrase."),
    ("P3", "POV: 100 RON-od van, először crypto", "POV: ai 100 RON și vrei prima oară crypto."),
    ("P3", "3 dolog amit 18 évesen hittem", "3 lucruri pe care le-am crezut la 18 ani — false."),
    ("P4", "POV: crypto la masă duminică", "Când cineva îmi explică crypto la masă de duminică."),
    ("P3", "Generációs reakciók (bunica/frate/șef)", "Reacții generaționale la «Bitcoin»."),
    ("P3", "Crypto Twitter karakterek (4 típus)", "Tipuri de oameni în crypto Twitter — pe toate le joc."),
    ("P6", "Q&A sticker — kezdő kérdések", "Lăsați-mi întrebări — răspund mâine."),
    ("P3", "POV: birou crypto — meeting", "POV: stai în meeting, dar verifici BTC pe sub masă."),
    ("P3", "Reacția când prietenul zice 50%/lună", "Reacția mea când îmi zice cineva 50% pe lună."),
    ("P3", "POV: te magyarázod a grátar-on", "POV: ești ăla care explică crypto la grătar."),
    ("P4", "POV: tipuri de prieteni «crypto»", "Tipuri de prieteni când le zici că ești în crypto."),
    ("P3", "POV: la nuntă unchiul kérdez BTC", "POV: la nuntă, unchiul te întreabă de Bitcoin."),
    ("P3", "End-of-month vibe POV (31)", "Pe 31, când vezi cât ai cheltuit pe «doar un coin»."),
    ("P6", "Comment coinul tău (prompt)", "Comentează coinul tău — mâine îți zic 1 lucru factual."),
    ("P3", "Apu pénzügyi mondatai amit most értek", "Lucruri pe care le zicea tata — abia acum înțeleg."),
    ("P3", "Eu vs eu 2 évvel ezelőtt", "Eu vs eu de acum 2 ani în crypto."),
    ("P3", "POV: barátod aki mindent eladott mélypontnál", "POV: prietenul tău care a vândut totul la fund."),
    ("P3", "Tipuri de oameni la o petrecere crypto", "Tipuri de oameni la o petrecere de crypto."),
    ("P4", "POV: expert vs începător stil diferit", "POV: cum vorbește un expert vs un începător."),
    ("P3", "Reactia bunicii la wallet", "Reacția bunicii când îi explic wallet digital."),
    ("P3", "POV: copilul te întreabă unde sunt banii", "POV: copilul te întreabă «unde sunt banii?»."),
    ("P6", "Q&A AURA — kérdezzetek bármit", "Întrebați-mă orice despre AURA — răspund mâine."),
    ("P3", "Reactia mea la «doar 100 lei»", "Reacția mea la «doar 100 lei, ce ai de pierdut?»."),
    ("P4", "POV: la grătar, întrebare crypto", "POV: la grătar, cineva întreabă «ce e Bitcoin?»."),
    ("P3", "POV: prima oară te-a întrebat ANAF", "POV: prima oară te-a întrebat ANAF de crypto."),
    ("P6", "Community poll — mit a következő 30 napban", "30 zile recap — ce vreți să fac în următoarele 30?"),
    ("P3", "Tipuri de comentarii sub crypto video", "Tipuri de comentarii sub orice video de crypto."),
    ("P4", "Highlight reel — top momentele lunii", "Top momentele primei luni pe AURA."),
    ("P3", "Final community thank you POV", "Mulțumesc pentru 30 de zile — voi sunteți AURA."),
]

# SNAP-AM / SNAP-PM (60 — raw POV, brief description for planning only)
SNAP_AM_TOPICS = [
    ("P3", "Reggeli kávé + premarket check", "Mood crypto matinal."),
    ("P3", "Útközben — voice memo about an idea", "Idee crypto pe drum la cafenea."),
    ("P3", "Reading the news headlines", "Reacție live la titluri crypto."),
    ("P3", "Workspace setup show", "Cum arată desk-ul de creator crypto."),
    ("P3", "Reading a community comment aloud", "Comment românesc citit cu voce tare."),
    ("P3", "Quick chart take — TradingView open", "Chart look — 30 sec opinion."),
    ("P3", "Coffee + book recommendation crypto", "Cartea pe care o citesc azi."),
    ("P3", "Walking + thinking aloud about RO crypto", "Gând despre crypto România."),
    ("P3", "Phone tour — apps I use daily", "Aplicațiile mele zilnice (TradingView, AURA, etc.)."),
    ("P3", "Quick rant — un singur thing about scams", "Rant scurt despre un scam."),
    ("P3", "Behind-the-scenes — pregătesc videoul", "Behind-the-scenes pillar shoot."),
    ("P3", "Quick poll — bull or bear today?", "Întrebare rapidă: bull or bear azi?"),
    ("P3", "Reading article + reacting", "Articol crypto + reacție."),
    ("P3", "Quick demo — wallet feature", "Demo rapid: o feature wallet."),
    ("P3", "Family / friend reaction snippet", "Reacția familiei la munca mea."),
    ("P3", "Coffee shop crypto convo overhead", "Conversație crypto auzită la cafenea."),
    ("P3", "Reflection: 1 lucru am învățat azi", "Lecția zilei despre crypto."),
    ("P3", "Quick screen recording — fee compare", "Fee compare AURA vs alt exchange."),
    ("P3", "Live chart move reaction", "Reacție la o mișcare live de chart."),
    ("P3", "Question I got DM-ed today", "O întrebare interesantă din DM."),
    ("P3", "Random thought — money mindset", "Gând despre money mindset."),
    ("P3", "Mid-shoot break — life update", "Pauză shoot — viața de creator."),
    ("P3", "Quick book quote + crypto take", "Citat din carte + paralela crypto."),
    ("P3", "Watching news — live reaction", "TV știri crypto — reacția mea."),
    ("P3", "Walking home + recap zilei", "Recap zilei pe drum spre casă."),
    ("P3", "Workout + crypto monologue", "Antrenament + monolog crypto."),
    ("P3", "Pet appearance (vibe content)", "Pet vibe shot — break from crypto."),
    ("P3", "Random shop visit + price comp", "Vizita la magazin — prețuri vs inflație."),
    ("P3", "Sunday prep behind-the-scenes", "Pregătire pentru weekly shoot."),
    ("P3", "1 quote that defined month", "Citatul lunii."),
]

SNAP_PM_TOPICS = [
    ("P3", "Reacție post-piață a zilei", "Reacția mea la cum a fost piața azi."),
    ("P3", "Reading top comments of the day", "Top 3 comentarii ale zilei."),
    ("P3", "Quick screen rec — feature show", "Quick demo unei funcții."),
    ("P3", "Random gândire crypto pe drum", "Gând crypto pe drum spre acasă."),
    ("P3", "Dinner + crypto news on phone", "Cina + verific telefon."),
    ("P3", "Late afternoon update — pregătesc videoul de seară", "Pregătire video de seară."),
    ("P3", "Coffee shop convo recap", "Conversație crypto recapitulată."),
    ("P3", "Watching a competitor video — react", "Reacție la un video competitor."),
    ("P3", "Trying a new tool — screen record", "Tool nou testat — quick reaction."),
    ("P3", "Friend Q&A — voice memo", "Întrebare de la prieten."),
    ("P3", "Random book pickup + page reaction", "Cartea pe care am ridicat-o azi."),
    ("P3", "Walking + casual market take", "Mers + take casual despre piață."),
    ("P3", "Cooking + thinking aloud about crypto", "Gătit + monolog crypto."),
    ("P3", "Quick reaction — un breaking news headline", "Breaking news — reacție rapidă."),
    ("P3", "End-of-workday wrap thoughts", "Gânduri end-of-day creator."),
    ("P3", "Recommendation: 1 podcast for tonight", "Podcast recomandat pentru seară."),
    ("P3", "Live take — un coin în trending", "Take live pe un coin trending."),
    ("P3", "Behind-the-scenes editing", "Behind-the-scenes vágás."),
    ("P3", "Pet snap + caption crypto pun", "Pet + crypto pun."),
    ("P3", "Friend call recap — interesting take", "Conversație telefonică interesantă."),
    ("P3", "Late commute reflection", "Reflectie pe drum spre casă."),
    ("P3", "Food shop + price observation", "Cumpărături + observație preț."),
    ("P3", "Looking at portfolio (no numbers shown)", "Portofoliu look — fără sume."),
    ("P3", "Quick weather + crypto vibe parallel", "Vremea + paralela cu crypto."),
    ("P3", "Sunset shot + reflection", "Apus + gând crypto."),
    ("P3", "Quick chat with neighbor about money", "Discuție cu vecinul despre bani."),
    ("P3", "Late-night phone scroll reaction", "Scroll noaptea + reacție."),
    ("P3", "Plan for tomorrow vlog snippet", "Planul de mâine."),
    ("P3", "Recap of best comment received", "Best comment al zilei recapitulat."),
    ("P3", "Goodnight thought — gratitude crypto", "Gând de noapte — gratitudine community."),
]

# LinkedIn text post topics (30) — quote-of-the-day style + insight
LI_TXT_TOPICS = [
    ("P2", "3 lecții din primele 24 ore pe TikTok", "Day 1 building in public — 3 lessons."),
    ("P2", "De ce românii sunt sceptici cu crypto", "Cultural context + financial trauma post-FNI."),
    ("P2", "Cum citesc piața în 60 sec", "Framework simplu pentru oameni busy."),
    ("P2", "1 greșeală pe care nu o repet", "Vulnerability + lesson — primii 5 ani."),
    ("P2", "Build in public — week 1 numbers", "Followers, views, learnings."),
    ("P2", "De ce education > prediction", "Pourquoi ne fac TA jóslás pe TikTok."),
    ("P2", "1 thing nimeni nu îți spune despre wallet-uri", "Hot vs cold + use case real."),
    ("P2", "ANAF crypto 2026 — quick guide", "10% impozit + ce trebuie să știi."),
    ("P2", "De ce diaspora are nevoie de stablecoin", "RO diaspora remittance case study."),
    ("P2", "Cum răspund la «crypto e Ponzi?»", "Răspuns onest în 3 puncte."),
    ("P2", "Lecția din lansarea TikTok crypto în 2026", "Algo, audience, retention insights."),
    ("P2", "1 podcast care a schimbat felul în care văd crypto", "Recomandare carte/podcast."),
    ("P2", "De ce «volume strategy» nu este pentru toată lumea", "Quality vs quantity debate."),
    ("P2", "Cum măsor success pe TikTok (nu views)", "Save rate, share, follow ratio."),
    ("P2", "Lessons from a viral moment (or lack thereof)", "Post-mortem onest."),
    ("P2", "De ce am ales să nu fac «signal posts»", "Etica conținutului crypto."),
    ("P2", "Romania crypto adoption — surprised me", "Romania surprise stat + cause."),
    ("P2", "1 thing despre AURA pe care nu îți zice nimeni", "Soft brand insight (no shilling)."),
    ("P2", "Cum gândesc despre risk în 2026", "Risk frame — macro context."),
    ("P2", "Half-month wrap — best și worst", "Recap 15 zile creator life."),
    ("P2", "De ce vorbesc cu părinții mei despre crypto", "Family + finance — bridge story."),
    ("P2", "Top 3 mistakes I see on Romanian crypto Twitter", "Honest critique constructive."),
    ("P2", "Cum integrez AI în content workflow", "Behind-the-scenes — Opus Clip, CapCut."),
    ("P2", "1 framework pentru a evita scam-urile", "Decision framework în 60 sec."),
    ("P2", "Lessons from week 3", "Recap structural."),
    ("P2", "De ce TikTok > LinkedIn pentru crypto education", "Platform fit honest take."),
    ("P2", "Romania regulation pulse check 2026", "Where we are, where we're going."),
    ("P2", "1 carte care a schimbat mindset-ul meu cu bani", "Book + 3 takeaway-uri."),
    ("P2", "Final lesson din prima lună creator", "Big lesson — month 1 wrap."),
    ("P2", "Ce urmează în luna 2 — roadmap public", "Build in public — next 30 days."),
]

# X clip + thread (30) — clip from pillar + 4-tweet thread
X_CLIP_TOPICS = [
    ("P2", "Thread: 5 piros zászló crypto", "5 fraze care înseamnă scam. Save."),
    ("P2", "Thread: BTC vs ETH — 4 differences", "Thread: BTC vs ETH în 4 tweets."),
    ("P5", "Thread: cum lucrează pig butchering", "Thread: pig butchering scam structure."),
    ("P2", "Thread: cum citești un chart", "Thread: chart reading 4-step framework."),
    ("P2", "Thread: ce e blockchain (5 tweets)", "Thread: blockchain explicat 5x."),
    ("P5", "Thread: Telegram VIP scam steps", "Thread: cum recunoști Telegram VIP scam."),
    ("P2", "Thread: stablecoin pentru români", "Thread: stablecoin — diaspora use case."),
    ("P2", "Thread: hot vs cold wallet", "Thread: când folosești care."),
    ("P5", "Thread: 5 fake AURA red flags", "Thread: cum recunoști AURA fals."),
    ("P2", "Thread: ANAF crypto 2026", "Thread: cum plătești impozit pe crypto."),
    ("P2", "Thread: DeFi în 5 tweets", "Thread: DeFi pentru începători."),
    ("P5", "Thread: rug pull anatomy", "Thread: cum se face un rug pull."),
    ("P2", "Thread: DCA vs lump sum data", "Thread: DCA vs lump sum în date reale."),
    ("P2", "Thread: KYC de ce protejează", "Thread: KYC e prietenul tău."),
    ("P5", "Thread: romance scam + crypto", "Thread: romance scam — pași și apărare."),
    ("P2", "Thread: gas fees explicate", "Thread: gas fees în 5 tweets."),
    ("P2", "Thread: NFT real vs hype", "Thread: NFT — ce a fost real."),
    ("P5", "Thread: recovery scam", "Thread: recovery scam — a doua undă."),
    ("P2", "Thread: DAO basics", "Thread: DAO în 4 tweets."),
    ("P5", "Thread: address poisoning", "Thread: address poisoning — clipboard attack."),
    ("P2", "Thread: EU MiCA pentru români", "Thread: EU MiCA — ce înseamnă 2026."),
    ("P5", "Thread: fake giveaway", "Thread: «trimite 1 ETH primești 2» NIMIC."),
    ("P2", "Thread: tokenomics 5 lucruri", "Thread: tokenomics — 5 lucruri să cauți."),
    ("P5", "Thread: phishing email", "Thread: phishing email — 4 semne."),
    ("P2", "Thread: position sizing 1%", "Thread: position sizing — regula 1%."),
    ("P5", "Thread: SIM swap atac", "Thread: SIM swap — cum lucrează."),
    ("P2", "Thread: 5 puncte safe exchange", "Thread: 5 puncte să verifici un exchange."),
    ("P5", "Thread: wallet drainer", "Thread: wallet drainer — site fals."),
    ("P2", "Thread: prima lună recap", "Thread: 30 zile — 5 lecții."),
    ("P2", "Thread: ce urmează în luna 2", "Thread: roadmap public pentru luna 2."),
]


def main():
    header = [
        "#", "Day", "Date", "Weekday",
        "Unit", "Time", "Type", "Platforms",
        "Pillar", "PreRecord", "Topic", "Hook (RO)",
        "Status", "Notes",
    ]
    rows = [header]
    idx_pm = idx_eve = idx_snap_am = idx_snap_pm = idx_li = idx_x = 0
    counter = 0

    for offset in range(30):
        d = START + timedelta(days=offset)
        wd = d.weekday()
        day_label = f"D{offset+1}"
        weekday_str = WEEKDAY_HU[wd]

        for unit_code, ptime, unit_type, platforms, pre in UNITS:
            counter += 1

            if unit_type == "VID-AM":
                pillar, topic, hook = VID_AM_BY_WEEKDAY[wd]
            elif unit_type == "VID-PM":
                pillar, topic, hook = VID_PM_TOPICS[idx_pm % len(VID_PM_TOPICS)]
                idx_pm += 1
            elif unit_type == "VID-EVE":
                pillar, topic, hook = VID_EVE_TOPICS[idx_eve % len(VID_EVE_TOPICS)]
                idx_eve += 1
            elif unit_type == "SNAP-AM":
                pillar, topic, hook = SNAP_AM_TOPICS[idx_snap_am % len(SNAP_AM_TOPICS)]
                idx_snap_am += 1
            elif unit_type == "SNAP-PM":
                pillar, topic, hook = SNAP_PM_TOPICS[idx_snap_pm % len(SNAP_PM_TOPICS)]
                idx_snap_pm += 1
            elif unit_type == "LI-TXT":
                pillar, topic, hook = LI_TXT_TOPICS[idx_li % len(LI_TXT_TOPICS)]
                idx_li += 1
            elif unit_type == "X-CLIP":
                pillar, topic, hook = X_CLIP_TOPICS[idx_x % len(X_CLIP_TOPICS)]
                idx_x += 1

            rows.append([
                counter, day_label, d.isoformat(), weekday_str,
                unit_code, ptime, unit_type, platforms,
                pillar, pre, topic, hook,
                "Planned", "",
            ])

    with open("AURA_RO_TikTok_tracker.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f, quoting=csv.QUOTE_MINIMAL).writerows(rows)

    igen = sum(1 for r in rows[1:] if r[9] == "Igen")
    print(f"Wrote {len(rows)-1} rows. PreRecord=Igen: {igen}, Nem: {len(rows)-1-igen}")
    print(f"= {(len(rows)-1)//30} units/day × 30 days = {len(rows)-1} content units")
    print(f"Post instances/day (cross-post expanded): 4+1+1+4+1+1+4 = 16/day = 480 total")


if __name__ == "__main__":
    main()
