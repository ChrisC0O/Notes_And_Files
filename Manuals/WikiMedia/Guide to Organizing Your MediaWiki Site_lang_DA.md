# **Ultimativ dybdegående guide til at organisere din MediaWiki-site**  
*Hvorfor du gør det, hvordan det virker, konkrete eksempler og trin-for-trin-best practices*

---

## Indledning: Hvorfor organisering er vigtigt

Forestil dig din wiki som en **by**.  
Uden gader (namespaces), trafiklys (templates) eller kort (categories) bliver brugerne fortabte.  
God organisering = **findbarhed**, **skalerbarhed**, **vedligeholdelse** og **samarbejde**.

> **Mål**: Alle skal kunne finde indhold på under 3 klik.  
> **Resultat**: Flere redigeringer, færre dubletter, gladere brugere.

Lad os bygge den by — **mursten for mursten**, med **begrundelser**, **eksempler** og **præcise trin**.

---

## 1. **Namespaces: Byens distrikter**

### Hvad er namespaces?

Namespaces er **foruddefinerede zoner** til forskellige typer indhold.  
Tænk på dem som **bydele**:
- **Centrum** = Main content (artikler)
- **Rådhus** = Project: (regler, portaler)
- **Bibliotek** = Help: (vejledninger)
- **Lager** = File: (billeder, PDF’er)

Hvert namespace har:
- Et **navn** (f.eks. `Help`)
- Et **ID** (f.eks. 12)
- En **talk page** (f.eks. Help talk:13)

---

### Fuldt namespace-oversigt (med virkelige anvendelser)

| ID | Namespace | Talk | Formål & **hvorfor bruge det** | Eksempel |
|----|-----------|------|--------------------------------|----------|
| 0 | **(Main)** | 1 | **Kerneartikler** — kun rigtigt indhold | `Solsystemet`, `Python Programming` |
| 2 | **User** | 3 | **Personligt rum** — drafts, sandbox, user CSS | `User:Alice/Sandbox` |
| 4 | **Project** | 5 | **Wiki-styring** — regler, portaler, about | `WikiRules`, `Portal:Naturvidenskab` |
| 6 | **File** | 7 | **Mediemetadata** — license, source, description | `File:Jorden.jpg` |
| 8 | **MediaWiki** | 9 | **System interface** — buttons, messages | `MediaWiki:Sidebar` |
| 10 | **Template** | 11 | **Reusable blocks** — infoboxes, warnings | `Template:Infobox planet` |
| 12 | **Help** | 13 | **Brugervejledninger** — how to edit, format | `Help:Redigering` |
| 14 | **Category** | 15 | **Dynamic indexes** — auto-lists | `Category:Planeter` |

---

### Sådan bruger du namespaces (trin for trin)

#### **Trin 1: Opret en side i et namespace**
1. Gå til URL: `https://dinwiki.dk/wiki/Help:Hvordan_man_redigerer`
2. Klik **"Create"** → edit → save.

> **Hvorfor?** Holder help adskilt fra artikler. Ingen rod.

#### **Trin 2: Link til namespaces**
```wiki
[[Help:Redigering]] → Help:Redigering  
[[User:Bob]] → User:Bob  
[[Template:Stub]] → {{Stub}} (løser automatisk)
```

> **Pro-tip**: Brug `{{ns:help}}` → udskriver "Help"

#### **Trin 3: Søg efter namespace**
Brug **Special:Search** → Advanced → tick "Help" only.

---

### **Custom namespaces (når du har brug for dem)**

Har du 100+ sider om **Opskrifter**? Opret `Opskrift:` namespace.

**Hvordan (i LocalSettings.php):**
```php
$wgExtraNamespaces[100] = "Opskrift";
$wgExtraNamespaces[101] = "Opskrift_talk";
```

Nu opret: `Opskrift:Chokoladekage`

> **Hvorfor?** Forhindrer `Chokoladekage` i at kollidere med `Chokoladekage (band)`  
> **Hvornår?** Først efter 50+ sider af samme type.

---

## 2. **Categories: Byens kort (selvopdaterende!)**

### Hvad er categories?

**Dynamiske lister** over sider, der deler et træk.

```wiki
[[Category:Planeter]]
```
→ Tilføjer siden til `Category:Planeter` **automatisk**.

---

### Sådan fungerer categories (bag kulisserne)

1. Du tilføjer `[[Category:X]]` → siden tilslutter sig listen.
2. `Category:X`-siden viser **alle medlemmer**.
3. Subcategories: `[[Category:Planeter]]` på `Category:Gasgiganter`

```
Category:Indhold
 └── Category:Naturvidenskab
      ├── Category:Fysik
      └── Category:Astronomi
           └── Category:Planeter
                ├── Mars
                └── Jupiter
```

---

### **Trin-for-trin: Byg et category tree**

#### **1. Opret root category**
```wiki
[[Category:Indhold]]
```
Side: `Category:Indhold` → dit **wiki-kort**

#### **2. Tilføj subcategories**
På `Category:Naturvidenskab`:
```wiki
[[Category:Indhold]]
```

#### **3. Kategorisér artikler**
På `Mars`-siden:
```wiki
[[Category:Planeter]]
[[Category:Jordlignende planeter]]
```

#### **4. Sortér korrekt**
```wiki
{{DEFAULTSORT:Mars}}
[[Category:Planeter]]
```
→ Sorterer under "Mars", ikke "mars"

---

### **Konkret eksempel: Wikipedia-stil category tree**

```
Category:Root
 └── Category:Teknologi
      ├── Category:Programmering
      │    ├── Python
      │    └── JavaScript
      └── Category:Hardware
           └── CPU
```

---

### **Best practices (med begrundelser)**

| Regel | Hvorfor | Hvordan |
|-------|---------|---------|
| **Kun ét category tree** | Undgår forvirring | Alle topniveauer → `Category:Indhold` |
| **Max 5–7 cat. pr. side** | For mange = støj | Prioritér mest specifikke |
| **Brug sort keys** | Alfabetisk kaos | `[[Category:Personer|Einstein, Albert]]` |
| **Skjul maintenance cats** | Ren UI | Tilføj `__HIDDENCAT__` til `Category:Stub` |
| **Ingen redirect categories** | Bryder links | Brug `{{Category redirect}}` template |

---

## 3. **Templates: De genanvendelige LEGO-klodser**

### Hvad er templates?

**Snippets** du indsætter med `{{Navn}}`.

---

### **Eksempel: Infobox template**

#### **Template:Infobox planet** (`Template:Infobox planet`)
```wiki
<includeonly>{| class="infobox" style="width:22em;"
! colspan="2" | {{{name}}}
|-
| '''Diameter''' || {{{diameter|Unknown}}}
|-
| '''Moons''' || {{{moons|0}}}
|}</includeonly>

<noinclude>
== Usage ==
{{Infobox planet
| name = Mars
| diameter = 6.779 km
| moons = 2
}}
[[Category:Infobox templates]]
</noinclude>
```

#### **Brug på Mars-siden:**
```wiki
{{Infobox planet
| name = Mars
| diameter = 6.779 km
| moons = 2
}}
```

→ Giver en pæn boks. Opdater template → **alle planeter opdateres**.

---

### **Template tags forklaret**

| Tag | Hvor vises det | Anvendelse |
|-----|----------------|------------|
| `<includeonly>` | Kun ved transclusion | Main content |
| `<noinclude>` | Kun på template page | Docs, categories |
| `<onlyinclude>` | Kun den del, der transcludes | Partial reuse |

---

### **Navbar template (navigationsbjælke)**

#### `Template:Navbar`
```wiki
<includeonly><div class="navbar">
[[:Category:Fysik|Fysik]] | [[:Category:Biologi|Biologi]] | [[Help:Redigering|Hjælp]]
</div></includeonly>

<noinclude>
Tilføj øverst på sider: {{Navbar}}
</noinclude>
```

→ Én ændring = hele sitet opdateret.

---

## 4. **Page structure & navigation**

### **Main Page layout (eksempel)**

```wiki
{{Portal box}}
== Velkommen til MinWiki ==
Søg eller gennemse nedenfor.

{{Search box}}

== Fremhævede emner ==
{{Portal list}}

== Ny her? ==
[[Help:Redigering]] | [[Project:Fællesskabsportal]]
```

---

### **Breadcrumbs (navigationssti)**

#### `Template:Breadcrumb`
```wiki
<includeonly><small>
[[Main Page]] > {{#if:{{{1|}}}|[[{{{1}}}]] > }}{{{2|}}}
</small></includeonly>
```

Brug:
```wiki
{{Breadcrumb|Naturvidenskab|Fysik}}
```
→ `Main Page > Naturvidenskab > Fysik`

---

### **Subpages: Hierarkisk indhold**

Aktivér i `LocalSettings.php`:
```php
$wgNamespacesWithSubpages[NS_MAIN] = true;
```

Nu:
- `Python/Functions`
- `Python/Classes`

> **Hvorfor?** Logisk gruppering  
> **Hvornår ikke?** Brug categories til cross-links

---

## 5. **Files & media**

### Upload & embed

1. Gå til **Special:Upload**
2. File: `File:Jorden fra rummet.jpg`
3. Description page:
   ```wiki
   == Summary ==
   Jorden fra Apollo 17.

   == Licensing ==
   {{PD-USGov-NASA}}
   ```

Embed:
```wiki
[[File:Jorden fra rummet.jpg|thumb|right|Jorden fra rummet]]
```

---

## 6. **Fuld checklist for best practices**

| Område | Gør dette | Hvorfor |
|--------|-----------|---------|
| **Content** | Draft i `User:Dig/Draft` → move to Main | Forhindrer broken links |
| **Naming** | `Help:Hvordan man redigerer` (ikke `hvordanmanredigerer`) | Searchable, consistent |
| **Templates** | Dokumentér med `/doc` subpage | Future-proof |
| **Categories** | Én root: `Category:Indhold` | Én source of truth |
| **Talk pages** | Brug til alle større ændringer | Transparency |
| **Redirects** | `#REDIRECT [[Target]]` | Håndterer old names |
| **Maintenance** | Patrolér Special:RecentChanges | Fang vandalism fast |

---

## 7. **Eksempel på wiki structure (lille wiki)**

```
Main Page
 ├── Portal:Naturvidenskab
 │    ├── Fysik
 │    └── Biologi
 ├── Help:Redigering
 ├── Project:Regler
 └── User:Alice/Sandbox

Category:Indhold
 └── Category:Naturvidenskab
      └── Category:Fysik

Template:Infobox
Template:Stub
Template:Navbar
```

---

## 8. **Pro-tips fra rigtige wikier**

1. **Kopiér Wikipedia templates** via **Special:Export**
2. **Brug VisualEditor** til nybegyndere
3. **Aktivér DiscussionTools** for bedre talk pages
4. **Tilføj en search box** på hver side
5. **Backup månedligt** med `Special:Export` (XML)

---

## Ressourcer

- [MediaWiki.org](https://www.mediawiki.org)
- [Manual:Namespaces](https://www.mediawiki.org/wiki/Manual:Namespaces)
- [Help:Categories](https://www.mediawiki.org/wiki/Help:Categories)
- [Template Documentation](https://www.mediawiki.org/wiki/Help:Templates)

---

**Du har nu en blueprint til at bygge en ren, skalerbar, brugervenlig wiki.**  
Start småt. Tilføj én template. Ét category tree. Se det vokse.

**God organisering!**
