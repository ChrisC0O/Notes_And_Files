# **Ultimativ dybdegående guide til at organisere din MediaWiki-side**  
*Hvorfor du gør det, hvordan det virker, konkrete eksempler og trin-for-trin-bedste-praksis*

---

## Indledning: Hvorfor organisering er vigtigt

Forestil dig din wiki som en **by**.  
Uden gader (navnerum), trafiklys (skabeloner) eller kort (kategorier) bliver brugerne fortabte.  
God organisering = **findbarhed**, **skalerbarhed**, **vedligeholdelse** og **samarbejde**.

> **Mål**: Alle skal kunne finde indhold på under 3 klik.  
> **Resultat**: Flere redigeringer, færre dubletter, gladere brugere.

Lad os bygge den by — **mursten for mursten**, med **begrundelser**, **eksempler** og **præcise trin**.

---

## 1. **Navnerum (Namespaces): Byens distrikter**

### Hvad er navnerum?

Navnerum er **foruddefinerede zoner** til forskellige typer indhold.  
Tænk på dem som **bydele**:
- **Centrum** = Hovedindhold (artikler)
- **Rådhus** = Projekt: (regler, portaler)
- **Bibliotek** = Hjælp: (vejledninger)
- **Lager** = Fil: (billeder, PDF’er)

Hvert navnerum har:
- Et **navn** (f.eks. `Hjælp`)
- Et **ID** (f.eks. 12)
- En **diskussionsside** (f.eks. Hjælp diskussion:13)

---

### Fuldt navnerum-oversigt (med virkelige anvendelser)

| ID | Navnerum | Diskussion | Formål & **hvorfor bruge det** | Eksempel |
|----|----------|------------|--------------------------------|----------|
| 0 | **(Hoved)** | 1 | **Kerneartikler** — kun rigtigt indhold | `Solsystemet`, `Python-programmering` |
| 2 | **Bruger** | 3 | **Personligt rum** — kladder, sandkasse, bruger-CSS | `Bruger:Alice/Sandkasse` |
| 4 | **Projekt** | 5 | **Wiki-styring** — regler, portaler, om | `WikiRegler`, `Portal:Naturvidenskab` |
| 6 | **Fil** | 7 | **Mediemetadata** — licens, kilde, beskrivelse | `Fil:Jorden.jpg` |
| 8 | **MediaWiki** | 9 | **Systemgrænseflade** — knapper, beskeder | `MediaWiki:Sidebjælke` |
| 10 | **Skabelon** | 11 | **Genanvendelige blokke** — infobokse, advarsler | `Skabelon:Infoboks planet` |
| 12 | **Hjælp** | 13 | **Brugervejledninger** — hvordan man redigerer, formaterer | `Hjælp:Redigering` |
| 14 | **Kategori** | 15 | **Dynamiske indekser** — automatiske lister | `Kategori:Planeter` |

---

### Sådan bruger du navnerum (trin for trin)

#### **Trin 1: Opret en side i et navnerum**
1. Gå til URL: `https://dinwiki.dk/wiki/Hjælp:Hvordan_man_redigerer`
2. Klik **"Opret"** → rediger → gem.

> **Hvorfor?** Holder hjælp adskilt fra artikler. Ingen rod.

#### **Trin 2: Link til navnerum**
```wiki
[[Hjælp:Redigering]] → Hjælp:Redigering  
[[Bruger:Bob]] → Bruger:Bob  
[[Skabelon:Stub]] → {{Stub}} (løser automatisk)
```

> **Pro-tip**: Brug `{{ns:help}}` → udskriver "Hjælp"

#### **Trin 3: Søg efter navnerum**
Brug **Special:Søg** → Avanceret → kryds af "Hjælp" kun.

---

### **Brugerdefinerede navnerum (når du har brug for dem)**

Har du 100+ sider om **Opskrifter**? Opret `Opskrift:` navnerum.

**Hvordan (i LocalSettings.php):**
```php
$wgExtraNamespaces[100] = "Opskrift";
$wgExtraNamespaces[101] = "Opskrift_diskussion";
```

Nu opret: `Opskrift:Chokoladekage`

> **Hvorfor?** Forhindrer `Chokoladekage` i at kollidere med `Chokoladekage (band)`  
> **Hvornår?** Først efter 50+ sider af samme type.

---

## 2. **Kategorier: Byens kort (selvopdaterende!)**

### Hvad er kategorier?

**Dynamiske lister** over sider, der deler et træk.

```wiki
[[Kategori:Planeter]]
```
→ Tilføjer siden til `Kategori:Planeter` **automatisk**.

---

### Sådan fungerer kategorier (bag kulisserne)

1. Du tilføjer `[[Kategori:X]]` → siden tilslutter sig listen.
2. `Kategori:X`-siden viser **alle medlemmer**.
3. Underkategorier: `[[Kategori:Planeter]]` på `Kategori:Gasgiganter`

```
Kategori:Indhold
 └── Kategori:Naturvidenskab
      ├── Kategori:Fysik
      └── Kategori:Astronomi
           └── Kategori:Planeter
                ├── Mars
                └── Jupiter
```

---

### **Trin-for-trin: Byg et kategoritræ**

#### **1. Opret rod-kategori**
```wiki
[[Kategori:Indhold]]
```
Side: `Kategori:Indhold` → dit **wiki-kort**

#### **2. Tilføj underkategorier**
På `Kategori:Naturvidenskab`:
```wiki
[[Kategori:Indhold]]
```

#### **3. Kategorisér artikler**
På `Mars`-siden:
```wiki
[[Kategori:Planeter]]
[[Kategori:Jordlignende planeter]]
```

#### **4. Sortér korrekt**
```wiki
{{DEFAULTSORT:Mars}}
[[Kategori:Planeter]]
```
→ Sorterer under "Mars", ikke "mars"

---

### **Konkret eksempel: Wikipedia-stil kategoritræ**

```
Kategori:Rod
 └── Kategori:Teknologi
      ├── Kategori:Programmering
      │    ├── Python
      │    └── JavaScript
      └── Kategori:Hardware
           └── CPU
```

---

### **Bedste praksis (med begrundelser)**

| Regel | Hvorfor | Hvordan |
|-------|---------|---------|
| **Kun ét kategoritræ** | Undgår forvirring | Alle topniveauer → `Kategori:Indhold` |
| **Max 5–7 kat. pr. side** | For mange = støj | Prioritér mest specifikke |
| **Brug sorteringsnøgler** | Alfabetisk kaos | `[[Kategori:Personer|Einstein, Albert]]` |
| **Skjul vedligeholdelses-kat.** | Ren brugerflade | Tilføj `__HIDDENCAT__` til `Kategori:Stub` |
| **Ingen omdirigerede kategorier** | Bryder links | Brug `{{Kategori omdirigering}}` skabelon |

---

## 3. **Skabeloner: De genanvendelige LEGO-klodser**

### Hvad er skabeloner?

**Kodesnipper** du indsætter med `{{Navn}}`.

---

### **Eksempel: Infoboks-skabelon**

#### **Skabelon:Infoboks planet** (`Skabelon:Infoboks planet`)
```wiki
<includeonly>{| class="infobox" style="width:22em;"
! colspan="2" | {{{navn}}}
|-
| '''Diameter''' || {{{diameter|Ukendt}}}
|-
| '''Måner''' || {{{måner|0}}}
|}</includeonly>

<noinclude>
== Brug ==
{{Infoboks planet
| navn = Mars
| diameter = 6.779 km
| måner = 2
}}
[[Kategori:Infoboks-skabeloner]]
</noinclude>
```

#### **Brug på Mars-siden:**
```wiki
{{Infoboks planet
| navn = Mars
| diameter = 6.779 km
| måner = 2
}}
```

→ Giver en pæn boks. Opdater skabelon → **alle planeter opdateres**.

---

### **Skabelon-tags forklaret**

| Tag | Hvor vises det | Anvendelse |
|-----|----------------|------------|
| `<includeonly>` | Kun ved transklusion | Hovedindhold |
| `<noinclude>` | Kun på skabelonsiden | Dokumentation, kategorier |
| `<onlyinclude>` | Kun den del, der transkluderes | Delvis genbrug |

---

### **Navigationsbjælke-skabelon**

#### `Skabelon:Navigationsbjælke`
```wiki
<includeonly><div class="navbar">
[[:Kategori:Fysik|Fysik]] | [[:Kategori:Biologi|Biologi]] | [[Hjælp:Redigering|Hjælp]]
</div></includeonly>

<noinclude>
Tilføj øverst på sider: {{Navigationsbjælke}}
</noinclude>
```

→ Én ændring = hele sitet opdateret.

---

## 4. **Sidestruktur & navigation**

### **Forside-layout (eksempel)**

```wiki
{{Portal boks}}
== Velkommen til MinWiki ==
Søg eller gennemse nedenfor.

{{Søgeboks}}

== Fremhævede emner ==
{{Portalliste}}

== Ny her? ==
[[Hjælp:Redigering]] | [[Projekt:Fællesskabsportal]]
```

---

### **Brødkrummer (navigationssti)**

#### `Skabelon:Brødkrumme`
```wiki
<includeonly><small>
[[Hovedside]] > {{#if:{{{1|}}}|[[{{{1}}}]] > }}{{{2|}}}
</small></includeonly>
```

Brug:
```wiki
{{Brødkrumme|Naturvidenskab|Fysik}}
```
→ `Hovedside > Naturvidenskab > Fysik`

---

### **Undersider: Hierarkisk indhold**

Aktivér i `LocalSettings.php`:
```php
$wgNamespacesWithSubpages[NS_MAIN] = true;
```

Nu:
- `Python/Funktioner`
- `Python/Klasser`

> **Hvorfor?** Logisk gruppering  
> **Hvornår ikke?** Brug kategorier til krydslinks

---

## 5. **Filer & medier**

### Upload & indsæt

1. Gå til **Special:Upload**
2. Fil: `Fil:Jorden fra rummet.jpg`
3. Beskrivelsesside:
   ```wiki
   == Resumé ==
   Jorden fra Apollo 17.

   == Licens ==
   {{PD-USGov-NASA}}
   ```

Indsæt:
```wiki
[[Fil:Jorden fra rummet.jpg|thumb|right|Jorden fra rummet]]
```

---

## 6. **Fuld tjekliste for bedste praksis**

| Område | Gør dette | Hvorfor |
|--------|-----------|---------|
| **Indhold** | Kladd i `Bruger:Dig/Kladde` → flyt til Hoved | Forhindrer ødelagte links |
| **Navngivning** | `Hjælp:Hvordan man redigerer` (ikke `hvordanmanredigerer`) | Søgbar, ensartet |
| **Skabeloner** | Dokumentér med `/doc` underside | Fremtidssikret |
| **Kategorier** | Én rod: `Kategori:Indhold` | Én sandhedskilde |
| **Diskussionssider** | Brug til alle større ændringer | Gennemsigtighed |
| **Omdirigeringer** | `#REDIRECT [[Mål]]` | Håndterer gamle navne |
| **Vedligehold** | Patrolér Special:Nylige ændringer | Fang hærværk hurtigt |

---

## 7. **Eksempel på wiki-struktur (lille wiki)**

```
Hovedside
 ├── Portal:Naturvidenskab
 │    ├── Fysik
 │    └── Biologi
 ├── Hjælp:Redigering
 ├── Projekt:Regler
 └── Bruger:Alice/Sandkasse

Kategori:Indhold
 └── Kategori:Naturvidenskab
      └── Kategori:Fysik

Skabelon:Infoboks
Skabelon:Stub
Skabelon:Navigationsbjælke
```

---

## 8. **Pro-tips fra rigtige wikier**

1. **Kopiér Wikipedia-skabeloner** via **Special:Export**
2. **Brug VisualEditor** til nybegyndere
3. **Aktivér DiscussionTools** for bedre diskussionssider
4. **Tilføj en søgeboks** på hver side
5. **Sikkerhedskopiér månedligt** med `Special:Export` (XML)

---

## Ressourcer

- [MediaWiki.org](https://www.mediawiki.org) *(engelsk)*
- [Manual:Namespaces](https://www.mediawiki.org/wiki/Manual:Namespaces)
- [Hjælp:Kategorier](https://www.mediawiki.org/wiki/Help:Categories/da)
- [Skabelondokumentation](https://www.mediawiki.org/wiki/Help:Templates)

---

**Du har nu en blueprint til at bygge en ren, skalerbar, brugervenlig wiki.**  
Start småt. Tilføj én skabelon. Ét kategoritræ. Se det vokse.

**God organisering!**
