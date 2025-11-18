| # | Dork / Search Command                                    | What it finds / Why it’s dangerous                                                                                  | Where it works best |
| --- |-----------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|---------------------|
| 1   | `"Firstname Lastname"`                                    | Exact full name matches (quotes force exact phrase)                                                                 | Google & DDG        |
| 2   | `"Firstname Lastname" "City"`                             | Your name + city – narrows down to your real location                                                               | Google & DDG        |
| 3   | `"Firstname Lastname" "Company Name"`                     | Links your name directly to your employer                                                                                   | Google & DDG        |
| 4   | `your.email@company.com`                                  | Any page containing your exact email address                                                                        | Google & DDG        |
| 5   | `intext:"your.email@company.com"`                         | Forces the email to appear in the page text (catches leaked docs, pastes, forums)                                   | Google & DDG        |
| 6   | `"@yourcompany.com"`                                      | Every email address on your company domain that Google has indexed                                                 | Google & DDG        |
| 7   | `"@yourcompany.com" -site:yourcompany.com`                | Your company emails leaked on third-party sites (huge red flag)                                                     | Google only         |
| 8   | `intext:"+1-xxx-xxx-xxxx"` OR `intext:"(xxx) xxx-xxxx"`   | Phone numbers in US format                                                                                                  | Google & DDG        |
| 9   | `site:pastebin.com intext:"@yourcompany.com"`             | Pastebin dumps containing any company email                                                                         | Google & DDG        |
| 10  | `site:pastebin.com "Firstname Lastname"`                  | Your name leaked on Pastebin                                                                                                | Google & DDG        |
| 11  | `intext:"password" "Firstname Lastname"`                  | Pages containing both your name and the word “password” (very often credential leaks)                               | Google & DDG        |
| 12  | `filetype:pdf "your company" "confidential"`              | Confidential PDFs that accidentally got indexed                                                                     | Google & DDG        |
| 13  | `filetype:xlsx OR filetype:csv "@yourcompany.com"`        | Excel/CSV exports with employee email lists                                                                                 | Google & DDG        |
| 14  | `filetype:sql "INSERT INTO" "@yourcompany.com"`           | Full database dumps (.sql files) containing your emails                                                             | Google & DDG        |
| 15  | `filetype:env "DB_PASSWORD" OR "API_KEY"`                 | Exposed .env files with secrets (common dev mistake)                                                                | Google & DDG        |
| 16  | `intext:"yourcompany.com" extension:env`                  | Same as above but specifically for your domain                                                                     | Google only         |
| 17  | `org:YourGitHubOrg password OR api_key OR token`          | Hardcoded secrets inside your company’s public GitHub repositories                                                 | Google & DDG        |
| 18  | `username:YourGitHubUsername password`                    | Secrets in your personal public repos                                                                                       | Google & DDG        |
| 19  | `site:github.com "your.email@company.com"`                | Any code or issue comment containing your email                                                                     | Google & DDG        |
| 20  | `site:truepeoplesearch.com "Firstname Lastname" "City"`   | US people-search site that often has current address + relatives                                                    | Google & DDG        |
| 21  | `site:fastpeoplesearch.com "Firstname Lastname"`          | Same as above – another major data-broker site                                                                      | Google & DDG        |
| 22  | `site:spokeo.com "Firstname Lastname"`                    | Paid people-search site (free results sometimes indexed)                                                            | Google & DDG        |
| 23  | `site:beenverified.com "Firstname Lastname"`              | Another data-broker site                                                                                                    | Google & DDG        |
| 24  | `site:linkedin.com/in "Firstname Lastname" "Company"`     | Your LinkedIn profile (attackers use it for spear-phishing)                                                         | Google & DDG        |
| 25  | `site:facebook.com "Firstname Lastname" "lives in"`       | Facebook profiles that mention city or employer                                                                     | Google & DDG        |
| 26  | `inurl:admin intext:"@yourcompany.com"`                   | Exposed admin logins or backup files containing emails                                                              | Google & DDG        |
| 27  | `intext:"Firstname Lastname" "dox" OR "leak" OR "dump"`   | Pages where someone already tried to dox you                                                                        | Google & DDG        |
| 28  | `!pastebin your.email@company.com` (DuckDuckGo bang)      | Instant Pastebin search via DDG                                                                                             | DuckDuckGo only     |
| 29  | `!gh yourcompany password` (DuckDuckGo bang)              | Instant GitHub search via DDG                                                                                               | DuckDuckGo only     |
| 30  | Reverse image search with your profile photo             | Finds every website using your exact headshot (forums, company pages, data brokers, etc.)                          | Google Images       |

4. Document every hit and immediately start the removal/opt-out process.

Run this full list at least once per quarter (or automate it), and you’ll stay far ahead of anyone trying to dox you or your team.
