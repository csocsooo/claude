# Agent-hálózat (orchestrator + al-agentek)

Ez a mappa egy **orchestrator + al-agent** felállást tartalmaz a Claude Code-hoz.
Egy koordinátor agent összetett feladatokat bont fel, és speciális al-agenteknek
delegál. A topológia egy 2 szintű "csillag": 1 koordinátor → N munkás-agent.

```
            ┌──────────────┐
            │ orchestrator │   ← felbont, delegál, szintetizál
            └──────┬───────┘
       ┌───────────┼───────────┬───────────────┐
       ▼           ▼           ▼               ▼
  ┌────────┐  ┌─────────┐  ┌─────────┐   ┌────────────┐
  │ kutato │  │fejleszto│  │tesztelo │   │ kodellenor │
  └────────┘  └─────────┘  └─────────┘   └────────────┘
   (olvas)     (módosít)   (tesztel)      (review)
```

## Az agentek

| Agent         | Szerep                        | Jogosultság           | Modell  |
|---------------|-------------------------------|-----------------------|---------|
| `orchestrator`| Koordinálás, delegálás        | `Task` + olvasás      | opus    |
| `kutato`      | Kódbázis feltérképezése       | csak olvasás          | sonnet  |
| `fejleszto`   | Implementáció                 | olvasás + írás + Bash | sonnet  |
| `tesztelo`    | Tesztek írása/futtatása       | olvasás + írás + Bash | sonnet  |
| `kodellenor`  | Változások átnézése           | csak olvasás + Bash   | opus    |

## Használat

A fő Claude Code munkamenetben egyszerűen kérd a koordinátort, pl.:

> Használd az `orchestrator` agentet: implementáld az X funkciót, írj rá tesztet,
> és nézesd át a változást.

A koordinátor felbontja a feladatot, és a `Task` eszközzel elindítja a megfelelő
al-agenteket — ahol lehet, párhuzamosan. A részeredményeket összegzi, és a végén
egyetlen, összefüggő választ ad vissza.

Al-agentet közvetlenül is meghívhatsz, az orchestrator megkerülésével:

> Kérd meg a `kutato` agentet, hogy térképezze fel, hol kezeljük az autentikációt.

## Hogyan működik a delegálás?

- Minden al-agent **külön kontextusban** fut: csak azt látja, amit a hívó átad
  neki, a teljes beszélgetést nem. Ezért fontos, hogy a koordinátor pontos,
  önmagában értelmezhető utasítást adjon.
- Az al-agent a saját, **szűkített toolkészletével** dolgozik (lásd a táblázat).
  A `kutato` és a `kodellenor` szándékosan nem tud írni.
- Az al-agent **utolsó üzenete** tér vissza a hívóhoz eredményként — a részletes
  lépéseit a felhasználó nem látja, ezért az al-agenteket úgy hangoltuk, hogy a
  végén tömör, érthető összefoglalót adjanak.

## Mélyebb hálózat (több szint)

Alapból az al-agentek **nem** kapnak `Task` eszközt, így nem indítanak további
al-agenteket — ez tudatos: a megbízható minta a 2 szintű csillag. Ha tényleg
mély, tetszőleges topológiájú agent-hálózatot szeretnél (agentek, akik egymásnak
delegálnak), arra a **Claude Agent SDK** (Python/TypeScript) a megfelelő eszköz,
ahol programból írod meg a vezérlési logikát.

## Testreszabás

- Új agent: hozz létre egy `.md` fájlt itt, a fenti frontmatter-mintával
  (`name`, `description`, `tools`, `model`).
- A `description` mező a döntő: ez alapján választ a koordinátor (és a fő agent),
  hogy mikor hívja az adott al-agentet — írd minél egyértelműbbre.
- A `tools` mezővel szűkítsd a jogosultságot a szerephez (legkisebb jogosultság elve).
