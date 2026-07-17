#!/usr/bin/env python3
"""Inject a static SEO layer into the Claude Design standalone bundle.
Re-runnable on any fresh Design export: adds head meta + JSON-LD + a
crawler-visible <noscript> content mirror. Visual site is unchanged (the
noscript is inert when JS runs; injected head tags don't affect the runtime)."""
import re, sys, json

path = sys.argv[1]
html = open(path, encoding="utf-8").read()

if "<!-- seo-layer -->" in html:
    print("SEO layer already present; skipping.")
    sys.exit(0)

TITLE = "DataKollekt AB — Data &amp; AI-Agent Engineering in Stockholm | Pooya Shahryari"
DESC = ("DataKollekt AB is the Stockholm engineering consultancy of Pooya Shahryari — 7+ years "
        "building data platforms for Swedish enterprises (Dun &amp; Bradstreet, Svenska kyrkan, "
        "Wasa Kredit, Axfood), now building production AI-agent and LLM systems. Data engineering, "
        "ETL, data warehousing, and Claude/MCP agent development.")
DESC_PLAIN = re.sub("&amp;", "&", DESC)

SKILLS = ["Data engineering","ETL","ELT","Data warehousing","Data Vault 2.0","Dimensional modeling",
          "SQL","Python","Pentaho","SSIS","Azure Data Factory","Snowflake","PostgreSQL","Oracle",
          "Elasticsearch","Power BI","Qlik","Apache Airflow","Apache Spark","Databricks","Linux",
          "AI agents","Large language models","Claude Agent SDK","Model Context Protocol (MCP)",
          "CI/CD","Infrastructure as code"]

jsonld = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "ProfessionalService",
      "@id": "https://datakollekt.se/#organization",
      "name": "DataKollekt AB",
      "url": "https://datakollekt.se/",
      "slogan": "Omvandlar data till resultat.",
      "description": ("Stockholm engineering consultancy specialising in data platforms, ETL/data "
                      "warehousing, and production AI-agent / LLM systems."),
      "foundingDate": "2021",
      "areaServed": ["Sweden", "European Union"],
      "knowsAbout": SKILLS,
      "founder": {"@id": "https://datakollekt.se/#pooya"},
      "address": {"@type": "PostalAddress", "addressLocality": "Stockholm", "addressCountry": "SE"},
      "sameAs": ["https://www.linkedin.com/in/pooya-sh/", "https://github.com/pooya-sh"]
    },
    {
      "@type": "Person",
      "@id": "https://datakollekt.se/#pooya",
      "name": "Pooya Shahryari",
      "givenName": "Pooya", "familyName": "Shahryari",
      "jobTitle": "Data & AI-Agent Engineer",
      "description": ("Data engineer turned AI-agent engineer and founder of DataKollekt AB. 7+ years "
                      "building data platforms for Swedish enterprises; now building production "
                      "multi-agent AI systems."),
      "url": "https://datakollekt.se/",
      "worksFor": {"@id": "https://datakollekt.se/#organization"},
      "address": {"@type": "PostalAddress", "addressLocality": "Stockholm", "addressCountry": "SE"},
      "knowsLanguage": ["Swedish", "English", "Persian"],
      "knowsAbout": SKILLS,
      "sameAs": ["https://www.linkedin.com/in/pooya-sh/", "https://github.com/pooya-sh"]
    },
    {
      "@type": "WebSite",
      "@id": "https://datakollekt.se/#website",
      "url": "https://datakollekt.se/",
      "name": "DataKollekt AB — Pooya Shahryari",
      "inLanguage": "en",
      "publisher": {"@id": "https://datakollekt.se/#organization"}
    }
  ]
}

head = f'''
  <!-- seo-layer -->
  <meta name="description" content="{DESC}">
  <meta name="author" content="Pooya Shahryari">
  <link rel="canonical" href="https://datakollekt.se/">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="theme-color" content="#0a0c10">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="DataKollekt AB">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{DESC}">
  <meta property="og:url" content="https://datakollekt.se/">
  <meta property="og:locale" content="en_SE">
  <meta property="og:image" content="https://datakollekt.se/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="DataKollekt AB — Data platforms and AI agents that run in production">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{TITLE}">
  <meta name="twitter:description" content="{DESC}">
  <meta name="twitter:image" content="https://datakollekt.se/og-image.png">
  <script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False, separators=(",", ":"))}</script>
  <!-- /seo-layer -->
'''

noscript = '''
<noscript><!-- seo-layer -->
<main>
<h1>DataKollekt AB — Data platforms and AI agents that run in production</h1>
<p>DataKollekt AB is the Stockholm engineering consultancy of <strong>Pooya Shahryari</strong> — 7+ years building data platforms for Swedish enterprises, now building AI-agent systems that stay in production. <em>Omvandlar data till resultat.</em></p>

<h2>Services</h2>
<h3>Data engineering</h3>
<p>ETL/ELT pipelines, data warehousing (Data Vault 2.0, dimensional), and migrations off legacy stacks. Tools: SQL, Python, Pentaho, SSIS, Azure Data Factory, Snowflake, PostgreSQL, Oracle, Elasticsearch, Power BI / Qlik, Apache Airflow, Apache Spark, Databricks.</p>
<h3>AI-agent &amp; LLM systems</h3>
<p>Production agents on the Claude Agent SDK and MCP: autonomous services, custom MCP servers, LLM pipelines with test suites, CI gates, sandboxing and secrets management — engineering discipline applied to AI.</p>
<h3>Automation &amp; platform operations</h3>
<p>Self-healing services, infrastructure-as-code, monitoring, disaster-recovery runbooks, privilege-separated security models, and Linux. Systems that keep running when nobody is watching.</p>

<h2>Selected work (internal R&amp;D)</h2>
<ul>
<li><strong>Quant</strong> — advisory-only AI trading cockpit; FastAPI + SSE backend, React 19 frontend; the AI has zero execution authority; 150+ test files with CI-enforced architecture.</li>
<li><strong>Agent platform infrastructure</strong> — infrastructure-as-code for a multi-agent stack running 24/7 on self-hosted hardware, with privilege separation, keychain-only secrets, and a commit-gate pipeline.</li>
<li><strong>Content engine</strong> — a fleet of hand-built MCP servers and inference/media services; 400+ test files.</li>
<li><strong>Stealth SaaS</strong> — a multi-tenant AI teammate for software teams (in development).</li>
<li>Open source: <a href="https://github.com/pooya-sh/voice-inbox-bot">voice-inbox-bot</a>; spotify-genre-sync.</li>
</ul>

<h2>Founder — Pooya Shahryari</h2>
<p>Data engineer turned AI-agent engineer. 7+ years building data platforms for Swedish enterprises; since 2024 investing in a production multi-agent AI platform running 24/7 on self-hosted infrastructure. DataKollekt is deliberately a one-person consultancy — you work directly with the engineer who built everything.</p>
<h3>Experience</h3>
<ul>
<li>DataKollekt AB — Founder &amp; consultant (2021–present), Stockholm</li>
<li>Dun &amp; Bradstreet (Bisnode) — ETL developer: consolidating ~400 ETL jobs from a dozen legacy technologies into Pentaho (Java, Perl, Bash, PostgreSQL, Oracle, Elasticsearch)</li>
<li>XLENT — Data engineer (2019–2021): Data Vault 2.0 warehouse on Azure for Svenska kyrkan; SQL Server DW at Wasa Kredit</li>
<li>Avaus — Data engineer (2019): customer analytics for Axfood (Python, Snowflake, Teradata)</li>
<li>Academic Work — Java developer (2018–2019)</li>
<li>DIW — Founder (2014–2019): e-commerce</li>
<li>Huddinge kommun — Team lead / acting unit chief (2012–2018)</li>
</ul>
<p>Certifications: Certified SAFe 6 Agilist; Professional Scrum Master (scrum.org). Working languages: Swedish, English, Persian.</p>

<h2>Contact</h2>
<p>Email: <a href="mailto:pooya@datakollekt.se">pooya@datakollekt.se</a> · <a href="https://www.linkedin.com/in/pooya-sh/">LinkedIn</a> · <a href="https://github.com/pooya-sh">GitHub</a> · DataKollekt AB, Stockholm, Sweden.</p>
</main>
<!-- /seo-layer --></noscript>
'''

# 1) lang on the document <html>
html = re.sub(r"<html(?![^>]*\blang=)([^>]*)>", r'<html lang="en"\1>', html, count=1)
# 2) title in the raw head
if re.search(r"<title>.*?</title>", html, re.S):
    html = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", html, count=1, flags=re.S)
else:
    html = re.sub(r"</head>", f"  <title>{TITLE}</title>\n</head>", html, count=1)
# 3) head meta + JSON-LD before </head>
html = re.sub(r"</head>", head + "</head>", html, count=1)
# 4) noscript content mirror right after <body ...>
html = re.sub(r"(<body\b[^>]*>)", r"\1" + noscript, html, count=1)

open(path, "w", encoding="utf-8").write(html)
print("injected. new size:", len(html))
