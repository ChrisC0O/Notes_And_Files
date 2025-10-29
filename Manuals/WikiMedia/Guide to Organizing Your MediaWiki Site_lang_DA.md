# **ULTIMATIV, EKSTREMT, TOTALT UDDYBENDE GUIDE TIL AT ORGANISERE DIN MEDIAWIKI**  
*Alt på dansk – men alle tekniske MediaWiki-termer står på **original engelsk** (namespace, template, category, transclusion osv.).  
Denne guide er **den mest detaljerede nogensinde** – hver linje, hver handling, hvert klik, hver database-forespørgsel, hvert scenarie er forklaret.  
Ingen sten bliver uforstyrret.*

---

## **INDLEDNING: HVORFOR ORGANISERING ER LIV ELLER DØD FOR DIN WIKI**

En wiki er ikke bare en samling af sider – det er et **levende, voksende økosystem**.  
Uden struktur bliver det:

| Symptom | Årsag | Konsekvens |
|--------|-------|------------|
| Brugere finder ikke indhold | Ingen klar navigation | De forlader |
| Dubletter opstår | Ingen kategori-struktur | Kaos |
| Templates bryder | Forkert brug af tags | Inkonsistens |
| Vandalisme spredes | Ingen patrol | Tab af tillid |

> **Målet med denne guide**  
> - **0% forvirring**  
> - **100% skalerbarhed**  
> - **Automatisk vedligeholdelse**  
> - **Nybegynder-venlig, ekspert-robust**

---

## **1. NAMESPACES – DEN ARKITEKTONISKE GRUNDPLAN FOR HELE WIKIEN**

### **Hvad er et namespace – helt nede på database-niveau?**

Et **namespace** er en **logisk partition** i MediaWiki-databasen.  
Hver side gemmes i tabellen `page` med felterne:

| Felt | Eksempel | Betydning |
|------|---------|-----------|
| `page_id` | 123 | Unikt ID |
| `page_title` | `Redigering` | Titel uden namespace |
| `page_namespace` | 12 | Namespace ID (her: Help) |

Når du skriver `Help:Redigering`, sker følgende:

1. **Parser** splitter titlen ved `:`  
2. **Slår op i `$wgCanonicalNamespaceNames`** → finder ID 12  
3. **Kombinerer** → `page_namespace=12`, `page_title="Redigering"`  
4. **Henter siden** fra databasen

---

### **KOMPLET NAMESPACE-OVERSIGT MED ALT**

| ID | Namespace | Talk ID | **Formål (præcis)** | **Hvorfor det er vigtigt** | **Eksempel** | **Rettigheder** | **Subpages?** | **Transclusion?** |
|----|-----------|---------|---------------------|---------------------------|--------------|-----------------|---------------|-------------------|
| -2 | **Media** | – | Direkte link til filens **rå data** (ikke beskrivelsessiden) | Bruges i `<img src=>` eller når du vil have filen uden metadata | `[[Media:Logo.png]]` → `https://wiki.com/images/Logo.png` | Ingen redigering | Nej | Nej |
| -1 | **Special** | – | Dynamisk genererede sider (ikke i databasen) | Systemfunktioner: søgning, statistik, admin | `Special:Version` | Kun system | Nej | Nej |
| 0 | **(Main)** | 1 | **Kerneindhold** – artikler, leksika, fakta | Dette er det, læserne kommer for | `Python`, `København` | Alle kan redigere | Ja (hvis aktiveret) | Ja |
| 1 | **Talk** | – | Diskussion om Main-sider | Samarbejde, forslag, konsensus | `Talk:Python` | Alle | Ja | Nej |
| 2 | **User** | 3 | Personligt rum: drafts, sandbox, CSS/JS | Sikker testplads, personlig tilpasning | `User:Alice/Sandbox` | Kun ejer + admins | Ja | Ja (begrænset) |
| 3 | **User talk** | – | Beskeder til brugere | Notifikationer, kommunikation | `User talk:Alice` | Alle | Ja | Nej |
| 4 | **Project** | 5 | Wikiens "meta" – regler, portaler, om | Central styring, branding | `Project:Retningslinjer` | Alle | Ja | Ja |
| 5 | **Project talk** | – | Diskussion om Project-sider | Konsensus om regler | `Project talk:Retningslinjer` | Alle | Ja | Nej |
| 6 | **File** | 7 | Metadata for uploadede filer | Licens, kilde, beskrivelse, versionering | `File:Earth.jpg` | Alle (med upload-rettighed) | Nej | Ja |
| 7 | **File talk** | – | Diskussion om filer | Klarhed om brug, ophavsret | `File talk:Earth.jpg` | Alle | Nej | Nej |
| 8 | **MediaWiki** | 9 | Systembeskeder, interface-tekster | Oversættelse, tilpasning af UI | `MediaWiki:Sidebar` | Kun interface-admins | Nej | Ja |
| 9 | **MediaWiki talk** | – | Diskussion om systembeskeder | Koordinering | `MediaWiki talk:Sidebar` | Alle | Nej | Nej |
| 10 | **Template** | 11 | Genanvendelige kodesnipper | Konsistens, automatisering | `Template:Infobox` | Alle | Ja | **Ja (transclusion)** |
| 11 | **Template talk** | – | Diskussion om templates | Forbedringer, fejlretning | `Template talk:Infobox` | Alle | Ja | Nej |
| 12 | **Help** | 13 | Brugervejledninger | Onboarding, selvbetjening | `Help:Redigering` | Alle | Ja | Ja |
| 13 | **Help talk** | – | Feedback på vejledninger | Forbedring | `Help talk:Redigering` | Alle | Ja | Nej |
| 14 | **Category** | 15 | Dynamiske lister over sider | Navigation, søgning, struktur | `Category:Planeter` | Alle | Nej | Ja |
| 15 | **Category talk** | – | Diskussion om kategorier | Struktur, navngivning | `Category talk:Planeter` | Alle | Nej | Nej |

---

### **SÅDAN OPRETTER DU EN SIDE I ET NAMESPACE – TRIN FOR TRIN MED ALT**

#### **Eksempel: Opret `Help:Redigering` fra bunden**

1. **Åbn browser** → gå til:
   ```
   https://dinwiki.dk/wiki/Help:Redigering
   ```
2. **Siden findes ikke** → rød link → klik på **"Opret"**.
3. **Redigeringsvindue åbnes** → indsæt:
   ```wiki
   = Sådan redigerer du en side =

   1. Klik på fanen '''Rediger''' øverst.
   2. Skriv dit indhold.
   3. Brug [[Help:Formatering|formatering]] for at gøre teksten pæn.
   4. Skriv en kort [[Help:Redigeringsresumé|redigeringsresumé]].
   5. Klik '''Gem side'''.

   {{Tip|Hvis du er usikker, brug [[Help:Sandbox|sandkassen]] først!}}

   [[Category:Hjælpesider]]
   [[Category:Grundlæggende redigering]]
   ```
4. **Klik "Vis eksempel"** → tjek:
   - Overskrift er niveau 1
   - Nummereret liste vises korrekt
   - Template `{{Tip}}` vises som boks
5. **Udfyld redigeringsresumé**:
   ```
   Oprettede grundlæggende redigeringsguide
   ```
6. **Klik "Gem side"**.

> **Hvad sker i databasen?**  
> - Ny række i `page` med `page_namespace=12`, `page_title="Redigering"`  
> - Ny revision i `revision`  
> - Kategorilinks i `categorylinks` for `Hjælpesider` og `Grundlæggende redigering`

---

### **LINKS TIL NAMESPACES – ALLE MULIGHEDER**

| Syntax | Resultat | Hvornår bruges det? |
|-------|----------|---------------------|
| `[[Help:Redigering]]` | Help:Redigering | Normalt link |
| `[[Help:Redigering|hvordan man redigerer]]` | hvordan man redigerer | Brugerdefineret tekst |
| `[[User:Alice]]` | User:Alice | Går til brugerprofil |
| `[[User:Alice/Sandbox|sandkasse]]` | sandkasse | Subpage-link |
| `[[Template:Stub]]` | Template:Stub | Link til template |
| `{{Stub}}` | (indhold af Template:Stub) | **Transclusion** |
| `{{FULLPAGENAME}}` | `Help:Redigering` | Viser fuld titel |
| `{{NAMESPACE}}` | `Help` | Viser kun namespace |
| `{{ns:help}}` | `Help` | Namespace-navn som tekst |
| `{{int:edit}}` | `Rediger` | Oversat systemtekst |

---

### **CUSTOM NAMESPACES – FRA IDÉ TIL FÆRDIG IMPLEMENTERING**

#### **Hvornår skal du bruge custom namespaces?**

| Situation | Eksempel | Namespace | Begrundelse |
|----------|----------|-----------|-------------|
| 100+ opskrifter | `Chokoladekage` | `Opskrift:` | Undgå kollision med `Chokoladekage (band)` |
| API-dokumentation | `GET /users` | `API:` | Adskil fra Main |
| Bogprojekt | `Kap 1: Indledning` | `Bog:` | Hierarkisk struktur |

#### **Fuld opsætning i `LocalSettings.php`**

```php
# === OPSKRIFT NAMESPACE ===
$wgExtraNamespaces[100] = "Opskrift";
$wgExtraNamespaces[101] = "Opskrift_talk";

# Tillad subpages (f.eks. Opskrift:Chokoladekage/Ingredienser)
$wgNamespacesWithSubpages[100] = true;

# Søg i Opskrift som standard
$wgNamespacesToBeSearchedDefault[100] = true;

# Beskyttelse (valgfrit)
$wgNamespaceProtection[100] = array("edit-opskrift");  # Kræver rettighed
$wgGroupPermissions['editor']['edit-opskrift'] = true;
```

> **Genindlæs siden** – ingen server-genstart nødvendig.

#### **Opret første side**

1. Gå til: `https://dinwiki.dk/wiki/Opskrift:Chokoladekage`
2. Opret med:
   ```wiki
   = Chokoladekage =

   {{Infobox opskrift
   | sværhedsgrad = Let
   | tid = 45 min
   | portioner = 8
   }}

   == Ingredienser ==
   * 200 g mørk chokolade
   * 200 g smør

   [[Category:Chokoladeopskrifter]]
   [[Category:Kager]]
   ```

---

## **2. CATEGORIES – DET SELVOPDATERENDE NAVIGATIONSSYSTEM**

### **Hvad sker der præcist, når du skriver `[[Category:Planeter]]`?**

1. **Parser** finder `[[Category:Planeter]]`  
2. **Tjekker om `Category:Planeter` findes** → opretter hvis ikke  
3. **Tilføjer række i `categorylinks` tabellen**:
   ```sql
   INSERT INTO categorylinks (cl_from, cl_to, cl_sortkey, cl_timestamp)
   VALUES (123, 'Planeter', 'MARS', '20251029123456');
   ```
4. **Næste gang `Category:Planeter` vises** → SQL:
   ```sql
   SELECT page_title FROM page
   JOIN categorylinks ON page_id = cl_from
   WHERE cl_to = 'Planeter'
   ORDER BY cl_sortkey;
   ```

---

### **BYG ET FULDT CATEGORY TREE – TRIN FOR TRIN MED ALLE DETALJER**

#### **Trin 1: Opret rod-kategorien `Category:Indhold`**

```wiki
= Wikiens indhold =

Dette er hovedkategorien. Alle andre kategorier skal være under denne.

[[Category:Wiki-struktur]]
```

#### **Trin 2: Opret hovedkategorier**

På `Category:Naturvidenskab`:
```wiki
= Naturvidenskab =

[[Category:Indhold]]
```

#### **Trin 3: Opret underkategorier**

På `Category:Astronomi`:
```wiki
= Astronomi =

[[Category:Naturvidenskab]]
```

#### **Trin 4: Kategorisér en artikel**

På `Mars`:
```wiki
{{DEFAULTSORT:Mars}}
[[Category:Planeter]]
[[Category:Jordlignende planeter]]
[[Category:Solsystemet]]
[[Category:Opdaget i 1600-tallet]]
```

> **Hvorfor `DEFAULTSORT`?**  
> - Uden: Sorteres under "M" for "Mars"  
> - Med: Sorteres under "Mars" (ignoreres "Den røde planet" osv.)  
> - Virker på **alle kategorier** på siden

---

### **AVANCEREDE CATEGORY-TEKNIKKER MED KODE**

| Teknik | Kode | Effekt | Hvornår bruges |
|-------|------|--------|----------------|
| **Sort key** | `[[Category:Personer|Einstein, Albert]]` | Sorteres under "Einstein, Albert" | Personnavne |
| **Hidden category** | `__HIDDENCAT__` på `Category:Stub` | Skjules i bunden af sider | Vedligeholdelse |
| **Category redirect** | `{{Category redirect|Kategori:Gamle planeter}}` | Omdirigerer kategori | Oprydning |
| **Category tree** | `<categorytree mode=pages>Planeter</categorytree>` | Vis træ i artikel | Navigation |
| **Dynamic category** | `{{#ifexist:Template:Stub|[[Category:Stub-sider]]}}` | Tilføj kun hvis template findes | Avanceret |

---

## **3. TEMPLATES – DEN MAGISKE GENBRUGS-MASKINE**

### **Hvad sker ved `{{Infobox}}` – trin for trin**

1. **Parser** finder `{{Infobox}}`  
2. **Søger i Template namespace** → `Template:Infobox`  
3. **Henter indhold**  
4. **Erstatter `{{{parameter}}}`** med værdier fra brug  
5. **Transcluderer** resultatet  
6. **Cachelagrer** i `objectcache` tabellen  
7. **Ved ændring i template** → cache ryddes → alle sider opdateres ved næste visning

---

### **FULD INFOBOX MED ALLE FUNKTIONER**

#### **`Template:Infobox planet`**
```wiki
<includeonly>{| class="infobox" style="float:right; width:22em; font-size:90%; background:#f9f9f9; border:1px solid #aaa;"
|-
! colspan="2" style="font-size:120%; text-align:center; background:#ddf;" | {{{name|{{PAGENAME}}}}}
{{#if: {{{image|}}} | {{!}}-
{{!}} colspan="2" style="text-align:center;" {{!}} [[File:{{{image}}}|220px|alt={{{name}}}]]
}}
|-
{{#if: {{{diameter|}}} | {{!}} '''Diameter''' {{!!}} {{{diameter}}} }}
|-
{{#if: {{{moons|}}} | {{!}} '''Måner''' {{!!}} {{{moons}}} }}
|-
| colspan="2" style="text-align:center; font-size:85%; color:#555;" | 
''Sidst opdateret: {{REVISIONMONTH}}/{{REVISIONYEAR}}''
|}</includeonly>

<noinclude>{{Infobox planet/doc}}</noinclude>
```

#### **`Template:Infobox planet/doc`**
```wiki
== Brug ==
<pre>
{{Infobox planet
| name = Mars
| image = Mars.jpg
| diameter = 6.779 km
| moons = 2
}}
</pre>

== Parametre ==
* '''name''' – planetens navn (valgfri, bruger sidetitel hvis tom)
* '''image''' – billede (uden File:)
* '''diameter''' – i km
* '''moons''' – antal

[[Category:Infobox templates]]
</noinclude>
```

---

## **4. NAVIGATION & SIDESTRUKTUR – ALT**

### **Main Page – din velkomstportal**

```wiki
{{Navbar}}

== Velkommen til [[Project:Om|DinWiki]] ==
{{Search box}}

{{Portal box
| Naturvidenskab | Teknologi | Kultur
}}

== Seneste ændringer ==
{{Special:RecentChanges/10}}

== Hjælp ==
* [[Help:Redigering]]
* [[Help:Formatering]]
* [[Help:Sandbox|Sandkasse]]
```

---

## **5. FILES – KORREKT UPLOAD OG BRUG**

### **Upload-trin – med alt**

1. **Special:Upload**  
2. Vælg fil → `Earth.jpg`  
3. **Beskrivelsesside**:
   ```wiki
   == Resumé ==
   Jorden set fra Apollo 17.

   == Kilde ==
   NASA

   == Licens ==
   {{PD-USGov-NASA}}

   [[Category:Billeder fra rummet]]
   [[Category:NASA-billeder]]
   ```
4. **Embed**:
   ```wiki
   [[File:Earth.jpg
   |thumb
   |right
   |250px
   |Jorden set fra rummet
   |alt=Jorden fra Apollo 17
   ]]
   ```

---

## **6. FULD CHECKLIST – FRA A TIL Z**

| Område | Regel | Hvorfor | Hvordan | Eksempel |
|--------|------|---------|---------|----------|
| **Content** | Draft i `User:` → flyt til Main | Undgå ødelagte links | `Move` funktion | `User:Dig/Draft` → `Python` |
| **Naming** | `Help:Hvordan man redigerer` | Søgbar | Undgå specialtegn | `Help:Redigering` |
| **Templates** | Altid `/doc` | Klarhed | `{{Documentation}}` | `Template:Infobox/doc` |
| **Categories** | Én rod: `Category:Indhold` | Enhed | Subcategories | `Category:Indhold` |
| **Talk** | Brug ved ændringer > 500 tegn | Konsensus | Underskrift: `~~~~` | `Talk:Python` |
| **Redirects** | `#REDIRECT [[Mål]]` | Gamle navne | Opret efter flytning | `#REDIRECT [[Python]]` |
| **Maintenance** | Patrol `Special:RecentChanges` | Vandalisme | Watchlist | `Special:Watchlist` |

---

## **7. EKSEMPEL: FULDT STRUKTURERET MINI-WIKI**

```
Main Page
 ├── Portal:Naturvidenskab
 │    ├── Fysik
 │    └── Astronomi
 │         └── Planeter
 ├── Help:Redigering
 ├── Project:Retningslinjer
 └── User:Alice/Sandbox

Category:Indhold
 └── Category:Naturvidenskab
      └── Category:Astronomi
           └── Category:Planeter

Template:Infobox planet
Template:Navbar
Template:Stub
Template:Tip
```

---

## **8. PRO-TIPS FRA WIKIPEDIA & STORE WIKIER**

1. **Brug Extension:CategoryTree** → interaktivt træ  
2. **Semantic MediaWiki** → søg med SPARQL  
3. **VisualEditor + TemplateData** → nem infobox-redigering  
4. **Null edit** efter template-ændring → tving cache-opdatering  
5. **Backup** med `Special:Export` → XML → gem i Git  
6. **Brug `{{PAGENAME}}` i templates** for automatisk titel  
7. **Aktivér `$wgUseTidy = true;`** for ren HTML

---

## **RESSOURCER**

- [Manual:Namespaces](https://www.mediawiki.org/wiki/Manual:Namespaces)  
- [Help:Categories](https://www.mediawiki.org/wiki/Help:Categories)  
- [Help:Templates](https://www.mediawiki.org/wiki/Help:Templates)  
- [Extension:CategoryTree](https://www.mediawiki.org/wiki/Extension:CategoryTree)

---

**DU HAR NU ALT – FRA DATABASE TIL BRUGERGRÆNSEFLADE – FOR AT BYGGE EN PERFEKT MEDIAWIKI.**

**Start nu. Opret din første `Template:Navbar`. Se magien ske.**

**Held og lykke – din wiki bliver legendarisk!**
