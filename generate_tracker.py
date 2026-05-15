#!/usr/bin/env python3
"""AURA Romania 30-day TikTok tracker CSV generator.

Start: Monday 2026-05-18.
Adds PreRecord column: "Igen" = előre felvehető batch shootban, "Nem" = aznapra kötött (hír / élő komment / aktuális trend).
"""
import csv
from datetime import date, timedelta

START = date(2026, 5, 18)  # Monday

WEEKDAY_HU = ["H", "K", "Sze", "Cs", "P", "Szo", "V"]

PILLAR_NAMES = {
    "P1": "Crypto hír",
    "P2": "Edukáció",
    "P3": "Relatable/POV",
    "P4": "Trend hijack",
    "P5": "Scam warning",
    "P6": "Community/Q&A",
}

HASHTAGS = {
    "P1": "#fyp #romania #cryptoromania #bitcoinromania #auraromania",
    "P2": "#educatiefinanciara #cryptoromania #fyp #romania #auraromania",
    "P3": "#pov #romania #relatable #fyp #cryptoromania",
    "P4": "#fyp #romania #cryptoromania #trending #auraromania",
    "P5": "#scamalert #cryptoromania #fyp #romania #protectie",
    "P6": "#qa #cryptoromania #fyp #romania #auraromania",
}

# (day_offset, slot, post_time, pillar, topic_HU, hook_RO, cta_RO, pre_record)
PLAN = [
    # D1 — Mon May 18 — LAUNCH
    (0, "Reggel", "08:30", "P1", "BTC piaci snapshot + LAUNCH intro", "Bitcoin tocmai a făcut o mișcare pe care trebuie să o vezi. Bun venit pe AURA.", "Follow pentru update zilnic 08:30", "Nem"),
    (0, "Dél",    "13:00", "P2", "3 piros zászló kezdőknek", "Dacă auzi una din astea 3 — FUGI.", "Salvează + trimite părinților", "Igen"),
    (0, "Este",   "20:00", "P3", "POV: szóltam a szüleimnek hogy bitcoint vettem", "POV: tocmai ai zis părinților că ai cumpărat Bitcoin.", "Tag pe cineva care a pățit-o", "Igen"),
    # D2 — Tue May 19
    (1, "Reggel", "08:30", "P1", "Aznapi top hír", "Știrea zilei din crypto — în 30 de secunde.", "Follow", "Nem"),
    (1, "Dél",    "13:00", "P2", "BTC vs ETH 45 mp-ben", "Diferența între Bitcoin și Ethereum, fără jargon.", "Save", "Igen"),
    (1, "Este",   "20:00", "P6", "Q&A sticker — kezdő kérdések (prompt)", "Lăsați-mi întrebări de începător — răspund mâine.", "Întrebați orice", "Igen"),
    # D3 — Wed May 20
    (2, "Reggel", "09:00", "P1", "BNR-fordítás (RO szabályozás)", "BNR a zis ceva despre crypto. Hai să traducem.", "Follow pentru context RO", "Nem"),
    (2, "Dél",    "13:00", "P2", "Crypto adózás Romániában 2026", "Cum se plătește impozitul pe crypto în România în 2026.", "Save (și întrebați contabilul)", "Igen"),
    (2, "Este",   "20:00", "P3", "POV: te vagy az egyetlen aki érti a seed phrase-t", "POV: ești singurul din grup care înțelege ce e un seed phrase.", "Comment dacă tu", "Igen"),
    # D4 — Thu May 21
    (3, "Reggel", "08:30", "P1", "Heti félidős market check", "La jumătatea săptămânii: cine câștigă, cine pierde.", "Follow", "Nem"),
    (3, "Dél",    "13:00", "P5", "Fake AURA / fake support DM scam", "NOI NU vă scriem niciodată primii pe DM.", "Screenshot + report", "Igen"),
    (3, "Este",   "20:30", "P4", "POV: dolgok amit irodában csinálsz crypto-sként", "Lucruri pe care le faci la birou când ești în crypto.", "Tag colegul", "Igen"),
    # D5 — Fri May 22
    (4, "Reggel", "08:30", "P1", "Friday news dump — 5 hír", "5 lucruri din crypto, în 60 de secunde.", "Save pentru weekend", "Nem"),
    (4, "Dél",    "13:00", "P2", "Crypto 101 Ep.1 — blockchain mama nyelvén", "Crypto 101 Ep.1: ce e blockchain-ul, pe înțelesul mamei.", "Save (urmează Ep.2)", "Igen"),
    (4, "Este",   "20:00", "P3", "3 dolog amit 18 évesen hittem a cryptóról", "3 lucruri pe care le-am crezut la 18 ani — și care erau false.", "Comment care a fost a ta", "Igen"),
    # D6 — Sat May 23
    (5, "Reggel", "09:00", "P1", "Weekend wrap + 1 alt-coin", "Weekend recap + un alt-coin despre care se vorbește.", "Follow", "Nem"),
    (5, "Dél",    "13:00", "P2", "Wallet bunica portofeljével magyarázva", "Îți explic ce e un wallet cu portofelul de la bunica.", "Save", "Igen"),
    (5, "Este",   "20:30", "P4", "POV: crypto la masă de duminică", "Când cineva îmi explică crypto la masă de duminică.", "Like dacă te-ai văzut", "Igen"),
    # D7 — Sun May 24
    (6, "Reggel", "09:30", "P1", "Heti előrejelzés — 3 esemény", "3 lucruri de urmărit săptămâna asta.", "Bookmark", "Nem"),
    (6, "Dél",    "14:00", "P5", "Pig butchering scam — RO target", "De ce românii sunt ținta preferată a unei escrocherii numite «porc la tăiere».", "Share cu părinții", "Igen"),
    (6, "Este",   "20:00", "P3", "POV: 100 RON-od van, először crypto", "POV: ai 100 RON și vrei să intri în crypto pentru prima oară.", "Comment dacă te-ai văzut", "Igen"),
    # D8 — Mon May 25
    (7, "Reggel", "08:30", "P1", "Hétfői hír-dump", "Hétfői 3 sztori, 60 mp.", "Follow", "Nem"),
    (7, "Dél",    "13:00", "P2", "Crypto 101 Ep.2 — exchange + AURA", "Ce e un exchange și prin ce diferă AURA.", "Save", "Igen"),
    (7, "Este",   "20:00", "P6", "Comment coint (prompt)", "Comentează coinul tău — mâine îți zic 1 lucru factual despre el.", "Comment cu coinul", "Igen"),
    # D9 — Tue May 26
    (8, "Reggel", "08:30", "P1", "Aznapi top hír", "Știrea zilei.", "Follow", "Nem"),
    (8, "Dél",    "13:00", "P6", "Coin komment válaszok", "Răspund la 5 coinuri din comments.", "Alte coinuri?", "Nem"),
    (8, "Este",   "20:30", "P4", "Trending sound — portofelul vs ce zic prietenii", "Cum arată portofelul meu vs ce zic prietenii că am.", "Tag prietenul", "Nem"),
    # D10 — Wed May 27
    (9, "Reggel", "09:00", "P1", "Stablecoin / on-chain hír", "Stablecoin news — ce mișcă piața.", "Follow", "Nem"),
    (9, "Dél",    "13:00", "P2", "Stablecoin diaszpórának — remittance", "Românii din străinătate — de ce stablecoin?", "Save și share cu cei plecați", "Igen"),
    (9, "Este",   "20:00", "P3", "Crypto Twitter karakterek (4 típus)", "Tipuri de oameni în crypto Twitter — pe toate le joc eu.", "Comment care ești tu", "Igen"),
    # D11 — Thu May 28
    (10, "Reggel", "08:30", "P1", "Heti félidő wrap", "Heti félidő — 3 sztori.", "Follow", "Nem"),
    (10, "Dél",    "13:00", "P2", "Crypto 101 Ep.3 — self-custody + hardware wallet", "Ce înseamnă self-custody — și de ce contează.", "Save", "Igen"),
    (10, "Este",   "20:30", "P4", "Stitch RO finance creator", "Stitch + adăugare constructivă.", "Comment cu opinia ta", "Nem"),
    # D12 — Fri May 29
    (11, "Reggel", "08:30", "P1", "Friday news dump", "5 lucruri din crypto, 60 de secunde.", "Save", "Nem"),
    (11, "Dél",    "13:00", "P5", "Rug pull RO/CEE eset", "Un rug pull real — cum a funcționat și cum îl recunoști.", "Share", "Igen"),
    (11, "Este",   "20:00", "P3", "Generációs reakciók — bunica/frate/șef", "Cum reacționează diferite generații când zici «Bitcoin».", "Comment generația ta", "Igen"),
    # D13 — Sat May 30
    (12, "Reggel", "09:00", "P1", "Weekend wrap", "Weekend recap.", "Follow", "Nem"),
    (12, "Dél",    "13:00", "P2", "Crypto 101 Ep.4 — KYC miért véd téged", "KYC — de ce trebuie să dai poza cu buletinul.", "Save", "Igen"),
    (12, "Este",   "20:30", "P4", "Trend hijack — aktuális sound", "Trending sound + crypto twist.", "Like", "Nem"),
    # D14 — Sun May 31 (EOM)
    (13, "Reggel", "09:30", "P1", "Heti előrejelzés", "3 lucruri săptămâna asta.", "Bookmark", "Nem"),
    (13, "Dél",    "14:00", "P2", "3 könyv egy barátnak pénzről + cryptóról", "3 cărți pe care le-aș da unui prieten.", "Save", "Igen"),
    (13, "Este",   "20:00", "P3", "End-of-month vibe POV", "Pe 31, când vezi cât ai cheltuit pe «doar un coin».", "Like dacă tu", "Igen"),
    # D15 — Mon Jun 1 (Ziua Copilului)
    (14, "Reggel", "08:30", "P1", "Ziua Copilului — pénzügyi ajándék gyereknek", "Cel mai bun cadou financiar pe care i-l poți face unui copil în 2026.", "Save", "Igen"),
    (14, "Dél",    "13:00", "P2", "Hogyan magyaráznám el a gyerekemnek mi a Bitcoin", "Cum i-aș explica copilului meu ce e Bitcoin.", "Share părinți", "Igen"),
    (14, "Este",   "20:00", "P3", "Pénzügyi tanulságok szülőktől → gyerekeknek", "Lucruri învățate de la părinți — și ce schimb pentru copiii mei.", "Comment", "Igen"),
    # D16 — Tue Jun 2
    (15, "Reggel", "08:30", "P1", "Aznapi hír", "Știrea zilei.", "Follow", "Nem"),
    (15, "Dél",    "13:00", "P6", "Tegnapi Q&A top 3 válasz", "Cele mai bune 3 întrebări — răspunsuri.", "Alte întrebări?", "Nem"),
    (15, "Este",   "20:30", "P4", "Trending sound — «spălat bani» kontra", "Când cineva spune că crypto e doar pentru spălat bani.", "Like dacă te-a obosit", "Nem"),
    # D17 — Wed Jun 3
    (16, "Reggel", "09:00", "P1", "ETF / institutional flow", "Cine cumpără de fapt Bitcoin în 2026.", "Follow", "Nem"),
    (16, "Dél",    "13:00", "P2", "Crypto 101 Ep.5 — gas fees autostradával", "Gas fees explicate cu autostrada.", "Save", "Igen"),
    (16, "Este",   "20:00", "P3", "Tipuri de prieteni când le zici că ești crypto", "Tipuri de prieteni când le zici că ești în crypto.", "Tag prietenul", "Igen"),
    # D18 — Thu Jun 4
    (17, "Reggel", "08:30", "P1", "Heti félidő", "Heti félidő.", "Follow", "Nem"),
    (17, "Dél",    "13:00", "P5", "Telegram VIP / signal scam", "«Grup VIP» și «signaluri» — cum recunoști capcana.", "Share", "Igen"),
    (17, "Este",   "20:30", "P4", "Duet RO creator", "Duet + build on top.", "Comment", "Nem"),
    # D19 — Fri Jun 5
    (18, "Reggel", "08:30", "P1", "Friday news dump", "5 lucruri.", "Save", "Nem"),
    (18, "Dél",    "13:00", "P2", "Hogyan olvass BTC chartot 60 mp-ben", "Cum citesc un grafic de Bitcoin în 60 de secunde — fără TA jóslás.", "Save", "Igen"),
    (18, "Este",   "20:00", "P3", "POV: a barátod aki mindent eladott a mélypontnál", "POV: prietenul tău care a vândut totul la fund.", "Tag prietenul", "Igen"),
    # D20 — Sat Jun 6
    (19, "Reggel", "09:00", "P1", "Weekend wrap", "Weekend recap.", "Follow", "Nem"),
    (19, "Dél",    "13:00", "P6", "Live Q&A bejelentés + take 1 kommentre", "Cea mai bună întrebare a săptămânii — răspuns.", "Alte întrebări?", "Nem"),
    (19, "Este",   "20:30", "P4", "Trend hijack", "Trending sound + crypto twist.", "Like", "Nem"),
    # D21 — Sun Jun 7
    (20, "Reggel", "09:30", "P1", "Heti előrejelzés", "3 lucruri săptămâna asta.", "Bookmark", "Nem"),
    (20, "Dél",    "14:00", "P5", "Romance scam + crypto (nőket céloz)", "Romance scam + crypto — cum funcționează.", "Share cu prietenele", "Igen"),
    (20, "Este",   "20:00", "P3", "Apu pénzügyi mondatai amit most értek", "Lucruri pe care le zicea tata despre bani și pe care abia acum le înțeleg.", "Comment", "Igen"),
    # D22 — Mon Jun 8
    (21, "Reggel", "08:30", "P1", "Heti nyitány", "Hétfői hír-dump.", "Follow", "Nem"),
    (21, "Dél",    "13:00", "P2", "Hogyan szervezem a portfóliómat (folyamat)", "Cum îmi organizez portofelul — fără să zic cât am sau ce cumpăr.", "Save", "Igen"),
    (21, "Este",   "20:00", "P6", "Q&A AURA — kérdezzetek bármit (prompt)", "Întrebați-mă orice despre AURA — răspund mâine.", "Întrebări?", "Igen"),
    # D23 — Tue Jun 9
    (22, "Reggel", "08:30", "P1", "Aznapi hír", "Știrea zilei.", "Follow", "Nem"),
    (22, "Dél",    "13:00", "P6", "AURA Q&A válaszok (őszinte)", "Răspund la 3 întrebări despre AURA — inclusiv ce încă lucrăm.", "Alte întrebări?", "Nem"),
    (22, "Este",   "20:30", "P4", "Trending sound — explici familiei ce faci", "Când explici familiei ce faci la muncă.", "Like", "Nem"),
    # D24 — Wed Jun 10
    (23, "Reggel", "09:00", "P1", "Hír", "Știrea zilei.", "Follow", "Nem"),
    (23, "Dél",    "13:00", "P2", "DCA vs lump sum — adat", "DCA vs lump sum — care a funcționat în ultimii 5 ani.", "Save", "Igen"),
    (23, "Este",   "20:00", "P3", "Én vs én 2 évvel ezelőtt", "Eu vs eu de acum 2 ani în crypto.", "Comment", "Igen"),
    # D25 — Thu Jun 11
    (24, "Reggel", "08:30", "P1", "Heti félidő", "Heti félidő.", "Follow", "Nem"),
    (24, "Dél",    "13:00", "P2", "50%/hó hozam debunk — matek", "De ce nu îți zice nimeni adevărul despre randamentele de 50% pe lună.", "Save", "Igen"),
    (24, "Este",   "20:30", "P3", "Reacția când prietenul zice că are 50%/lună", "Reacția mea când îmi zice cineva că face 50% pe lună.", "Tag prietenul", "Igen"),
    # D26 — Fri Jun 12
    (25, "Reggel", "08:30", "P1", "Friday news dump + havi recap", "Friday news + recap pe luna trecută.", "Save", "Nem"),
    (25, "Dél",    "13:00", "P5", "Fake AURA app Play Store / App Store", "Aplicația falsă AURA — cum o recunoști.", "Save și share", "Igen"),
    (25, "Este",   "20:00", "P3", "POV: te magyarázod a grátar-on a cryptót", "POV: ești ăla din grup care le explică altora crypto la grătar.", "Tag prietenul", "Igen"),
    # D27 — Sat Jun 13
    (26, "Reggel", "09:00", "P1", "Hónap wrap-up — 3 hír", "3 știri care au definit luna.", "Follow", "Nem"),
    (26, "Dél",    "13:00", "P6", "Community poll — mit a következő 30 napban", "M-ați urmărit 30 de zile. Ce vreți să fac în următoarele 30?", "Comment + poll", "Igen"),
    (26, "Este",   "20:30", "P4", "Highlight reel + első brand CTA", "30 de zile pe AURA TikTok — și locul în care lucrez.", "Link în bio", "Nem"),
    # D28 — Sun Jun 14
    (27, "Reggel", "09:30", "P1", "Heti előrejelzés (új hónap)", "3 lucruri săptămâna care vine.", "Bookmark", "Nem"),
    (27, "Dél",    "14:00", "P2", "5 pontos checklist — biztonságos exchange", "Cum verifici dacă un exchange e safe — checklist de 5 puncte.", "Save", "Igen"),
    (27, "Este",   "20:00", "P3", "POV: la nuntă te întreabă unchiul de Bitcoin", "POV: ești la nuntă și unchiul te întreabă de Bitcoin.", "Tag pe cineva", "Igen"),
    # D29 — Mon Jun 15
    (28, "Reggel", "08:30", "P1", "Hétfői hír-dump", "Hétfői 3 sztori.", "Follow", "Nem"),
    (28, "Dél",    "13:00", "P2", "#1 kezdő hiba — saját tapasztalat", "Greșeala #1 a începătorilor — și am făcut-o și eu.", "Comment cu a ta", "Igen"),
    (28, "Este",   "20:00", "P6", "Q&A: mit változtassak a 2. hónapban (prompt)", "Ce vreți să schimb în luna 2? Întrebați.", "Comment", "Igen"),
    # D30 — Tue Jun 16
    (29, "Reggel", "08:30", "P1", "Aznapi hír", "Știrea zilei.", "Follow", "Nem"),
    (29, "Dél",    "13:00", "P2", "Top 3 lecții din 30 zile", "Top 3 lecții din prima lună pe AURA TikTok.", "Save", "Igen"),
    (29, "Este",   "20:30", "P4", "Hónap zárás + soft brand CTA", "30 de zile, o lecție mare — și ce urmează.", "Link în bio", "Nem"),
]


def main():
    header = [
        "#", "Day", "Date", "Weekday", "Slot", "PostTime",
        "Pillar", "PillarName", "PreRecord",
        "Topic (HU)", "Hook (RO)", "CTA (RO)",
        "Hashtags", "Status", "ShootDate", "PostURL",
        "Views", "Likes", "Comments", "Shares", "Saves", "Follows",
        "Notes",
    ]
    rows = [header]
    for i, (offset, slot, ptime, pillar, topic, hook, cta, pre) in enumerate(PLAN, 1):
        d = START + timedelta(days=offset)
        rows.append([
            i, f"D{offset+1}", d.isoformat(), WEEKDAY_HU[d.weekday()],
            slot, ptime, pillar, PILLAR_NAMES[pillar], pre,
            topic, hook, cta,
            HASHTAGS[pillar], "Planned", "", "",
            "", "", "", "", "", "", "",
        ])
    with open("AURA_RO_TikTok_tracker.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f, quoting=csv.QUOTE_MINIMAL).writerows(rows)
    igen = sum(1 for r in PLAN if r[7] == "Igen")
    print(f"Wrote {len(rows)-1} rows. PreRecord=Igen: {igen}, Nem: {len(PLAN)-igen}")


if __name__ == "__main__":
    main()
