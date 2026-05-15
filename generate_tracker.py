#!/usr/bin/env python3
"""Generate the AURA Romania 30-day TikTok tracker as CSV."""
import csv
from datetime import date, timedelta

START = date(2026, 5, 15)

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

# (day_offset, slot_label, post_time, pillar, topic_RO, hook_RO, cta)
PLAN = [
    # D1 — 2026-05-15 P — LAUNCH
    (0, "Reggel", "08:30", "P1", "BTC piaci snapshot, launch nap", "Bitcoin tocmai a făcut o mișcare pe care trebuie să o vezi.", "Follow pentru update zilnic 08:30"),
    (0, "Dél",    "13:00", "P2", "3 piros zászló kezdőknek", "Dacă auzi una din astea 3 — FUGI.", "Salvează + trimite părinților"),
    (0, "Este",   "20:00", "P3", "POV: szóltam a szüleimnek hogy bitcoint vettem", "POV: tocmai ai zis părinților că ai cumpărat Bitcoin.", "Tag pe cineva care a pățit-o"),
    # D2 — 05-16 Szo
    (1, "Reggel", "09:00", "P1", "Weekend market wrap — top 3 mozgás", "3 lucruri care s-au mișcat în crypto săptămâna asta.", "Comment cu coinul tău"),
    (1, "Dél",    "13:00", "P2", "Ce e egy wallet — bunica portofeljével magyarázva", "Îți explic ce e un wallet cu portofelul de la bunica.", "Save"),
    (1, "Este",   "20:30", "P4", "Trend hijack — crypto la masă de Paște", "Când cineva îmi explică crypto la masă de duminică.", "Like dacă te-ai văzut"),
    # D3 — 05-17 V
    (2, "Reggel", "09:30", "P1", "Heti előrejelzés — 3 esemény", "3 lucruri de urmărit săptămâna asta în crypto.", "Bookmark"),
    (2, "Dél",    "14:00", "P5", "Pig butchering scam — RO target", "De ce românii sunt ținta preferată a unei escrocherii numite «porc la tăiere».", "Share cu părinții"),
    (2, "Este",   "20:00", "P3", "3 dolog amit 18 évesen hittem a cryptóról", "3 lucruri pe care le-am crezut la 18 ani despre crypto — și care erau false.", "Comment care a fost a ta"),
    # D4 — 05-18 H
    (3, "Reggel", "08:30", "P1", "Heti nyitány — 4 sztori 60 mp", "Ce s-a întâmplat în crypto cât ai dormit.", "Follow"),
    (3, "Dél",    "13:00", "P2", "BTC vs ETH 45 mp-ben", "Diferența între Bitcoin și Ethereum, fără jargon, în 45 de secunde.", "Save"),
    (3, "Este",   "20:00", "P6", "Q&A sticker — kezdő kérdések", "Lăsați-mi întrebări de începător — răspund mâine.", "Întrebați orice"),
    # D5 — 05-19 K
    (4, "Reggel", "08:30", "P1", "Aznapi top hír", "Știrea zilei din crypto — în 30 de secunde.", "Follow"),
    (4, "Dél",    "13:00", "P6", "Tegnapi Q&A top 3 válasz", "Cele mai bune 3 întrebări de ieri — răspunsuri.", "Alte întrebări în comments"),
    (4, "Este",   "20:30", "P4", "Trending sound — portofelul vs ce zic prietenii", "Cum arată portofelul meu vs ce zic prietenii că am.", "Tag prietenul"),
    # D6 — 05-20 Sze
    (5, "Reggel", "09:00", "P1", "BNR-fordítás (RO szabályozás)", "BNR a zis ceva despre crypto. Hai să traducem.", "Follow pentru context RO"),
    (5, "Dél",    "13:00", "P2", "Crypto adózás Romániában 2026", "Cum se plătește impozitul pe crypto în România în 2026.", "Save (și întrebați contabilul)"),
    (5, "Este",   "20:00", "P3", "POV: te vagy az egyetlen aki érti a seed phrase-t", "POV: ești singurul din grup care înțelege ce e un seed phrase.", "Comment dacă tu ești ăla"),
    # D7 — 05-21 Cs
    (6, "Reggel", "08:30", "P1", "Heti félidős market check", "La jumătatea săptămânii: cine câștigă, cine pierde.", "Follow"),
    (6, "Dél",    "13:00", "P5", "Fake AURA / fake support DM scam", "NOI NU vă scriem niciodată primii pe DM. Iată cum recunoști.", "Screenshot + report"),
    (6, "Este",   "20:30", "P4", "Stitch RO finance creator-ral", "Stitch + adăugare constructivă.", "Comment cu opinia ta"),
    # D8 — 05-22 P
    (7, "Reggel", "08:30", "P1", "Friday news dump — 5 hír", "5 lucruri din crypto, în 60 de secunde.", "Save pentru weekend"),
    (7, "Dél",    "13:00", "P2", "Crypto 101 Ep.1 — blockchain mama nyelvén", "Crypto 101 Ep.1: ce e blockchain-ul, pe înțelesul mamei.", "Save (urmează Ep.2)"),
    (7, "Este",   "20:00", "P3", "Dolgok amit irodában csinálsz crypto-sként", "Lucruri pe care le faci la birou când ești în crypto.", "Tag colegul"),
    # D9 — 05-23 Szo
    (8, "Reggel", "09:00", "P1", "Weekend wrap + 1 alt-coin sztori", "Weekend recap + un alt-coin despre care se vorbește.", "Follow"),
    (8, "Dél",    "13:00", "P2", "Crypto 101 Ep.2 — exchange + AURA", "Ce e un exchange și prin ce diferă AURA.", "Save"),
    (8, "Este",   "20:30", "P4", "Trend hijack — aktuális", "Trend hijack + crypto twist.", "Like"),
    # D10 — 05-24 V
    (9, "Reggel", "09:30", "P1", "Heti előrejelzés", "3 lucruri de urmărit săptămâna care vine.", "Bookmark"),
    (9, "Dél",    "14:00", "P5", "Telegram VIP / signal scam", "«Grup VIP» și «signaluri» — cum recunoști capcana.", "Share"),
    (9, "Este",   "20:00", "P3", "Generációs reakciók — bunica/frate/șef", "Cum reacționează diferite generații când zici «Bitcoin».", "Comment generația ta"),
    # D11 — 05-25 H
    (10, "Reggel", "08:30", "P1", "Hétfői hír-dump", "Hétfői 3 sztori, 60 mp.", "Follow"),
    (10, "Dél",    "13:00", "P2", "Crypto 101 Ep.3 — self-custody + hardware wallet", "Ce înseamnă self-custody — și de ce contează.", "Save"),
    (10, "Este",   "20:00", "P6", "Komment coint, holnap 1 tényt mondok róla", "Comentează coinul tău — mâine îți zic 1 lucru factual despre el.", "Comment cu coinul"),
    # D12 — 05-26 K
    (11, "Reggel", "08:30", "P1", "Aznapi top hír", "Știrea zilei.", "Follow"),
    (11, "Dél",    "13:00", "P6", "Coin komment válaszok (3-5 db)", "Răspund la 5 coinuri din comments.", "Alte coinuri?"),
    (11, "Este",   "20:30", "P4", "Trending sound — «crypto = spălat bani» kontra", "Când cineva spune că crypto e doar pentru spălat bani.", "Like dacă te-a obosit"),
    # D13 — 05-27 Sze
    (12, "Reggel", "09:00", "P1", "Stablecoin / on-chain hír", "Stablecoin news — ce mișcă piața.", "Follow"),
    (12, "Dél",    "13:00", "P2", "Stablecoin diaszpórának — remittance", "Românii care trimit bani din străinătate — de ce stablecoin?", "Save și share cu cei plecați"),
    (12, "Este",   "20:00", "P3", "Crypto Twitter karakterek (4 típus)", "Tipuri de oameni în crypto Twitter — pe toate le joc eu.", "Comment care ești tu"),
    # D14 — 05-28 Cs
    (13, "Reggel", "08:30", "P1", "Heti félidő wrap", "Heti félidő — 3 sztori.", "Follow"),
    (13, "Dél",    "13:00", "P2", "Crypto 101 Ep.4 — KYC miért véd téged", "KYC — de ce trebuie să dai poza cu buletinul (și de ce te protejează).", "Save"),
    (13, "Este",   "20:30", "P4", "Duet RO creator videójával", "Duet + build on top.", "Comment cu părerea"),
    # D15 — 05-29 P
    (14, "Reggel", "08:30", "P1", "Friday news dump", "5 lucruri din crypto, 60 de secunde.", "Save"),
    (14, "Dél",    "13:00", "P5", "Rug pull RO/CEE eset", "Un rug pull real — cum a funcționat și cum îl recunoști.", "Share"),
    (14, "Este",   "20:00", "P3", "POV: 100 RON-od van, először crypto", "POV: ai 100 RON și vrei să intri în crypto pentru prima oară.", "Comment dacă te-ai văzut"),
    # D16 — 05-30 Szo
    (15, "Reggel", "09:00", "P1", "Weekend wrap", "Weekend recap.", "Follow"),
    (15, "Dél",    "13:00", "P6", "Live Q&A bejelentés + take 1 kommentre", "Cea mai bună întrebare a săptămânii — răspuns.", "Alte întrebări?"),
    (15, "Este",   "20:30", "P4", "Trend hijack", "Trending sound + crypto twist.", "Like"),
    # D17 — 05-31 V
    (16, "Reggel", "09:30", "P1", "Heti előrejelzés", "3 lucruri săptămâna asta.", "Bookmark"),
    (16, "Dél",    "14:00", "P2", "3 könyv egy barátnak pénzről + cryptóról", "3 cărți pe care le-aș da unui prieten care vrea să înțeleagă banii.", "Save"),
    (16, "Este",   "20:00", "P3", "End-of-month vibe POV", "Pe 31, când vezi cât ai cheltuit pe «doar un coin».", "Like dacă tu"),
    # D18 — 06-01 H — Ziua Copilului
    (17, "Reggel", "08:30", "P1", "Hír + Ziua Copilului — pénzügyi ajándék gyereknek", "Cel mai bun cadou financiar pe care i-l poți face unui copil în 2026.", "Save"),
    (17, "Dél",    "13:00", "P2", "Hogyan magyaráznám el a gyerekemnek mi a Bitcoin", "Cum i-aș explica copilului meu ce e Bitcoin.", "Share părinți"),
    (17, "Este",   "20:00", "P3", "Pénzügyi tanulságok szülőktől → gyerekeknek", "Lucruri învățate despre bani de la părinți — și ce schimb pentru copiii mei.", "Comment"),
    # D19 — 06-02 K
    (18, "Reggel", "08:30", "P1", "Aznapi hír", "Știrea zilei.", "Follow"),
    (18, "Dél",    "13:00", "P2", "Crypto 101 Ep.5 — gas fees autostradával", "Gas fees explicate cu autostrada.", "Save"),
    (18, "Este",   "20:30", "P4", "Trending sound + crypto twist", "Trend hijack.", "Like"),
    # D20 — 06-03 Sze
    (19, "Reggel", "09:00", "P1", "ETF / institutional flow", "Cine cumpără de fapt Bitcoin în 2026.", "Follow"),
    (19, "Dél",    "13:00", "P2", "DCA vs lump sum — adat", "DCA vs lump sum — care a funcționat în ultimii 5 ani.", "Save"),
    (19, "Este",   "20:00", "P6", "Stitch cinikus kommenttel", "Stitch + răspuns respectuos, factual.", "Comment"),
    # D21 — 06-04 Cs
    (20, "Reggel", "08:30", "P1", "Heti félidő", "Heti félidő.", "Follow"),
    (20, "Dél",    "13:00", "P5", "Fake AURA app Play Store / App Store", "Aplicația falsă AURA — cum o recunoști.", "Save și share"),
    (20, "Este",   "20:30", "P4", "Tipuri de prieteni când le zici că ești crypto", "Tipuri de prieteni când le zici că ești în crypto.", "Tag prietenul"),
    # D22 — 06-05 P
    (21, "Reggel", "08:30", "P1", "Friday news dump", "5 lucruri.", "Save"),
    (21, "Dél",    "13:00", "P2", "Hogyan olvass BTC chartot 60 mp-ben", "Cum citesc un grafic de Bitcoin în 60 de secunde — fără TA jóslás.", "Save"),
    (21, "Este",   "20:00", "P3", "POV: a barátod aki mindent eladott a mélypontnál", "POV: prietenul tău care a vândut totul la fund.", "Tag prietenul"),
    # D23 — 06-06 Szo
    (22, "Reggel", "09:00", "P1", "Weekend wrap", "Weekend recap.", "Follow"),
    (22, "Dél",    "13:00", "P2", "#1 kezdő hiba — saját tapasztalat", "Greșeala #1 a începătorilor — și am făcut-o și eu.", "Comment cu a ta"),
    (22, "Este",   "20:30", "P4", "Trend hijack", "Trending sound + crypto.", "Like"),
    # D24 — 06-07 V
    (23, "Reggel", "09:30", "P1", "Heti előrejelzés", "3 lucruri săptămâna asta.", "Bookmark"),
    (23, "Dél",    "14:00", "P5", "Romance scam + crypto (nőket céloz)", "Romance scam + crypto — cum funcționează.", "Share cu prietenele"),
    (23, "Este",   "20:00", "P3", "Apu pénzügyi mondatai amit most értek", "Lucruri pe care le zicea tata despre bani și pe care abia acum le înțeleg.", "Comment"),
    # D25 — 06-08 H
    (24, "Reggel", "08:30", "P1", "Heti nyitány", "Hétfői hír-dump.", "Follow"),
    (24, "Dél",    "13:00", "P2", "Hogyan szervezem a portfóliómat (folyamat, nem allokáció)", "Cum îmi organizez portofelul — fără să zic cât am sau ce cumpăr.", "Save"),
    (24, "Este",   "20:00", "P6", "Q&A AURA — kérdezzetek bármit", "Întrebați-mă orice despre AURA — răspund mâine.", "Întrebări?"),
    # D26 — 06-09 K
    (25, "Reggel", "08:30", "P1", "Aznapi hír", "Știrea zilei.", "Follow"),
    (25, "Dél",    "13:00", "P6", "AURA Q&A válaszok (3 db, őszinte)", "Răspund la 3 întrebări despre AURA — inclusiv ce încă lucrăm.", "Alte întrebări?"),
    (25, "Este",   "20:30", "P4", "Trending sound — explici familiei ce faci la muncă", "Când explici familiei ce faci la muncă.", "Like"),
    # D27 — 06-10 Sze
    (26, "Reggel", "09:00", "P1", "Hír", "Știrea zilei.", "Follow"),
    (26, "Dél",    "13:00", "P2", "5 pontos checklist — biztonságos exchange", "Cum verifici dacă un exchange e safe — checklist de 5 puncte.", "Save"),
    (26, "Este",   "20:00", "P3", "Én vs én 2 évvel ezelőtt", "Eu vs eu de acum 2 ani în crypto.", "Comment"),
    # D28 — 06-11 Cs
    (27, "Reggel", "08:30", "P1", "Heti félidő", "Heti félidő.", "Follow"),
    (27, "Dél",    "13:00", "P2", "50%/hó hozam debunk — matek", "De ce nu îți zice nimeni adevărul despre randamentele de 50% pe lună.", "Save"),
    (27, "Este",   "20:30", "P4", "Stitch RO creator", "Stitch + adăugare.", "Comment"),
    # D29 — 06-12 P
    (28, "Reggel", "08:30", "P1", "Friday news dump + havi recap", "Friday news + recap pe luna mai.", "Save"),
    (28, "Dél",    "13:00", "P2", "Top 3 lecke az elmúlt hónapból", "Top 3 lecții din ultima lună pe AURA TikTok.", "Save"),
    (28, "Este",   "20:00", "P3", "POV: te magyarázod a grátar-on a cryptót", "POV: ești ăla din grup care le explică altora crypto la grătar.", "Tag prietenul"),
    # D30 — 06-13 Szo — HÓNAP ZÁRÁS
    (29, "Reggel", "09:00", "P1", "Hónap wrap-up — 3 hír", "3 știri care au definit luna.", "Follow"),
    (29, "Dél",    "13:00", "P6", "Community poll — mit a következő 30 napban", "M-ați urmărit 30 de zile. Ce vreți să fac în următoarele 30?", "Comment + poll"),
    (29, "Este",   "20:30", "P4", "Highlight reel + első brand CTA", "30 de zile pe AURA TikTok — și locul în care lucrez.", "Link în bio"),
]


def main():
    rows = []
    header = [
        "#", "Day", "Date", "Weekday", "Slot", "PostTime",
        "Pillar", "PillarName", "Topic (HU)", "Hook (RO)", "CTA (RO)",
        "Hashtags", "Status", "ShootDate", "PostURL",
        "Views", "Likes", "Comments", "Shares", "Saves", "Follows",
        "Notes",
    ]
    rows.append(header)
    for i, (offset, slot, ptime, pillar, topic, hook, cta) in enumerate(PLAN, 1):
        d = START + timedelta(days=offset)
        day_label = f"D{offset+1}"
        weekday = WEEKDAY_HU[d.weekday()]
        rows.append([
            i, day_label, d.isoformat(), weekday, slot, ptime,
            pillar, PILLAR_NAMES[pillar], topic, hook, cta,
            HASHTAGS[pillar], "Planned", "", "",
            "", "", "", "", "", "",
            "",
        ])
    with open("AURA_RO_TikTok_tracker.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerows(rows)
    print(f"Wrote {len(rows)-1} rows to AURA_RO_TikTok_tracker.csv")


if __name__ == "__main__":
    main()
