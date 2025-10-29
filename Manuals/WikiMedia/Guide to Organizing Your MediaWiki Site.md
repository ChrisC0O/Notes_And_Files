# Comprehensive Guide to Organizing Your MediaWiki Site

MediaWiki, the open-source software behind Wikipedia and thousands of other wikis, provides powerful tools like **namespaces**, **categories**, **templates**, **subpages**, and **navigation structures** to keep your site structured, scalable, and user-friendly. Proper organization ensures content is easy to find, maintain, and expand—whether you're running a personal wiki, documentation site, or collaborative knowledge base. This guide covers the fundamentals, best practices, and pro tips.

## 1. Namespaces: The Foundation of Organization

**Namespaces** group pages by purpose, prefixed in titles (e.g., `Help:Guide`). They prevent clutter in the main content area and enable special behaviors like transclusion (for templates) or dynamic lists (for categories). Every wiki has **16 default subject namespaces** (even IDs) paired with **talk namespaces** (odd IDs) for discussions, plus 2 special ones (-2 Media, -1 Special).

### Default Namespaces Table

| ID | Namespace | Talk ID | Purpose |
|----|-----------|---------|---------|
| -2 | **Media** | N/A | Direct links to files (bypasses description page). |
| -1 | **Special** | N/A | Dynamic pages (e.g., search, recent changes)—not editable. |
| 0 | **(Main)** | 1 | Core content pages—no prefix. |
| **1** | **Talk** | N/A | Discussions for main pages. |
| **2** | **User** | **3** | User profiles, drafts, personal JS/CSS (subpages restricted). |
| **3** | **User talk** | N/A | Messages to users (auto-notifications). |
| **4** | **Project**<br>(e.g., WikiName:) | **5** | Wiki guidelines, policies, portals. |
| **5** | **Project talk** | N/A | Discussions on project pages. |
| **6** | **File**<br>(alias: Image) | **7** | Media metadata, licensing. |
| **7** | **File talk** | N/A | File discussions. |
| **8** | **MediaWiki** | **9** | System messages, site-wide CSS/JS (requires special rights). |
| **9** | **MediaWiki talk** | N/A | System message discussions. |
| **10** | **Template** | **11** | Reusable content blocks. |
| **11** | **Template talk** | N/A | Template discussions. |
| **12** | **Help** | **13** | User guides and tutorials. |
| **13** | **Help talk** | N/A | Help discussions. |
| **14** | **Category** | **15** | Dynamic page indexes. |
| **15** | **Category talk** | N/A | Category discussions. |

**How to Use:**
- **Create pages**: Visit `Namespace:PageName` and edit (e.g., `User:YourName/Draft`).
- **Link**: `[[Namespace:Page]]` or shortcuts like `{{ns:User}}` magic word.
- **Transclude templates**: `{{TemplateName}}` (defaults to Template:).
- **Best practices**:
  | Do | Don't |
  |----|-------|
  | Use Main for articles. | Mix content types (e.g., no templates in Main). |
  | Draft in User:. | Create pages in Special/Media. |
  | Policies in Project:. | Overuse custom namespaces initially. |
  | Help for guides. | Ignore talk pages—use for feedback! |

**Custom Namespaces**: Admins can add via config (IDs 100+). Great for projects like `Book:`, `Module:`. 

## 2. Categories: Dynamic Grouping and Navigation

**Categories** create automatic, hierarchical indexes. Add `[[Category:Foo]]` at a page's bottom to join it.

- **How it works**: Pages list alphabetically on `Category:Foo`; subcategories form trees.
- **Hierarchy**: Add categories to category pages (e.g., `Category:Animals` → `[[Category:Biology]]`).
- **Sort keys**: `[[Category:Foo\|Bar]]` sorts under "Bar".
- **Magic tags**:
  | Tag | Effect |
  |-----|--------|
  | `__HIDDENCAT__` | Hides from page bottom (e.g., maintenance cats). |
  | `{{DEFAULTSORT:Key}}` | Sets default sort for all cats on page. |

**Best Practices**:
- **One top-level tree** (e.g., `Category:Contents`).
- **Search before creating** (Special:Categories).
- **5-10 cats per page** max.
- **Templates**: Use `<includeonly>[[Category:Foo]]</includeonly>` to cat *using* pages only.
- **Maintenance**: No cat redirects—use templates. Null-edit after template changes.
- **View trees**: `<categorytree>` tag or Special:CategoryTree.

## 3. Templates: Reuse and Standardize

**Templates** (in Template:) are transcluded blocks for consistency (e.g., infoboxes, navbars).

- **Create**: Edit `Template:Infobox`.
- **Use**:
  | Syntax | Effect |
  |--------|--------|
  | `{{Infobox}}` | Dynamic transclude (updates everywhere). |
  | `{{subst:Infobox}}` | Static copy. |
  | `{{Infobox\|param=Value}}` | Parameters ({{{param\|default}}}). |

**Best Practices**:
- **Documentation**: Subpage `/doc` with `{{Documentation}}`.
- **Tags**:
  | Tag | Where Visible |
  |-----|---------------|
  | `<noinclude>` | Template page only. |
  | `<includeonly>` | Transcluded pages only. |
  | `<onlyinclude>` | Transcluded content only. |
- **Avoid loops/recursion**.
- **Copy from Wikipedia** via Special:Export.
- **Navigation**: `{{Navbar}}` for menus.

## 4. Page Structure and Navigation

- **Subpages**: `Page/Subpage` for hierarchy (e.g., `Project:Guide/Advanced`).
- **Main Page**: Portals, featured content, search box.
- **Redirects**: `#REDIRECT [[Target]]` for aliases.
- **Disambiguation**: `{{Disambig}}` for similar titles.
- **Media**: Upload to File:; embed `[[File:Img.jpg\|thumb]]`.
- **Links**: Internal `[[Page]]`, interwiki `[[wikipedia:Foo]]`.

## 5. Top Best Practices for Your Wiki

| Category | Practices |
|----------|-----------|
| **Content** | - Bold edits; fix mistakes easily.<br>- Draft in User:, publish to Main.<br>- Categories > subpages for cross-linking.<br>- Templates for infoboxes/nav/stubs. |
| **Community** | - Talk pages for all changes.<br>- Watchlists for monitoring.<br>- Assume good faith; praise contributors. |
| **Navigation** | - Breadcrumb templates.<br>- Search-optimized titles.<br>- Portals in Project:. |
| **Maintenance** | - Recent changes patrol.<br>- Hidden cats for errors.<br>- Back up via XML export. |
| **Growth** | - Start small: Main Page + Help.<br>- Train with editathons.<br>- Extensions: Semantic MediaWiki for queries. |

**Pro Tip**: **Wiki Way**—centralize, collaborate, iterate. Use VisualEditor for noobs.

For more: [mediawiki.org](https://www.mediawiki.org). Happy wikifying! 🚀
