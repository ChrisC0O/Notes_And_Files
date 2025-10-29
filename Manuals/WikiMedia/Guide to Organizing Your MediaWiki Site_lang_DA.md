# **ULTIMATIV, EKSTREMT DYBDEGÅENDE GUIDE TIL AT ORGANISERE DIN MEDIAWIKI**  
*Alt er på dansk, men alle tekniske MediaWiki-termer står på **original engelsk** (namespace, template, category osv.).  
Hver eneste detalje er forklaret: **hvorfor**, **hvordan**, **hvad sker bag kulisserne**, **trin-for-trin**, **eksempler**, **faldgruber**, **pro-tips**, **kodelinje-for-kodelinje**.*

---

## **Indledning: Hvorfor organisering er selve fundamentet for en sund wiki**

En MediaWiki uden struktur er som en by uden veje, skilte eller kort.  
Brugere finder ikke indhold. Redaktører opretter dubletter. Administratorer drukner i kaos.

> **Målet med god organisering**  
> 1. **Findbarhed**: Max 3 klik til ethvert indhold.  
> 2. **Skalerbarhed**: 10 eller 10.000 sider – systemet skal fungere ens.  
> 3. **Vedligeholdelse**: Én ændring → opdatering overalt (via templates).  
> 4. **Samarbejde**: Nye brugere forstår strukturen med det samme.

---

## **1. Namespaces – den arkitektoniske grundplan**

### **Hvad er et namespace præcist?**

Et **namespace** er en **logisk container** til sider med samme formål.  
Hver side i MediaWiki har en **fuld titel** = `Namespace:SideNavn` (undtagen Main, hvor præfikset udelades).

> **Teknisk set**:  
> - Hver namespace har et **unikt ID** (heltal).  
> - Hvert namespace (undtagen Special og Media) har en **talk namespace** med ID + 1.  
> - Systemet bruger disse ID’er til **søgning**, **rettigheder**, **subpages**, **transclusion** osv.

---

### **Komplet namespace-oversigt med detaljeret forklaring**

| ID | Namespace | Talk ID | **Formål** | **Hvorfor bruge det?** | **Eksempel** | **Rettigheder** |
|----|-----------|---------|------------|------------------------|--------------|-----------------|
| -2 | **Media** | – | Direkte link til fil (bypasser beskrivelsesside) | Hurtig adgang til rå fil | `[[Media:Logo.png]]` | Ingen redigering |
| -1 | **Special** | – | Dynamiske system-sider | Genereres on-the-fly | `Special:RecentChanges` | Kun system |
| 0 | **(Main)** | 1 | **Kerneindhold** – artikler, leksika | Hovedfokus for læsere | `Python`, `København` | Alle kan redigere |
| 1 | **Talk** | – | Diskussion om Main-sider | Samarbejde, forslag | `Talk:Python` | Alle |
| 2 | **User** | 3 | Personligt rum, drafts, sandbox, CSS/JS | Sikker testplads | `User:Alice/Sandbox` | Kun ejer + admins |
| 3 | **User talk** | – | Beskeder til brugere | Notifikationer | `User talk:Alice` | Alle |
| 4 | **Project** | 5 | Wikiens "meta" – regler, portaler, om | Central styring | `Project:Retningslinjer` | Alle |
| 5 | **Project talk** | – | Diskussion om Project-sider | Konsensus | `Project talk:Retningslinjer` | Alle |
| 6 | **File** | 7 | Metadata for uploadede filer | Licens, kilde, beskrivelse | `File:Earth.jpg` | Alle (med upload-rettighed) |
| 7 | **File talk** | – | Diskussion om filer | Klarhed om brug | `File talk:Earth.jpg` | Alle |
| 8 | **MediaWiki** | 9 | Systembeskeder, interface-tekster | Oversættelse, tilpasning | `MediaWiki:Sidebar` | Kun interface-admins |
| 9 | **MediaWiki talk** | – | Diskussion om systembeskeder | Koordinering | `MediaWiki talk:Sidebar` | Alle |
| 10 | **Template** | 11 | Genanvendelige kodesnipper | Konsistens | `Template:Infobox` | Alle |
| 11 | **Template talk** | – | Diskussion om templates | Forbedringer | `Template talk:Infobox` | Alle |
| 12 | **Help** | 13 | Brugervejledninger | Onboarding | `Help:Redigering` | Alle |
| 13 | **Help talk** | – | Feedback på vejledninger | Forbedring | `Help talk:Redigering` | Alle |
| 14 | **Category** | 15 | Dynamiske lister over sider | Navigation, søgning | `Category:Planeter` | Alle |
| 15 | **Category talk** | – | Diskussion om kategorier | Struktur | `Category talk:Planeter` | Alle |

---

### **Sådan opretter du en side i et namespace – trin for trin**

#### **Eksempel: Opret `Help:Redigering`**

1. **Gå til URL**:  
   ```
   https://dinwiki.dk/wiki/Help:Redigering
   ```
2. **Klik “Opret”** (hvis siden ikke findes).  
3. **Indsæt indhold**:
   ```wiki
   = Sådan redigerer du =
   Klik på '''Rediger''' øverst.

   Brug [[Help:Formatering|formatering]] for at gøre teksten pæn.

   Gem med en kort [[Help:Redigeringsresumé|redigeringsresumé]].
   ```
4. **Tilføj kategori**:
   ```wiki
   [[Category:Hjælpesider]]
   ```
5. **Gem**.

> **Hvorfor i Help-namespace?**  
> - Adskilt fra Main → ingen forvirring.  
> - Søgning i Help kun → `intitle:Redigering inhelp`  
> - Talk-sider aktiveres automatisk.

---

### **Hvordan linker du til namespaces?**

| Syntax | Resultat | Bemærkning |
|-------|----------|------------|
| `[[Help:Redigering]]` | Help:Redigering | Normalt link |
| `[[User:Alice]]` | User:Alice | Går til brugerprofil |
| `[[Template:Stub]]` | Template:Stub | Men vises som **Stub** i editor |
| `{{Stub}}` | (indhold af Template:Stub) | **Transclusion** |
| `{{FULLPAGENAME}}` | `Help:Redigering` | Magic word |
| `{{ns:help}}` | `Help` | Namespace-navn |

---

### **Custom namespaces – hvornår og hvordan**

#### **Hvornår skal du bruge custom namespaces?**

| Situation | Eksempel | Namespace |
|----------|----------|-----------|
| 100+ opskrifter | `Chokoladekage` | `Opskrift:` |
| Dokumentation | `API v2` | `Dokumentation:` |
| Bogprojekt | `Kap 1` | `Bog:` |

#### **Sådan opretter du et custom namespace (i `LocalSettings.php`)**

```php
// Opret Opskrift: (ID 100) og Opskrift talk: (ID 101)
$wgExtraNamespaces[100] = "Opskrift";
$wgExtraNamespaces[101] = "Opskrift_talk";

// Tillad subpages i Opskrift:
$wgNamespacesWithSubpages[100] = true;

// Søg kun i Opskrift:
$wgNamespacesToBeSearchedDefault[100] = true;
```

> **Genstart ikke serveren** – kun genindlæs siden.

#### **Opret første side**
```
https://dinwiki.dk/wiki/Opskrift:Chokoladekage
```

---

## **2. Categories – det selvopdaterende navigationssystem**

### **Hvad sker der, når du tilføjer `[[Category:Planeter]]`?**

1. **Parseren** ser `[[Category:Planeter]]`.  
2. **Tjekker om `Category:Planeter` findes** → opretter hvis ikke.  
3. **Tilføjer siden til databasen** i tabellen `categorylinks`.  
4. **Næste gang `Category:Planeter` vises** → SQL-forespørgsel henter alle sider.  
5. **Automatisk sortering** efter `page_title` (medmindre sort key bruges).

---

### **Byg et fuldt category tree – trin for trin**

#### **Trin 1: Opret rod-kategorien**

```wiki
[[Category:Indhold]]
```

> **Side: `Category:Indhold`**  
> Indhold:
> ```wiki
> Dette er wikiens hovedkategori. Alle andre kategorier skal være under denne.
> ```

#### **Trin 2: Opret hovedkategorier**

På `Category:Naturvidenskab`:
```wiki
[[Category:Indhold]]
```

#### **Trin 3: Opret underkategorier**

På `Category:Astronomi`:
```wiki
[[Category:Naturvidenskab]]
```

#### **Trin 4: Kategorisér en artikel**

På `Mars`:
```wiki
{{DEFAULTSORT:Mars}}
[[Category:Planeter]]
[[Category:Jordlignende planeter]]
[[Category:Solsystemet]]
```

> **Hvorfor `DEFAULTSORT`?**  
> Uden → sorteres under "M" for "Mars".  
> Med → under "Mars" (ignoreres "Den røde planet" osv.).

---

### **Avancerede category-teknikker**

| Teknik | Kode | Effekt |
|-------|------|--------|
| **Sort key** | `[[Category:Personer|Einstein, Albert]]` | Sorteres under "Einstein, Albert" |
| **Hidden category** | `__HIDDENCAT__` på `Category:Stub` | Skjules i bunden af sider |
| **Category redirect** | `{{Category redirect|Kategori:Gamle planeter}}` | Omdirigerer kategori |
| **Category tree** | `<categorytree mode=pages>Planeter</categorytree>` | Vis træ i artikel |

---

## **3. Templates – den magiske genbrugs-maskine**

### **Hvad sker ved `{{Infobox}}`?**

1. Parser finder `{{Infobox}}`.  
2. Søger i **Template namespace**.  
3. Finder `Template:Infobox`.  
4. **Transcluderer** indholdet.  
5. Erstatter `{{{parameter}}}` med værdier.  
6. **Cachelagrer** resultatet (indtil template ændres).

---

### **Eksempel: Fuld infobox med dokumentation**

#### **`Template:Infobox planet`**
```wiki
<includeonly>{| class="infobox" style="float:right; width:22em; font-size:90%;"
|-
! colspan="2" style="font-size:120%; text-align:center;" | {{{name|{{PAGENAME}}}}}
{{#if: {{{image|}}} | {{!}}-
{{!}} colspan="2" style="text-align:center;" {{!}} [[File:{{{image}}}|220px]]
}}
|-
{{#if: {{{diameter|}}} | {{!}} '''Diameter''' {{!!}} {{{diameter}}} }}
|-
{{#if: {{{moons|}}} | {{!}} '''Måner''' {{!!}} {{{moons}}} }}
|-
| colspan="2" style="text-align:center; font-size:85%;" | ''Sidst opdateret: {{REVISIONMONTH}}/{{REVISIONYEAR}}''
|}</includeonly>

<noinclude>{{Infobox planet/doc}}</noinclude>
```

#### **`Template:Infobox planet/doc` (subpage)**
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
* '''name''' – planetens navn
* '''image''' – billede (uden File:)
* '''diameter''' – i km
* '''moons''' – antal

[[Category:Infobox templates]]
</noinclude>
```

> **Fordele ved `/doc` subpage**:  
> - Dokumentation vises kun på template-siden.  
> - Brug `{{Documentation}}` for automatisk boks.

---

### **Template tags – detaljeret**

| Tag | Hvor vises | Eksempel | Brug |
|-----|------------|---------|------|
| `<includeonly>` | Kun ved transclusion | Kode | Undgå at vise på template-siden |
| `<noinclude>` | Kun på template-siden | Docs | Dokumentation, kategorier |
| `<onlyinclude>` | Kun transcluderet del | Delvis | Brug i store templates |

---

## **4. Navigation & sidestruktur**

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
```

---

### **Breadcrumbs med logik**

```wiki
{{#switch: {{NAMESPACE}}
  | Main = 
  | Help = {{Breadcrumb|Hjælp|{{PAGENAME}}}}
  | #default = {{Breadcrumb|{{NAMESPACE}}|{{PAGENAME}}}}
}}
```

---

## **5. Files – korrekt upload og brug**

### **Upload-trin**

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

## **6. Fuld checklist – fra nybegynder til ekspert**

| Område | Regel | Hvorfor | Hvordan |
|--------|------|---------|---------|
| **Content** | Draft i `User:` → flyt til Main | Undgå ødelagte links | `Move` funktion |
| **Naming** | `Help:Hvordan man redigerer` | Søgbar | Undgå specialtegn |
| **Templates** | Altid `/doc` | Klarhed | `{{Documentation}}` |
| **Categories** | Én rod: `Category:Indhold` | Enhed | Subcategories |
| **Talk** | Brug ved ændringer > 500 tegn | Konsensus | Underskrift: `~~~~` |
| **Redirects** | `#REDIRECT [[Mål]]` | Gamle navne | Opret efter flytning |
| **Maintenance** | Patrol `Special:RecentChanges` | Vandalisme | Watchlist |

---

## **7. Eksempel: Fuldt struktureret mini-wiki**

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
```

---

## **8. Pro-tips fra Wikipedia & store wikier**

1. **Brug Extension:CategoryTree** → interaktivt træ.  
2. **Semantic MediaWiki** → søg med SPARQL.  
3. **VisualEditor + TemplateData** → nem infobox-redigering.  
4. **Null edit** efter template-ændring → tving cache-opdatering.  
5. **Backup** med `Special:Export` → XML → gem i Git.

---

## **Ressourcer**

- [Manual:Namespaces](https://www.mediawiki.org/wiki/Manual:Namespaces)  
- [Help:Categories](https://www.mediawiki.org/wiki/Help:Categories)  
- [Help:Templates](https://www.mediawiki.org/wiki/Help:Templates)  
- [Extension:CategoryTree](https://www.mediawiki.org/wiki/Extension:CategoryTree)

---

**Du har nu alt, hvad du skal bruge for at bygge en professionel, skalerbar, brugervenlig MediaWiki – fra første side til 100.000.**

**Start nu. Opret din første `Template:Navbar`. Se magien ske.**

**Held og lykke med din wiki!**
