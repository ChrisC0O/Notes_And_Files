# **Guide to Organizing Your MediaWiki Site**  
*Why You Do It, How It Works, Real Examples, and Step-by-Step Best Practices*

---

## Introduction: Why Organization Matters

Imagine your wiki as a **city**.  
Without streets (namespaces), traffic lights (templates), or maps (categories), users get lost.  
Good organization = **findability**, **scalability**, **maintainability**, and **collaboration**.

> **Goal**: Anyone should find content in < 3 clicks.  
> **Result**: More edits, fewer duplicates, happier users.

Let’s build that city — **brick by brick**, with **reasons**, **examples**, and **exact steps**.

---

## 1. **Namespaces: The City Districts**

### What Are Namespaces?

Namespaces are **pre-defined zones** for different types of content.  
Think of them as **neighborhoods**:
- **Downtown** = Main content (articles)
- **City Hall** = Project: (policies, portals)
- **Library** = Help: (guides)
- **Warehouse** = File: (images, PDFs)

Each namespace has:
- A **name** (e.g., `Help`)
- An **ID** (e.g., 12)
- A **talk page** (e.g., Help talk:13)

---

### Full Namespace Table (With Real-World Use)

| ID | Namespace | Talk | Purpose & **Why Use It** | Example |
|----|-----------|------|---------------------------|--------|
| 0 | **(Main)** | 1 | **Core articles** — only real content | `Solar System`, `Python Programming` |
| 2 | **User** | 3 | **Personal space** — drafts, sandbox, user CSS | `User:Alice/Sandbox` |
| 4 | **Project** | 5 | **Wiki governance** — rules, portals, about | `WikiRules`, `Portal:Science` |
| 6 | **File** | 7 | **Media metadata** — license, source, description | `File:Earth.jpg` |
| 8 | **MediaWiki** | 9 | **System interface** — buttons, messages | `MediaWiki:Sidebar` |
| 10 | **Template** | 11 | **Reusable blocks** — infoboxes, warnings | `Template:Infobox planet` |
| 12 | **Help** | 13 | **User guides** — how to edit, format | `Help:Editing` |
| 14 | **Category** | 15 | **Dynamic indexes** — auto-lists | `Category:Planets` |

---

### How to Use Namespaces (Step-by-Step)

#### **Step 1: Create a Page in a Namespace**
1. Go to URL: `https://yourwiki.com/wiki/Help:How_to_Edit`
2. Click **"Create"** → edit → save.

> **Why?** Keeps help separate from articles. No clutter.

#### **Step 2: Link to Namespaces**
```wiki
[[Help:Editing]] → Help:Editing  
[[User:Bob]] → User:Bob  
[[Template:Stub]] → {{Stub}} (auto-resolves)
```

> **Pro Tip**: Use `{{ns:help}}` → outputs "Help"

#### **Step 3: Search by Namespace**
Use **Special:Search** → Advanced → tick "Help" only.

---

### **Custom Namespaces (When You Need Them)**

You have 100+ pages on **Recipes**? Create `Recipe:` namespace.

**How (in LocalSettings.php):**
```php
$wgExtraNamespaces[100] = "Recipe";
$wgExtraNamespaces[101] = "Recipe_talk";
```

Now create: `Recipe:Chocolate Cake`

> **Why?** Prevents `Chocolate Cake` from clashing with `Chocolate Cake (band)`  
> **When?** Only after 50+ pages of same type.

---

## 2. **Categories: The City Map (Auto-Updating!)**

### What Are Categories?

**Dynamic lists** of pages that share a trait.

```wiki
[[Category:Planets]]
```
→ Adds page to `Category:Planets` **automatically**.

---

### How Categories Work (Behind the Scenes)

1. You add `[[Category:X]]` → page joins list.
2. `Category:X` page shows **all members**.
3. Subcategories: `[[Category:Planets]]` on `Category:Gas Giants`

```
Category:Contents
 └── Category:Science
      ├── Category:Physics
      └── Category:Astronomy
           └── Category:Planets
                ├── Mars
                └── Jupiter
```

---

### **Step-by-Step: Build a Category Tree**

#### **1. Create Root Category**
```wiki
[[Category:Contents]]
```
Page: `Category:Contents` → your **wiki map**

#### **2. Add Subcategories**
On `Category:Science`:
```wiki
[[Category:Contents]]
```

#### **3. Categorize Articles**
On `Mars` page:
```wiki
[[Category:Planets]]
[[Category:Terrestrial planets]]
```

#### **4. Sort Correctly**
```wiki
{{DEFAULTSORT:Mars}}
[[Category:Planets]]
```
→ Sorts by "Mars", not "mars"

---

### **Real Example: Wikipedia-Style Category Tree**

```
Category:Root
 └── Category:Technology
      ├── Category:Programming
      │    ├── Python
      │    └── JavaScript
      └── Category:Hardware
           └── CPU
```

---

### **Best Practices (With Reasons)**

| Rule | Why | How |
|------|-----|-----|
| **1 category tree only** | Avoids confusion | All top-level → `Category:Contents` |
| **Max 5–7 cats per page** | Too many = noise | Prioritize most specific |
| **Use sort keys** | Alphabetical chaos | `[[Category:People|Einstein, Albert]]` |
| **Hide maintenance cats** | Clean UI | Add `__HIDDENCAT__` to `Category:Stub` |
| **No redirect categories** | Breaks links | Use `{{Category redirect}}` template |

---

## 3. **Templates: The Reusable LEGO Bricks**

### What Are Templates?

**Snippets** you insert with `{{Name}}`.

---

### **Example: Infobox Template**

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
| diameter = 6,779 km
| moons = 2
}}
[[Category:Infobox templates]]
</noinclude>
```

#### **Use on Mars page:**
```wiki
{{Infobox planet
| name = Mars
| diameter = 6,779 km
| moons = 2
}}
```

→ Renders clean box. Update template → **all planets update**.

---

### **Template Tags Explained**

| Tag | Where It Shows | Use Case |
|-----|----------------|---------|
| `<includeonly>` | Only when transcluded | Main content |
| `<noinclude>` | Only on template page | Docs, categories |
| `<onlyinclude>` | Only transcluded part | Partial reuse |

---

### **Navbar Template (Navigation Bar)**

#### `Template:Navbar`
```wiki
<includeonly><div class="navbar">
[[:Category:Physics|Physics]] | [[:Category:Biology|Biology]] | [[Help:Editing|Help]]
</div></includeonly>

<noinclude>
Add to top of pages: {{Navbar}}
</noinclude>
```

→ One change = site-wide nav update.

---

## 4. **Page Structure & Navigation**

### **Main Page Layout (Example)**

```wiki
{{Portal box}}
== Welcome to MyWiki ==
Search or browse below.

{{Search box}}

== Featured Topics ==
{{Portal list}}

== New Here? ==
[[Help:Editing]] | [[Project:Community portal]]
```

---

### **Breadcrumbs (Navigation Trail)**

#### `Template:Breadcrumb`
```wiki
<includeonly><small>
[[Main Page]] > {{#if:{{{1|}}}|[[{{{1}}}]] > }}{{{2|}}}
</small></includeonly>
```

Use:
```wiki
{{Breadcrumb|Science|Physics}}
```
→ `Main Page > Science > Physics`

---

### **Subpages: Hierarchical Content**

Enable in `LocalSettings.php`:
```php
$wgNamespacesWithSubpages[NS_MAIN] = true;
```

Now:
- `Python/Functions`
- `Python/Classes`

> **Why?** Logical grouping  
> **When not?** Use categories for cross-links

---

## 5. **Files & Media**

### Upload & Embed

1. Go to **Special:Upload**
2. File: `File:Earth from space.jpg`
3. Description page:
   ```wiki
   == Summary ==
   Earth from Apollo 17.

   == Licensing ==
   {{PD-USGov-NASA}}
   ```

Embed:
```wiki
[[File:Earth from space.jpg|thumb|right|Earth from space]]
```

---

## 6. **Full Best Practices Checklist**

| Area | Do This | Why |
|------|--------|-----|
| **Content** | Draft in `User:You/Draft` → move to Main | Prevents broken links |
| **Naming** | `Help:How to edit` (not `howtoedit`) | Searchable, consistent |
| **Templates** | Document with `/doc` subpage | Future-proof |
| **Categories** | One root: `Category:Contents` | Single source of truth |
| **Talk Pages** | Use for all major changes | Transparency |
| **Redirects** | `#REDIRECT [[Target]]` | Handles old names |
| **Maintenance** | Patrol Special:RecentChanges | Catch vandalism fast |

---

## 7. **Example Wiki Structure (Small Wiki)**

```
Main Page
 ├── Portal:Science
 │    ├── Physics
 │    └── Biology
 ├── Help:Editing
 ├── Project:Rules
 └── User:Alice/Sandbox

Category:Contents
 └── Category:Science
      └── Category:Physics

Template:Infobox
Template:Stub
Template:Navbar
```

---

## 8. **Pro Tips from Real Wikis**

1. **Copy Wikipedia templates** via **Special:Export**
2. **Use VisualEditor** for new users
3. **Enable DiscussionTools** for better talk pages
4. **Add a Search box** on every page
5. **Back up monthly** with `Special:Export` (XML)

---

## Resources

- [MediaWiki.org](https://www.mediawiki.org)
- [Manual:Namespaces](https://www.mediawiki.org/wiki/Manual:Namespaces)
- [Help:Categories](https://www.mediawiki.org/wiki/Help:Categories)
- [Template Documentation](https://www.mediawiki.org/wiki/Help:Templates)

---

**You now have a blueprint to build a clean, scalable, user-friendly wiki.**  
Start small. Add one template. One category tree. Watch it grow.

**Happy organizing!**
