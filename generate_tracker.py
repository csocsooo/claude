#!/usr/bin/env python3
"""AURA Romania 30-day TikTok tracker — 10 video/day variant.

Start: Monday 2026-05-18.
Daily 10 slots: 07:00, 08:30, 10:00, 11:30, 13:00, 14:30, 16:00, 18:00, 20:00, 21:30.
Pillar cadence per day: P1×3 (hír) + P2×2 (edu) + P3×2 (POV) + P4×1 (trend) + P5×1 (scam) + P6×1 (Q&A) = 10.
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

SLOTS = [
    # (slot_label, time, pillar)
    ("S1",  "07:00", "P1"),  # morning news
    ("S2",  "08:30", "P2"),  # quick tip
    ("S3",  "10:00", "P3"),  # POV morning
    ("S4",  "11:30", "P1"),  # midday market
    ("S5",  "13:00", "P2"),  # deep edu / Crypto 101
    ("S6",  "14:30", "P4"),  # trend
    ("S7",  "16:00", "P5"),  # scam warning
    ("S8",  "18:00", "P3"),  # POV evening
    ("S9",  "20:00", "P1"),  # evening wrap
    ("S10", "21:30", "P6"),  # community
]

# --- P1 hír (90 db = 3/nap) — weekday flavored templates ---
# Each day's 3 P1 slots, varied by weekday for slot 1 (07:00).
WEEKDAY_MORNING_NEWS = {
    0: ("Hétfői hír-dump — ce a făcut crypto în weekend", "Weekend recap: 3 lucruri care s-au mișcat."),
    1: ("Aznapi top hír", "Știrea zilei din crypto — 30 de secunde."),
    2: ("Wednesday hír — BNR / EU regulation focus", "Ce a zis regulatorul azi — pe înțelesul tău."),
    3: ("Heti félidős market check", "La jumătatea săptămânii: cine câștigă, cine pierde."),
    4: ("Friday news dump — 5 hír", "5 lucruri din crypto, în 60 de secunde."),
    5: ("Weekend market wrap", "Weekend recap + 1 alt-coin de urmărit."),
    6: ("Heti előrejelzés — 3 esemény", "3 lucruri de urmărit săptămâna care vine."),
}
MIDDAY_MARKET = ("Aznapi piaci frissítés", "Update: BTC, ETH, top mover-ul zilei — 30 sec.")
EVENING_WRAP = ("Esti wrap — ce a contat azi", "Esti recap: ce trebuie să știi înainte să dormi.")

# --- P2 edukáció (60 db = 2/nap) ---
P2_TOPICS = [
    ("3 piros zászló kezdőknek", "Dacă auzi una din astea 3 — FUGI.", "Salvează + trimite părinților"),
    ("BTC vs ETH 45 mp", "Diferența între Bitcoin și Ethereum, fără jargon.", "Save"),
    ("Crypto adózás Romániában 2026", "Cum se plătește impozitul pe crypto în România.", "Save + întreabă contabilul"),
    ("Crypto 101 Ep.1 — blockchain mama nyelvén", "Crypto 101 Ep.1: ce e blockchain-ul, pe înțelesul mamei.", "Save (Ep.2 urmează)"),
    ("Crypto 101 Ep.2 — exchange + AURA", "Ce e un exchange și prin ce diferă AURA.", "Save"),
    ("Crypto 101 Ep.3 — self-custody + hardware wallet", "Ce înseamnă self-custody și de ce contează.", "Save"),
    ("Crypto 101 Ep.4 — KYC miért véd téged", "KYC — de ce dai poza cu buletinul (și de ce te protejează).", "Save"),
    ("Crypto 101 Ep.5 — gas fees autostradával", "Gas fees explicate cu autostrada.", "Save"),
    ("Crypto 101 Ep.6 — DeFi simply", "DeFi în 60 de secunde — fără hype.", "Save"),
    ("Crypto 101 Ep.7 — stablecoins", "Ce e un stablecoin și de ce contează pentru români.", "Save"),
    ("Crypto 101 Ep.8 — NFT debunk", "NFT — ce e real și ce a fost hype.", "Save"),
    ("Crypto 101 Ep.9 — DAO basics", "Ce e un DAO și de ce s-ar putea să-ți pese.", "Save"),
    ("Crypto 101 Ep.10 — EU MiCA", "EU MiCA — ce înseamnă pentru tine în 2026.", "Save"),
    ("Wallet bunica portofeljével", "Ce e un wallet — explicat cu portofelul de la bunica.", "Save"),
    ("Stablecoin diaszpórának — remittance", "Românii din străinătate — de ce stablecoin?", "Save + share cu cei plecați"),
    ("3 könyv egy barátnak pénzről + crypto", "3 cărți pentru un prieten care vrea să înțeleagă banii.", "Save"),
    ("Hogyan olvass BTC chartot 60 mp", "Cum citesc un grafic de Bitcoin — fără TA jóslás.", "Save"),
    ("DCA vs lump sum — adat", "DCA vs lump sum: care a funcționat în ultimii 5 ani.", "Save"),
    ("Hogyan szervezem a portfóliómat", "Cum îmi organizez portofelul — fără să zic cât am.", "Save"),
    ("50%/hó hozam debunk — matek", "De ce nu îți zice nimeni adevărul despre 50%/lună.", "Save"),
    ("5 pontos checklist — safe exchange", "Cum verifici dacă un exchange e safe — 5 puncte.", "Save"),
    ("#1 kezdő hiba — saját tapasztalat", "Greșeala #1 a începătorilor — și am făcut-o și eu.", "Comment cu a ta"),
    ("Hogyan magyaráznám gyermeknek mi a BTC", "Cum i-aș explica copilului meu ce e Bitcoin.", "Share părinți"),
    ("Top 3 lecții din 30 zile", "Top 3 lecții din prima lună pe AURA TikTok.", "Save"),
    ("Hot vs cold wallet", "Hot vs cold wallet — când folosești care.", "Save"),
    ("2FA — nem opcionális", "2FA — singurul lucru între tine și un hack.", "Save"),
    ("Seed phrase storage — 5 módszer", "5 moduri în care să-ți păstrezi seed phrase-ul.", "Save"),
    ("Mi az AMM (automated market maker)", "AMM în 45 de secunde — fără jargon.", "Save"),
    ("Liquidity pool magyarázva", "Ce e un liquidity pool — și de ce poți pierde bani.", "Save"),
    ("Yield farming kockázatok", "Yield farming — 3 riscuri pe care nu ți le zice nimeni.", "Save"),
    ("Impermanent loss példa", "Impermanent loss — explicat cu un exemplu real.", "Save"),
    ("Bridge-ek és kockázatuk", "Cross-chain bridges — și de ce sunt hack-uite.", "Save"),
    ("L1 vs L2 — Ethereum scaling", "L1 vs L2 — diferența în 60 de secunde.", "Save"),
    ("Mempool — mi az", "Ce e mempool-ul — și de ce contează pentru gas.", "Save"),
    ("Halving — mi és miért érdekes", "Bitcoin halving — ce e și de ce piața se mișcă.", "Save"),
    ("PoW vs PoS — konszenzus", "Proof of Work vs Proof of Stake — fără jargon.", "Save"),
    ("Validator vs node", "Validator vs node — diferența pentru începători.", "Save"),
    ("Slashing — mit kockáztat a staker", "Ce înseamnă slashing dacă faci staking.", "Save"),
    ("Gas optimization tippek", "5 trucuri să plătești mai puțin gas.", "Save"),
    ("Tokenomics olvasása — 5 pont", "Cum citești tokenomics-ul unui proiect în 60 sec.", "Save"),
    ("Whitepaper read tippek", "Cum citești un whitepaper fără să-ți pierzi vremea.", "Save"),
    ("On-chain analytics alapok", "On-chain analytics — ce să te uiți pentru BTC.", "Save"),
    ("Whale watching — mit nézel", "Whale watching — cum urmărești banii mari.", "Save"),
    ("Fear & Greed Index", "Fear & Greed Index — și cum nu-l folosesc lume.", "Save"),
    ("RSI alapok 30 mp", "RSI — indicatorul tehnic în 30 de secunde.", "Save"),
    ("MACD alapok", "MACD — și de ce începătorii îl folosesc greșit.", "Save"),
    ("Trendline rajzolás", "Cum desenezi un trendline care chiar funcționează.", "Save"),
    ("Support és resistance", "Support și resistance — în 60 de secunde.", "Save"),
    ("Volume olvasás", "Volume — de ce e mai important decât prețul.", "Save"),
    ("Halving cycle theory", "Bitcoin halving cycle — teoria în 60 de secunde.", "Save"),
    ("ETF flow — mit néz", "ETF flow — cum afli cine cumpără BTC.", "Save"),
    ("Korreláció: BTC vs S&P 500", "BTC vs bursa americană — corelația explicată.", "Save"),
    ("Inflation hedge teória — BTC vs gold", "BTC ca aur digital — teoria și realitatea.", "Save"),
    ("Macro: Fed rate cuts impact", "Fed cuts rate — ce se întâmplă cu BTC?", "Save"),
    ("Position sizing 1% rule", "Position sizing — regula 1% care îți salvează contul.", "Save"),
    ("Stop loss vs DCA", "Stop loss vs DCA — strategii diferite, când pe care.", "Save"),
    ("Tax loss harvesting RO 2026", "Tax loss harvesting — cum scazi impozitul legal.", "Save"),
    ("RON-crypto local payments", "Plăți crypto în România — 2026 update.", "Save"),
    ("Cum trimit bani din străinătate cu crypto", "Diaspora HOW-TO: trimite bani acasă cu stablecoin.", "Save + share"),
    ("Recovery seed phrase fogalom", "Ce e seed phrase-ul de recuperare — și unde îl NUUUU pui.", "Save"),
]

# --- P3 POV/relatable (60 db = 2/nap) ---
P3_TOPICS = [
    ("POV: szóltam szülőknek bitcointot vettem", "POV: tocmai ai zis părinților că ai cumpărat Bitcoin.", "Tag pe cineva care a pățit-o"),
    ("POV: te vagy az egyetlen aki érti seed phrase", "POV: ești singurul din grup care înțelege ce e un seed phrase.", "Comment dacă tu"),
    ("3 dolog amit 18 évesen hittem (false)", "3 lucruri pe care le-am crezut la 18 ani — și care erau false.", "Comment a ta"),
    ("POV: 100 RON-od van, először crypto", "POV: ai 100 RON și vrei să intri în crypto pentru prima oară.", "Comment dacă te-ai văzut"),
    ("Dolgok amit irodában csinálsz crypto-sként", "Lucruri pe care le faci la birou când ești în crypto.", "Tag colegul"),
    ("Crypto Twitter karakterek (4 típus)", "Tipuri de oameni în crypto Twitter — pe toate le joc eu.", "Comment care ești tu"),
    ("Generációs reakciók — bunica/frate/șef", "Cum reacționează generațiile când zici «Bitcoin».", "Comment generația ta"),
    ("End-of-month vibe POV", "Pe 31, când vezi cât ai cheltuit pe «doar un coin».", "Like dacă tu"),
    ("Pénzügyi tanulságok szülőktől → gyerekeknek", "Lucruri învățate de la părinți — și ce schimb pentru copiii mei.", "Comment"),
    ("Tipuri de prieteni când le zici că ești crypto", "Tipuri de prieteni când le zici că ești în crypto.", "Tag prietenul"),
    ("POV: barátod aki mindent eladott a mélypontnál", "POV: prietenul tău care a vândut totul la fund.", "Tag prietenul"),
    ("Eu vs eu 2 évvel ezelőtt", "Eu vs eu de acum 2 ani în crypto.", "Comment"),
    ("Apu pénzügyi mondatai amit most értek", "Lucruri pe care le zicea tata și abia acum le înțeleg.", "Comment"),
    ("Reacția când prietenul zice 50%/lună", "Reacția mea când îmi zice cineva că face 50% pe lună.", "Tag prietenul"),
    ("POV: te magyarázod a grátar-on", "POV: ești ăla care explică crypto la grătar.", "Tag prietenul"),
    ("POV: la nuntă unchiul kérdez BTC-ről", "POV: ești la nuntă și unchiul te întreabă de Bitcoin.", "Tag pe cineva"),
    ("POV: dr. de pe TikTok te diagnosztikál mint crypto bro", "POV: tipul de pe TikTok te diagnostichează ca «crypto bro».", "Like"),
    ("Reactia mea când văd un nou meme coin", "Reacția mea când văd un nou meme coin în trending.", "Comment"),
    ("POV: prietenul te invită la «oportunitate»", "POV: prietenul te invită la «o oportunitate unică».", "Tag prietenul"),
    ("Tipuri de oameni la o petrecere crypto", "Tipuri de oameni la o petrecere de crypto.", "Comment"),
    ("POV: la salon, doamna kérdez BTC-ről", "POV: la salon, doamna care te tunde te întreabă de Bitcoin.", "Like"),
    ("Crypto kid vs bani din job", "Eu cu bani din crypto vs eu cu bani din job.", "Comment"),
    ("POV: la pensia mătuașei spui ce csinálsz munkán", "POV: la masă, spui ce faci la muncă — și e crypto.", "Like"),
    ("Reactia bunicii la wallet", "Reacția bunicii când îi explic ce e un «wallet digital».", "Like"),
    ("POV: research = TikTok 30 sec", "POV: prietenul tău a făcut «research» = 30 sec pe TikTok.", "Tag prietenul"),
    ("Tipuri de copii la 8 ani când le explici banii", "Cum reacționează copiii când le explici banii.", "Comment"),
    ("POV: la Lidl, plătești cu crypto?", "POV: prietenul a uitat banii la Lidl — plătești cu crypto?", "Like"),
    ("POV: șeful te invită la «side hustle»", "POV: șeful te invită la «un side hustle simplu».", "Tag colegul"),
    ("Reactia mea când văd «guaranteed 30%»", "Reacția mea când văd «randament garantat 30%».", "Like dacă tu"),
    ("POV: cina romantică, spui ești în crypto", "POV: la cina romantică, spui că ești în crypto.", "Tag pe cineva"),
    ("Tipuri de oameni pe Telegram crypto", "Tipuri de oameni dintr-un grup de Telegram crypto.", "Comment"),
    ("POV: festival, prietenul a pierdut seed", "POV: la festival, prietenul a pierdut seed phrase-ul.", "Like"),
    ("Eu pe TikTok vs eu în viața reală", "Eu pe TikTok vs eu în viața reală cu crypto.", "Comment"),
    ("Tipi care vorbesc despre crypto la sală", "Tipi care vorbesc despre crypto între seturi la sală.", "Tag colegul"),
    ("Reacția când te întreabă «ce coin?»", "Reacția mea când mă întreabă cineva «ce coin?».", "Comment"),
    ("POV: în autobuz, doi seniori vorbesc despre BTC", "POV: în autobuz, doi seniori discută despre Bitcoin.", "Like"),
    ("Crypto teamomi — work from home cu crypto", "Crypto teamomi — mămici work from home în crypto.", "Comment"),
    ("POV: la party, prietenul beat explică DeFi", "POV: prietenul beat la party încearcă să explice DeFi.", "Tag prietenul"),
    ("Tipuri de șefi la «crypto research zi liberă»", "Tipuri de șefi când ceri o zi liberă pentru «crypto research».", "Comment"),
    ("POV: în concediu, dar checking portfolio", "POV: ești în concediu, dar tot la portofoliu te uiți.", "Like"),
    ("Reacția mea la «tu ce ai cumpărat?»", "Reacția mea când mă întreabă «tu ce ai cumpărat?».", "Like"),
    ("POV: când vine factura curentului", "POV: când vine factura și ai cumpărat un alt coin săptămâna trecută.", "Comment"),
    ("Tipuri de oameni dimineața după roșu", "Tipuri de oameni dimineața când piața e roșie.", "Comment"),
    ("POV: copilul te întreabă unde sunt banii", "POV: copilul te întreabă «unde sunt banii?».", "Like"),
    ("Eu cu profit vs Eu cu pierdere", "Eu cu zile de profit vs eu cu zile de pierdere.", "Comment"),
    ("POV: la salon, doamna zice de pump", "POV: la salon, doamna care îți face unghii zice de un pump.", "Like"),
    ("Tipuri de creatori despre crypto", "Tipuri de creatori care vorbesc despre crypto.", "Comment"),
    ("POV: la psiholog explici de ce ești obosit", "POV: la psiholog, explici de ce ești obosit — și e portfolio.", "Like"),
    ("Reacția când prietenul rămâne pe BTC vs alt", "Reacția mea când prietenul rămâne pe BTC vs cel cu alt-coins.", "Comment"),
    ("POV: la doctor, verifici prețul în waiting room", "POV: la doctor, dar tu verifici BTC în waiting room.", "Like"),
    ("Tipuri de comentarii sub un video de crypto", "Tipuri de comentarii sub orice video de crypto.", "Comment"),
    ("POV: prima oară când te-a întrebat ANAF", "POV: prima oară când te-a întrebat ANAF de crypto.", "Like"),
    ("Reacția când prietenul «împrumută» pentru a investi", "Reacția când prietenul împrumută bani să investească în crypto.", "Tag prietenul"),
    ("POV: în vacanță la mare, piața crashează", "POV: ești la mare, dar piața crashează.", "Like"),
    ("Tipuri de soțîi cu soți crypto", "Tipuri de soții cu soți în crypto.", "Tag pe cineva"),
    ("POV: «research» = 3 ore TikTok", "POV: spui «mă duc să fac research» = 3 ore pe TikTok.", "Like"),
    ("Reacția mea la «doar 100 lei»", "Reacția mea la «doar 100 lei, ce ai de pierdut?».", "Comment"),
    ("POV: la cumpărături, dar tot la BTC", "POV: la cumpărături, dar tot la BTC te gândești.", "Like"),
    ("Tipuri de experți pe Twitter", "Tipuri de «experți» pe crypto Twitter.", "Comment"),
    ("POV: tu ai făcut DD vs amicul cu hype", "POV: tu ai făcut DD vs amicul tău cu hype.", "Tag prietenul"),
]

# --- P5 scam (30 db = 1/nap) ---
P5_TOPICS = [
    ("Pig butchering scam RO", "De ce românii sunt ținta preferată a «porc la tăiere».", "Share cu părinții"),
    ("Fake AURA / fake support DM", "NOI NU vă scriem niciodată primii pe DM.", "Screenshot + report"),
    ("Telegram VIP / signal scam", "«Grup VIP» și «signaluri» — cum recunoști capcana.", "Share"),
    ("Rug pull RO/CEE eset", "Un rug pull real — cum a funcționat și cum îl recunoști.", "Share"),
    ("Fake AURA app Play Store", "Aplicația falsă AURA — cum o recunoști.", "Save + share"),
    ("Romance scam + crypto", "Romance scam + crypto — cum funcționează.", "Share cu prietenele"),
    ("Fake celebrity endorsement RO", "«Andrei Hossu vinde Bitcoin» — și de ce e mereu fake.", "Report"),
    ("Recovery scam — după ce ai pierdut", "Recovery scam — al doilea atac, după primul.", "Save"),
    ("Phishing email exchange", "Email de la «exchange» — cum vezi că e phishing.", "Save"),
    ("SIM swap atac", "SIM swap — și de ce 2FA SMS nu e suficient.", "Save"),
    ("Fake giveaway (Elon style)", "«Trimite 1 ETH, primești 2» — niciodată, NICIODATĂ.", "Share"),
    ("Ponzi scheme — Bitconnect 2.0", "Bitconnect 2.0 — semnele unei scheme Ponzi.", "Save"),
    ("ICO scam — proiect fals", "ICO scam — cum recunoști un proiect fără viitor.", "Save"),
    ("Discord moderator impersonation", "«Moderatorul Discord» te scrie — de 99% e scam.", "Save"),
    ("Address poisoning — clipboard", "Address poisoning — cum un virus îți schimbă adresa la copy-paste.", "Save"),
    ("Wallet drainer dApp", "Wallet drainer — site fals care îți golește wallet-ul.", "Save"),
    ("Honeypot token", "Honeypot token — îl cumperi, dar nu poți vinde.", "Save"),
    ("Fake AirDrop — wallet draindere", "AirDrop fals — conectezi wallet-ul, pierzi tot.", "Save"),
    ("MLM crypto scheme", "MLM crypto — cum recunoști o piramidă cu «lider».", "Share"),
    ("Tax refund scam — ANAF impostor", "«ANAF» te sună despre crypto — nu, e scam.", "Save"),
    ("Fake hardware wallet", "Hardware wallet de pe OLX — cum verifici că nu e modificat.", "Save"),
    ("Fake P2P trader OTC", "P2P OTC scam — cum recunoști un trader fals.", "Save"),
    ("Fake escrow service", "Escrow fals — cine «păstrează» banii dispar.", "Save"),
    ("Smart contract approval scam", "«Approval» nelimitat — și de ce îți drainează wallet.", "Save"),
    ("Pump and dump Telegram", "Pump and dump pe Telegram — și de ce pierzi mereu.", "Save"),
    ("Lending platform scam (Celsius)", "Platforme de lending — lecția Celsius.", "Save"),
    ("Fake job offer — interviewer", "Job interviu crypto — drainere prin task fals.", "Save"),
    ("Fake investment seminar", "Seminar de investiții cu plată — întotdeauna scam.", "Save"),
    ("Fake support live chat", "Live chat fals pe site clonă — cum verifici domeniul.", "Save"),
    ("Public WiFi QR code scam", "QR code în cafenea — cum te poate prinde.", "Save"),
]

# --- P4 trend (30 db = 1/nap) — POV-style = pre-recordable, others not ---
P4_TOPICS = [
    ("POV: crypto la masă duminică", "Când cineva îmi explică crypto la masă de duminică.", "Like dacă te-ai văzut", "Igen"),
    ("Trending sound — portofelul vs prieteni", "Cum arată portofelul meu vs ce zic prietenii că am.", "Tag prietenul", "Nem"),
    ("Stitch RO finance creator", "Stitch + adăugare constructivă.", "Comment opinia ta", "Nem"),
    ("Trending sound — «spălat bani» kontra", "Când cineva spune că crypto e doar pentru spălat bani.", "Like", "Nem"),
    ("Trend hijack aktuális", "Trending sound + crypto twist.", "Like", "Nem"),
    ("Duet RO creator", "Duet + build on top.", "Comment", "Nem"),
    ("POV: birou crypto — meeting", "POV: stai în meeting, dar verifici BTC pe sub masă.", "Tag colegul", "Igen"),
    ("POV: tipuri de prieteni «crypto»", "Tipuri de prieteni când le zici că ești în crypto.", "Tag prietenul", "Igen"),
    ("Trend dance + crypto caption", "Trending dance, dar caption-ul e crypto reality.", "Like", "Nem"),
    ("Stitch reply la misinfo", "Stitch + corectează informația greșită.", "Save", "Nem"),
    ("Duet motivational + crypto realism", "Duet creator motivațional + realism crypto.", "Comment", "Nem"),
    ("Trending pop-song + crypto lyric flip", "Schimb versurile unei piese trending — varianta crypto.", "Like", "Nem"),
    ("POV: explici familiei la masă", "POV: explici familiei ce e crypto — ei nu vor să audă.", "Tag pe cineva", "Igen"),
    ("Highlight reel — top momentele lunii", "Top momentele primei luni pe AURA TikTok.", "Like", "Nem"),
    ("Trending dance + funny caption", "Trending dance cu caption «crypto winter».", "Like", "Nem"),
    ("Stitch celebrity statement", "Stitch declarație de celebritate + reality check.", "Comment", "Nem"),
    ("Duet RO commentary creator", "Duet creator de comentariu RO.", "Like", "Nem"),
    ("Trending audio — but make it crypto", "Trending audio — dar crypto edition.", "Like", "Nem"),
    ("POV: prima zi la job vs pe TikTok", "POV: prima zi la job vs prima zi pe TikTok crypto.", "Comment", "Igen"),
    ("Trending sound — speed-talk", "Speed-talk trending — explic 3 concepte în 15 sec.", "Save", "Nem"),
    ("Stitch + educational add", "Stitch video viral + valoare educațională.", "Save", "Nem"),
    ("POV: expert vs începător stil diferit", "POV: cum vorbește un expert vs un începător despre crypto.", "Comment", "Igen"),
    ("Duet RO comedy creator", "Duet creator de comedie RO.", "Like", "Nem"),
    ("POV: la grătar, întrebare crypto", "POV: la grătar, cineva întreabă «ce e Bitcoin?».", "Tag prietenul", "Igen"),
    ("Trending audio reacție", "Trending audio + reacția mea autentică.", "Like", "Nem"),
    ("Stitch RO meme creator", "Stitch cu meme creator RO.", "Comment", "Nem"),
    ("Trending challenge participat", "Particip la challenge-ul trending — dar crypto twist.", "Like", "Nem"),
    ("POV: voice impression boomer", "POV: vorbesc ca tatăl meu boomer despre BTC.", "Like", "Igen"),
    ("Final month CTA + brand outro", "30 de zile, o lecție mare — și ce urmează.", "Link în bio", "Nem"),
    ("POV: în metru, semnal slab dar verifici prețul", "POV: în metrou, semnal slab — dar verifici BTC.", "Like", "Igen"),
]

# --- P6 community / Q&A (30 db = 1/nap) ---
P6_TOPICS = [
    ("Q&A sticker — kezdő kérdések (prompt)", "Lăsați-mi întrebări de începător — răspund mâine.", "Întrebați orice", "Igen"),
    ("Comment coinul tău (prompt)", "Comentează coinul tău — mâine îți zic 1 lucru factual.", "Comment cu coinul", "Igen"),
    ("Tegnapi Q&A top 3 válasz", "Cele mai bune 3 întrebări de ieri — răspunsuri.", "Alte întrebări?", "Nem"),
    ("Coin komment válaszok", "Răspund la 5 coinuri din comments.", "Alte coinuri?", "Nem"),
    ("Live Q&A bejelentés + take 1 komment", "Cea mai bună întrebare a săptămânii — răspuns.", "Alte întrebări?", "Nem"),
    ("Q&A AURA (prompt) — kérdezzetek bármit", "Întrebați-mă orice despre AURA — răspund mâine.", "Întrebări?", "Igen"),
    ("AURA Q&A válaszok (őszinte)", "Răspund la 3 întrebări despre AURA — inclusiv ce încă lucrăm.", "Alte întrebări?", "Nem"),
    ("Community poll — mit a következő 30 napban (prompt)", "M-ați urmărit 30 de zile. Ce vreți să fac în următoarele 30?", "Comment + poll", "Igen"),
    ("Q&A: mit változtassak a 2. hónapban (prompt)", "Ce vreți să schimb în luna 2? Întrebați.", "Comment", "Igen"),
    ("Stitch cinikus kommenttel", "Stitch + răspuns respectuos, factual.", "Comment", "Nem"),
    ("Reagálok a legkedvesebb kommentre", "Reacția mea la cel mai drag comment al săptămânii.", "Like", "Nem"),
    ("Comment cu wallet color (prompt random)", "Comentează ce culoare are wallet-ul tău — prompt random.", "Comment", "Igen"),
    ("Tag prietenul paranoid cu securitatea (prompt)", "Tag prietenul cel mai paranoid cu securitatea — vede asta!", "Tag", "Igen"),
    ("Q&A: cele mai bizare întrebări (reply)", "Cele mai bizare 3 întrebări — și răspunsurile.", "Like", "Nem"),
    ("Live Q&A — tudnivalók pentru hét", "Live Q&A vineri — ce să pregătiți.", "Set reminder", "Nem"),
    ("Comment portfolio split anonymous (prompt)", "Comentează split-ul tău de portofoliu — anonim, fără sume.", "Comment", "Igen"),
    ("Q&A: cele mai mari frici crypto (prompt)", "Care e cea mai mare frică a ta în crypto? Spune-mi.", "Comment", "Igen"),
    ("Răspuns la cea mai populară comment", "Răspund la comment-ul cu cele mai multe likes.", "Like", "Nem"),
    ("Poll: ce vrei să-ți explic? (prompt)", "Vot: care 3 subiecte vrei să le acopăr următoarea săptămână?", "Vote", "Igen"),
    ("Reply video la o întrebare anonimă", "Reply video la o întrebare bună anonimă din DM.", "Comment", "Nem"),
    ("Community shoutout — top commentator", "Shoutout pentru cel mai bun commentator al săptămânii.", "Tag", "Nem"),
    ("Q&A: ce coin mă întrebați des? (prompt)", "Care coin mă întrebați cel mai des? Comentează-l.", "Comment", "Igen"),
    ("AMA wrap — best 3 ale lunii", "Top 3 întrebări AMA ale lunii — cu răspunsuri.", "Save", "Nem"),
    ("Q&A despre AURA features (reply)", "Răspund la 3 întrebări despre features AURA.", "Comment", "Nem"),
    ("Tag amicul tău crypto skeptic (prompt)", "Tag amicul tău cel mai skeptic cu crypto.", "Tag", "Igen"),
    ("Comment «începător» vs «expert» (prompt)", "Te simți începător sau expert? Comentează unul.", "Comment", "Igen"),
    ("Q&A: care a fost prima cumpărare? (prompt)", "Care a fost prima ta cumpărare crypto? Comentează.", "Comment", "Igen"),
    ("Reply la «de ce nu ai răspuns?» (apology)", "Reply video — știu, n-am răspuns la X. Iată acum.", "Like", "Nem"),
    ("Comment greșeala ta crypto (prompt)", "Comentează cea mai mare greșeală a ta în crypto.", "Comment", "Igen"),
    ("Final community thank you", "Mulțumesc pentru 30 de zile — voi sunteți AURA.", "Like + share", "Igen"),
]


def main():
    header = [
        "#", "Day", "Date", "Weekday", "PostTime",
        "Pillar", "PreRecord",
        "Topic", "Hook (RO)", "CTA",
        "Status", "Notes",
    ]
    rows = [header]
    idx = {p: 0 for p in ["P2", "P3", "P4", "P5", "P6"]}
    counter = 0
    for offset in range(30):
        d = START + timedelta(days=offset)
        wd = d.weekday()
        for slot_label, ptime, pillar in SLOTS:
            counter += 1
            day_label = f"D{offset+1}"
            weekday_str = WEEKDAY_HU[wd]

            if pillar == "P1":
                if slot_label == "S1":
                    topic, hook = WEEKDAY_MORNING_NEWS[wd]
                    cta, pre = "Follow", "Nem"
                elif slot_label == "S4":
                    topic, hook = MIDDAY_MARKET
                    cta, pre = "Follow", "Nem"
                else:  # S9
                    topic, hook = EVENING_WRAP
                    cta, pre = "Save", "Nem"
            elif pillar == "P2":
                topic, hook, cta = P2_TOPICS[idx["P2"] % len(P2_TOPICS)]
                idx["P2"] += 1
                pre = "Igen"
            elif pillar == "P3":
                topic, hook, cta = P3_TOPICS[idx["P3"] % len(P3_TOPICS)]
                idx["P3"] += 1
                pre = "Igen"
            elif pillar == "P4":
                topic, hook, cta, pre = P4_TOPICS[idx["P4"] % len(P4_TOPICS)]
                idx["P4"] += 1
            elif pillar == "P5":
                topic, hook, cta = P5_TOPICS[idx["P5"] % len(P5_TOPICS)]
                idx["P5"] += 1
                pre = "Igen"
            elif pillar == "P6":
                topic, hook, cta, pre = P6_TOPICS[idx["P6"] % len(P6_TOPICS)]
                idx["P6"] += 1

            rows.append([
                counter, day_label, d.isoformat(), weekday_str,
                ptime, pillar, pre,
                topic, hook, cta,
                "Planned", "",
            ])

    with open("AURA_RO_TikTok_tracker.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f, quoting=csv.QUOTE_MINIMAL).writerows(rows)
    igen = sum(1 for r in rows[1:] if r[8] == "Igen")
    print(f"Wrote {len(rows)-1} rows. PreRecord=Igen: {igen}, Nem: {len(rows)-1-igen}")


if __name__ == "__main__":
    main()
