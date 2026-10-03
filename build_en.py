#!/usr/bin/env python3
"""내마음내과 홈페이지 영어판 생성기 (en/ 폴더).

build.py 를 실행하면 함께 실행됩니다. 공통 아이콘·스타일은 build.py 의 것을 쓰고,
영어 문구는 이 파일에서 관리합니다. 한국어 내용을 바꾸면 여기 영어 문구도 함께 고쳐 주세요.
"""
import re
from pathlib import Path

import build as ko
from build import icon, li, LOGO_MARK, CURRENT, CLOSED, HEAD_FONTS, CLINIC as KO

OUT = ko.ROOT / "en"

CLINIC = {
    "name": "My Heart Internal Medicine",
    "name_full": "My Heart Internal Medicine Clinic",
    "name_ko": KO["name_full"],
    "slogan": "Your health, always close by",
    "phone": KO["phone"],
    "phone_intl": "+82-31-480-6870",
    "address": "5F, Ansan Jungang Noblesse, 17 Yesuldaehak-ro, Danwon-gu, Ansan-si, Gyeonggi-do, Korea",
    "building": "5th floor, Ansan Jungang Noblesse (Hana Bank building)",
    "transit": "Within 500 m of Exit 1, Jungang Station (Seoul Subway Line 4)",
    "parking": "Underground parking in the building (first 1 hour 30 minutes free)",
    "owner": "Yongwook Kim",
    "biz_no": KO["biz_no"],
    "domain": KO["domain"],
}

SEO_KEYWORDS = ("My Heart Internal Medicine Clinic, MyHeart Internal Medicine Clinic, Naemaeum Internal Medicine, 내마음내과의원, Ansan internal medicine, "
                "Ansan health checkup, Ansan endoscopy, Ansan gastroscopy, Ansan colonoscopy, Ansan ultrasound, "
                "female doctor Ansan, Jungang Station clinic")

HOURS = [
    ("Weekdays", "08:00 – 18:00", "Lunch break 13:00 – 14:00", False),
    ("Saturday", "08:00 – 13:00", "", False),
    ("Sunday", "Closed", "", True),
    ("Public holidays", "Closed", "", True),
]

NAV = [
    ("about.html", "About Us"),
    ("clinic.html", "Services"),
    ("checkup.html", "Health Checkups"),
    ("info.html", "Visiting Us"),
    ("notice.html", "News"),
]

def logo(white=False):
    src = "assets/img/logo-white.png" if white else "assets/img/logo.png"
    return f'<a class="logo" href="./"><img src="{src}" alt="{CLINIC["name"]}" width="291" height="87"></a>'

def hours_table():
    rows = ""
    for d, t, note, closed in HOURS:
        extra = f'<span class="h-note">{note}</span>' if note else ""
        rows += f'<tr><th scope="row">{d}</th><td{CLOSED if closed else ""}><strong>{t}</strong>{extra}</td></tr>'
    return f'<table class="hours">{rows}</table>'

def header(current):
    def is_current(href):
        return href == current or (href == "notice.html" and current.startswith("notice-"))
    links = "".join(f'<a href="{h}"{CURRENT if is_current(h) else ""}>{l}</a>' for h, l in NAV)
    return f'''<header class="site-header">
  <div class="wrap">
    {logo()}
    <button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">{icon("menu")}</button>
    <nav class="nav" id="site-nav" aria-label="Main menu" hidden>{links}</nav>
    {ko.lang_switch("en", current)}
    <a class="header-call" href="tel:{CLINIC["phone"]}">{icon("phone")}{CLINIC["phone"]}</a>
  </div>
</header>'''

def footer():
    return f'''<footer class="site-footer">
  <div class="wrap">
    {logo(white=True)}
    <dl>
      <dt>Clinic</dt><dd>{CLINIC["name_full"]} ({CLINIC["name_ko"]}, Naemaeum Internal Medicine)</dd>
      <dt>Representative</dt><dd>{CLINIC["owner"]}, M.D.</dd>
      <dt>Address</dt><dd>{CLINIC["address"]}</dd>
      <dt>Phone</dt><dd>{CLINIC["phone"]} ({CLINIC["phone_intl"]})</dd>
      <dt>Business reg. no.</dt><dd>{CLINIC["biz_no"]}</dd>
    </dl>
    <p class="legal">Internal medicine, health checkups, gastroscopy, colonoscopy, ultrasound and care by a female internist near Jungang Station, Ansan.</p>
    <p class="legal">© {CLINIC["name_full"]}. Medical information on this website is general guidance only. For an accurate diagnosis and treatment, please visit the clinic and consult our doctors.</p>
  </div>
</footer>
<nav class="mbar" aria-label="Quick links">
  <a class="call" href="tel:{CLINIC["phone"]}">{icon("phone")}Call</a>
  <a href="info.html#hours">{icon("clock")}Hours</a>
  <a href="info.html#location">{icon("pin")}Directions</a>
</nav>
<script>
(function(){{
  var b=document.querySelector('.menu-btn'),n=document.getElementById('site-nav');
  if(!b||!n)return;
  b.addEventListener('click',function(){{var o=n.hidden;n.hidden=!o;b.setAttribute('aria-expanded',String(o));}});
}})();
</script>'''

def page(filename, title, description, body):
    page_title = (f'{CLINIC["name_full"]} | Internal Medicine, Health Checkups & Endoscopy in Ansan'
                  if filename == "index.html" else f'{title} | {CLINIC["name_full"]}, Ansan')
    path = "" if filename == "index.html" else filename
    url = f'{CLINIC["domain"]}/en/{path}'
    meta = (f'<title>{page_title}</title>'
            f'<meta name="description" content="{description}">'
            f'<meta name="keywords" content="{SEO_KEYWORDS}">{ko.verify_meta()}'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="{CLINIC["name_full"]}">'
            f'<meta property="og:locale" content="en_US"><meta property="og:url" content="{url}">'
            f'<meta property="og:title" content="{page_title}">'
            f'<meta property="og:description" content="{description}">'
            f'<meta property="og:image" content="{CLINIC["domain"]}/assets/img/doctors-banner-800.jpg">'
            f'<link rel="icon" href="assets/img/favicon.png"><link rel="canonical" href="{url}">{ko.hreflang(filename)}'
            f'{ko.json_ld("en") if filename == "index.html" else ""}'
            f'{HEAD_FONTS}<link rel="stylesheet" href="assets/style.css">')
    content = f'{header(filename)}\n<main>\n{body}\n</main>\n{footer()}'
    html = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{meta}\n</head>\n<body>\n{content}\n</body>\n</html>\n')
    # en/ 폴더에서 보므로 공용 이미지·스타일 경로를 한 단계 위로
    return re.sub(r'(?<=["\s,])assets/', '../assets/', html)

def page_hero(eyebrow, title, lead, subnav=None):
    sub = ""
    if subnav:
        sub = '<div class="subnav"><div class="wrap">' + "".join(
            f'<a href="#{a}">{l}</a>' for a, l in subnav) + "</div></div>"
    return f'''<section class="page-hero"><div class="wrap">
  <div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{lead}</p>
</div></section>{sub}'''

section_head = ko.section_head

# ── Doctors ──────────────────────────────────────────────────────────
DOCTORS = [
    {
        "id": "kimyw", "name": "Yongwook Kim", "role": "Chief Director", "room": "Exam Room 1",
        "spec": "Internal Medicine Specialist · Gastrointestinal Endoscopy Subspecialist",
        "photo": "assets/img/doctor-kimyw.jpg", "career": [], "societies": [], "awards": [],
    },
    {
        "id": "kimjw", "name": "Jiwoo Kim", "role": "Director", "room": "Exam Room 2",
        "spec": "Internal Medicine Specialist · Gastrointestinal Endoscopy Subspecialist",
        "photo": "assets/img/doctor-kimjw.jpg",
        "career": [
            "M.D., Yonsei University College of Medicine",
            "Internship, Severance Hospital, Yonsei University",
            "Residency in Internal Medicine, Severance Hospital, Yonsei University",
            "Clinical Fellowship in Gastroenterology, Severance Hospital, Yonsei University",
            "Master's and doctoral coursework, Department of Internal Medicine, Yonsei University College of Medicine",
            "Gastrointestinal Endoscopy Subspecialist",
            "Abdominal Ultrasound Subspecialist, Korean Association for the Study of the Liver",
            "Certified mammography equipment operator",
        ],
        "societies": [
            "Korean Association of Internal Medicine", "Korean Society of Gastrointestinal Endoscopy",
            "Korean Association for the Study of Intestinal Diseases", "Korean Society of Gastroenterology",
            "Korean Association for the Study of the Liver", "Korean Society of Hypertension",
            "Korean Diabetes Association", "Korean Endocrine Society", "Korean Society of Clinical Cardiology",
            "Korean Society of Ultrasound in Medicine", "Korean Society of Echocardiography",
        ],
        "awards": [
            "Excellent Paper Award, Korean Society of Gastroenterology (2019)",
            "Research at the Yoshikazu Uchida lab, School of Medicine, University of California, San Francisco (UCSF) (2016)",
        ],
        "papers": [
            '<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC12989655/" target="_blank" rel="noopener"><em>Effectiveness and Tolerability of Anti-Tumor Necrosis Factor Alpha Therapy in Refractory Intestinal Behçet\'s Disease: A Large Single-Center Study</em></a>. <span class="muted">Gut and Liver. 2026;20(2):305–314</span>',
        ],
    },
]

def doctor_card(d):
    blocks = [("Career", d["career"]), ("Professional societies", d["societies"]), ("Awards and research", d["awards"]), ("Publications", d.get("papers", []))]
    detail = "".join(f'<h4>{t}</h4><ul>{li(xs)}</ul>' for t, xs in blocks if xs)
    return f'''<article class="doctor" id="dr-{d["id"]}">
  <img class="doc-photo" src="{d["photo"]}" alt="Dr. {d["name"]}, {d["role"]}" width="640" height="640" loading="lazy">
  <div class="doc-body">
    <div class="role">{d["room"]} · {d["role"]}</div>
    <h3>Dr. {d["name"]} <small>{d["role"]}</small></h3>
    <p class="spec">{d["spec"]}</p>
    {detail}
  </div>
</article>'''

ROOMS = [
    ("room-reception", "Reception"), ("room-xray", "X-ray room"), ("room-iv", "IV therapy room"),
    ("room-lab", "Basic testing room"), ("room-recovery", "Recovery room"), ("room-endoscopy", "Endoscopy room"),
    ("room-ultrasound", "Ultrasound room"),
]

def gallery():
    return "".join(
        f'<figure><img src="assets/img/{f}.jpg" alt="{CLINIC["name"]} {n.lower()}" loading="lazy"><figcaption>{n}</figcaption></figure>'
        for f, n in ROOMS)

# ── Services ─────────────────────────────────────────────────────────
SERVICES = [
    ("general", "steth", "General internal medicine", "Care for everyday acute illnesses such as colds, gastroenteritis and indigestion."),
    ("chronic", "pulse", "Chronic disease care", "Ongoing management of high blood pressure, diabetes and high cholesterol."),
    ("endoscopy", "scope", "GI endoscopy", "Gastroscopy and colonoscopy performed by gastrointestinal endoscopy subspecialists."),
    ("ultrasound", "wave", "Ultrasound", "Abdominal, thyroid, carotid, cardiac and breast ultrasound."),
    ("thyroid", "thyroid", "Thyroid disease", "Diagnosis and management with thyroid function tests, ultrasound and fine-needle aspiration (FNA)."),
    ("checkup", "clipboard", "Health checkups", "National health screenings and insurer-designated checkups."),
    ("vaccine", "syringe", "Vaccinations", "Adult vaccines including flu, pneumococcal, shingles and hepatitis."),
    ("iv", "drop", "IV therapy", "IV fluids prescribed when needed after a consultation."),
]

CLINIC_DETAIL = {
    "general": (["Colds, flu and body aches", "Acute gastroenteritis, abdominal pain, indigestion", "Headache, dizziness",
                 "Fatigue and other symptoms with an unclear cause"],
                "For sudden symptoms, we look for the cause and guide you through the tests and treatment you need."),
    "chronic": (["High blood pressure", "Diabetes", "High cholesterol (dyslipidemia)", "Fatty liver"],
                "Chronic conditions need steady care. We check your numbers with regular tests and review your lifestyle and medication together."),
    "endoscopy": (["Gastroscopy (sedation available)", "Colonoscopy (sedation available)", "Recovery room after sedated endoscopy"],
                  "Gastroscopy and colonoscopy are performed by gastrointestinal endoscopy subspecialists. After a sedated endoscopy, you can rest in the recovery room before going home."),
    "ultrasound": (["Upper abdomen: liver cancer, cirrhosis, fatty liver, pancreatic cancer, gallstones and more",
                    "Thyroid: thyroid cancer, thyroid nodules, thyroiditis and more",
                    "Carotid: stroke risk, atherosclerosis, heart attack risk and more",
                    "Heart: heart attack, arrhythmia, other heart conditions",
                    "Breast: breast cancer, breast tumors, cysts and more"],
                   "Exams use a Philips Affiniti 70 ultrasound system. Breast and cardiac ultrasound are performed by our female physician."),
    "thyroid": (["Hyperthyroidism and hypothyroidism", "Follow-up of thyroid nodules", "Thyroid ultrasound",
                 "Thyroid fine-needle aspiration (FNA)"],
                "Symptoms such as fatigue, weight change or palpitations can be related to the thyroid."),
    "checkup": (["National health screening", "Samsung Life designated checkup clinic", "Korea University Hospital partner clinic"],
                "See the Health Checkups page for details."),
    "vaccine": (["Influenza (flu)", "Pneumococcal", "Shingles (Shingrix)", "HPV (Gardasil 9)", "Hepatitis A and B",
                 "Td/Tdap, MMR, chickenpox, meningococcal (Menveo)"],
                "Vaccine prices are listed under non-covered fees on the Visiting Us page."),
    "iv": (["Dehydration, recovery after gastroenteritis", "Fatigue"],
           "Prescribed only when needed after a consultation, in a separate, comfortable IV room."),
}

CLINIC_EXTRA = {
    "thyroid": """<div class="sub-blocks">
  <div class="sub-block">
    <span class="tag">Checking for nodules and cancer</span>
    <h3>Thyroid ultrasound</h3>
    <p>Used to find nodules that cannot be felt by hand, to screen people at high risk of thyroid cancer, and to check for recurrence or spread after thyroid cancer surgery.</p>
    <p>When a nodule is found, it also helps tell whether it is a fluid-filled cyst or a solid lump.</p>
  </div>
  <div class="sub-block">
    <span class="tag">Looking at nodules more closely</span>
    <h3>Thyroid fine-needle aspiration (FNA)</h3>
    <p>When ultrasound finds a nodule or shows signs that it may be cancerous, a very thin needle is used to collect cells from the nodule for testing.</p>
    <p>It is the standard test for assessing whether a nodule may be cancer, needs no special preparation, and takes only a short time.</p>
  </div>
</div>""",
}

def svc_cards():
    return "".join(
        f'<a class="svc" href="clinic.html#{k}"><span class="ico">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></a>'
        for k, ic, t, d in SERVICES)

# ── Fees ─────────────────────────────────────────────────────────────
FEES_EXAM = [
    ("Flu test", "30,000"), ("Arterial stiffness test", "30,000"), ("Sedated endoscopy care fee 2", "40,000"),
    ("Sedated endoscopy care fee 3", "90,000"), ("Thyroid ultrasound", "50,000"), ("Carotid ultrasound", "50,000"),
    ("Shingles vaccine (Shingrix)", "250,000"), ("HPV vaccine (Gardasil 9)", "210,000"), ("Flu vaccine", "30,000"),
    ("Td", "30,000"), ("Tdap", "50,000"), ("Pneumococcal vaccine", "130,000"), ("MMR", "30,000"),
    ("Hepatitis A vaccine", "70,000"), ("Hepatitis B vaccine", "35,000"), ("Chickenpox vaccine", "40,000"),
    ("Meningococcal vaccine (Menveo)", "160,000"),
]
FEES_DOCS = [
    ("General medical certificate", "20,000"), ("Health certificate", "20,000"),
    ("Certificate for work capacity assessment", "10,000"), ("Death certificate", "10,000"),
    ("Disability assessment certificate (physical)", "15,000"), ("Disability assessment certificate (mental)", "40,000"),
    ("Permanent impairment certificate", "100,000"), ("Military service certificate", "20,000"),
    ("National Pension disability certificate", "15,000"), ("Injury certificate (under 3 weeks)", "100,000"),
    ("Injury certificate (3 weeks or more)", "150,000"), ("General medical certificate in English", "20,000"),
    ("Certificate of outpatient visits", "3,000"), ("Certificate of treatment", "3,000"),
    ("Pre-employment physical (public servants)", "30,000"), ("Pre-employment physical (general)", "30,000"),
    ("Health certificate for food service workers", "25,000"),
    ("Copy of medical records (1–5 pages)", "1,000 per page"), ("Copy of medical records (6+ pages)", "100 per page"),
    ("Medical images on CD", "10,000"), ("Copy of a certificate", "10,000"),
]

def fee_table(rows, col):
    body = "".join(f'<tr><td>{n}</td><td class="num">{p}</td></tr>' for n, p in rows)
    return (f'<div class="table-wrap"><table class="table"><thead><tr><th>Item</th>'
            f'<th class="num">{col}</th></tr></thead><tbody>{body}</tbody></table></div>')

# ── News (same file names as the Korean notices) ─────────────────────
def notice_female_doctor():
    d = DOCTORS[1]
    return f'''<p>Hello from {CLINIC["name"]}.</p>
<p>Our female physician, <strong>Dr. Jiwoo Kim</strong>, sees patients in <strong>Exam Room 2</strong>.
If you would prefer to be seen by a female doctor, please feel free to visit.</p>
<figure class="post-figure"><img src="assets/img/notice-female-doctor.jpg" alt="Female physician now seeing patients: Dr. Jiwoo Kim, Exam Room 2 (image in Korean)" width="768" height="1024"></figure>
<h2>Dr. Jiwoo Kim: career</h2><ul>{li(d["career"])}</ul>
<h2>Professional societies</h2><ul>{li(d["societies"])}</ul>
<h2>Awards and research</h2><ul>{li(d["awards"])}</ul>
<h2>Publications</h2><ul>{li(d["papers"])}</ul>
<p>See our hours on the <a href="info.html#hours">Visiting Us</a> page, or call {CLINIC["phone"]}.</p>'''

def notice_ultrasound():
    return f'''<p>{CLINIC["name"]} now uses a <strong>Philips Affiniti 70</strong> ultrasound system, and our female physician, Dr. Jiwoo Kim, performs breast and cardiac ultrasound.</p>
<figure class="post-figure"><img src="assets/img/notice-ultrasound.jpg" alt="Breast and cardiac ultrasound by a female physician with the Philips Affiniti 70 (image in Korean)" width="556" height="556"></figure>
<h2>About the equipment</h2>
<p>This ultrasound system is also used in university hospitals and covers many areas, including the abdomen, heart, breast, thyroid, carotid arteries and musculoskeletal system.</p>
<p>Its micro-flow imaging (Micro CPA), beamforming and PureWave technologies help produce clear images even for patients who are harder to image, such as those with obesity or liver disease.</p>
<h2>Types of ultrasound exams</h2>
<ul>{li(CLINIC_DETAIL["ultrasound"][0])}</ul>
<p>For appointments and prices, please call {CLINIC["phone"]}.</p>'''

def notice_obesity():
    return f'''<p>Hello from {CLINIC["name"]}.</p>
<p>We offer <strong>weight management consultations</strong>, including consultations on <strong>weight-loss medication</strong> such as Wegovy and Mounjaro.</p>
<h2>What the consultation covers</h2>
<ul>
  <li>Body composition and blood tests to check your current condition</li>
  <li>Checking for related conditions such as high blood pressure, diabetes, high cholesterol and fatty liver</li>
  <li>Advice on diet, exercise and daily habits</li>
  <li>Medication when needed, after an examination by a specialist</li>
</ul>
<h2>About weight-loss medication</h2>
<ul>
  <li><strong>Wegovy (semaglutide)</strong>: a GLP-1 injection given once a week.</li>
  <li><strong>Mounjaro (tirzepatide)</strong>: an injection that acts on two hormones, GLP-1 and GIP, given once a week.</li>
</ul>
<p>Both are prescription-only medicines and can be used only after a doctor's examination and prescription. We prescribe them after checking that you meet the criteria, such as body mass index (BMI) and related conditions. Side effects such as nausea, vomiting, diarrhea and constipation may occur. Results and side effects vary from person to person, so please discuss them fully with your doctor.</p>
<p>For a consultation, please call {CLINIC["phone"]}.</p>'''

NOTICES = [
    ("notice-1.html", "2026-10-02", "Female physician now seeing patients",
     "Dr. Jiwoo Kim, our female internist, sees patients in Exam Room 2.", "notice-female-doctor.jpg", notice_female_doctor),
    ("notice-3.html", "2026-10-02", "Weight management consultations",
     "Consultations on weight-loss medication such as Wegovy and Mounjaro are available.", None, notice_obesity),
    ("notice-2.html", "2026-10-02", "Breast and cardiac ultrasound by a female physician",
     "Breast and cardiac ultrasound with the Philips Affiniti 70 system.", "notice-ultrasound.jpg", notice_ultrasound),
]

def notice_items(limit=None, compact=False):
    out = ""
    for fn, d, t, sm, th, _ in NOTICES[:limit]:
        date = d.replace("-", ".")
        if compact:
            out += f'<li><a href="{fn}"><span class="n-title">{t}</span><time datetime="{d}">{date}</time></a></li>'
        else:
            thumb = (f'<img class="n-thumb" src="assets/img/{th}" alt="" loading="lazy">' if th
                     else f'<span class="n-thumb n-thumb-logo">{LOGO_MARK}</span>')
            out += (f'<li><a href="{fn}">{thumb}'
                    f'<span class="n-text"><span class="n-title">{t}</span><span class="n-sum">{sm}</span>'
                    f'<time datetime="{d}">{date}</time></span></a></li>')
    return out

# ── Pages ────────────────────────────────────────────────────────────
def home():
    docs = "".join(f'''<a class="doc-teaser" href="about.html#dr-{d["id"]}">
  <img src="{d["photo"]}" alt="Dr. {d["name"]}, {d["role"]}" width="640" height="640" loading="lazy">
  <span><span class="role">{d["room"]}</span><strong>Dr. {d["name"]}, {d["role"]}</strong><span class="spec">{d["spec"]}</span></span>
</a>''' for d in DOCTORS)
    return f'''<section class="hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">{CLINIC["slogan"]}</div>
      <h1>Care that listens,<br><em>My Heart Internal Medicine</em></h1>
      <p class="lead">Two internal medicine specialists, including a female physician, care for you. Endoscopy, ultrasound and health checkups are all available in one place.</p>
      <div class="badges">
        <span class="badge">{icon("shield")}Samsung Life designated checkup clinic</span>
        <span class="badge">{icon("shield")}Korea University Hospital partner clinic</span>
      </div>
      <div class="hero-actions">
        <a class="btn primary" href="tel:{CLINIC["phone"]}">{icon("phone")}Call {CLINIC["phone"]}</a>
        <a class="btn ghost" href="info.html#hours">See opening hours</a>
      </div>
    </div>
    <figure class="hero-photo"><img src="assets/img/doctors-banner-800.jpg" srcset="assets/img/doctors-banner-800.jpg 800w, assets/img/doctors-banner.jpg 1254w" sizes="(max-width:860px) 360px, 440px" alt="Dr. Yongwook Kim and Dr. Jiwoo Kim" width="800" height="800"></figure>
  </div>
</section>

<section class="quick"><div class="wrap"><div class="quick-grid">
  <div class="quick-card"><h3>{icon("clock")}Opening hours</h3>{hours_table()}</div>
  <div class="quick-card"><h3>{icon("phone")}Call us</h3>
    <a class="big" href="tel:{CLINIC["phone"]}">{CLINIC["phone"]}</a>
    <p>Please call with any questions about appointments or checkups. Phone support is mainly in Korean.</p>
    <a class="more" href="info.html#fees">See non-covered fees →</a></div>
  <div class="quick-card"><h3>{icon("pin")}Getting here</h3>
    <p>{CLINIC["building"]}</p><p>{CLINIC["transit"]}</p><p>{CLINIC["parking"]}</p>
    <a class="more" href="info.html#location">Directions →</a></div>
</div></div></section>

<section class="section"><div class="wrap">
  {section_head("Services", "What we treat", "From everyday illnesses to chronic disease care, endoscopy, ultrasound and health checkups.")}
  <div class="svc-grid">{svc_cards()}</div>
</div></section>

<section class="section alt"><div class="wrap">
  {section_head("Our doctors", "Care by internal medicine specialists")}
  <div class="doc-teasers">{docs}</div>
</div></section>

<section class="section"><div class="wrap">
  {section_head("Health video", "Managing chronic disease with Dr. Jiwoo Kim", "Why do diabetes, high blood pressure and high cholesterol often come together? Watch to learn how to manage them. (Video in Korean)")}
  <div class="video">
    <iframe src="https://www.youtube-nocookie.com/embed/{ko.VIDEO_ID}" title="{ko.VIDEO_TITLE}" loading="lazy"
      allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>
  <p class="video-src">Source: HiDoc health channel · <a href="https://youtu.be/{ko.VIDEO_ID}" target="_blank" rel="noopener">Watch on YouTube</a></p>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="section-head row"><div><div class="eyebrow">News</div><h2>News from the clinic</h2></div>
    <a class="link-more" href="notice.html">See all →</a></div>
  <ul class="notice-list compact">{notice_items(4, compact=True)}</ul>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    {section_head("Health checkups", "Regular checkups close to home")}
    <ul class="checklist">
      <li>National health screening</li><li>Samsung Life designated checkup clinic</li><li>Korea University Hospital partner clinic</li>
      <li>Endoscopy, ultrasound, X-ray and recovery rooms on site</li>
    </ul>
    <div class="hero-actions"><a class="btn primary" href="checkup.html">About health checkups</a></div>
  </div>
  <div class="panel">
    <h3>Before your checkup</h3>
    <ul class="checklist">
      <li>No food after 9 p.m. the night before (a little water is fine)</li>
      <li>Bring your ID (foreign residents: alien registration card or passport)</li>
      <li>Tell us in advance about any medication you take</li>
    </ul>
  </div>
</div></section>
'''

GREETING = [
    "Hello,",
    f"Thank you for visiting {CLINIC['name']}.",
    "With good facilities and our best care, we strive to go beyond each patient's satisfaction and bring happiness through medical care. We will treat every patient with warmth and sincerity.",
    "Thank you.",
]

def about():
    paras = "".join(f"<p>{p}</p>" for p in GREETING)
    return page_hero("About us", "About the clinic", CLINIC["slogan"],
                     [("greeting", "Welcome"), ("doctors", "Our doctors"), ("facility", "Facilities")]) + f'''
<section class="section anchor" id="greeting"><div class="wrap">
  {section_head("Welcome", "Care that listens to you")}
  <div class="greeting">{paras}<p class="sign">{CLINIC["owner"]}, M.D., Chief Director</p></div>
</div></section>

<section class="section alt anchor" id="doctors"><div class="wrap">
  {section_head("Our doctors", "Meet our doctors")}
  <div class="doctors">{"".join(doctor_card(d) for d in DOCTORS)}</div>
</div></section>

<section class="section anchor" id="facility"><div class="wrap">
  {section_head("Facilities", "A comfortable, clean place for care")}
  <div class="gallery">{gallery()}</div>
</div></section>
'''

def clinic():
    blocks = ""
    for k, ic, t, _ in SERVICES:
        items, desc = CLINIC_DETAIL[k]
        blocks += f'''<div class="detail anchor" id="{k}">
  <div><span class="ico">{icon(ic)}</span><h2>{t}</h2></div>
  <div><p>{desc}</p><ul>{li(items)}</ul>{CLINIC_EXTRA.get(k, "")}</div>
</div>'''
    return page_hero("Services", "Our services", "From acute illness to chronic disease care, endoscopy, ultrasound and health checkups.",
                     [(k, t) for k, _, t, _ in SERVICES]) + f'''
<section class="section"><div class="wrap">{blocks}
  <p class="notice" style="margin-top:24px">Treatment and results vary depending on each person's condition. If you have symptoms, please visit and consult our doctors.</p>
</div></section>
'''

def checkup():
    return page_hero("Health checkups", "Health checkups", "Get regular checkups close to home and review your results with a specialist.",
                     [("types", "Checkup types"), ("equipment", "Facilities"), ("prepare", "How to prepare")]) + f'''
<section class="section anchor" id="types"><div class="wrap">
  <div class="detail">
    <div><span class="tag">National Health Insurance Service</span><h2>National health screening</h2></div>
    <div><p>You can have the health screening offered by the National Health Insurance Service (NHIS). You can check whether you are eligible on the NHIS website or app.</p></div>
  </div>
  <div class="detail">
    <div><span class="tag">Designated clinic</span><h2>Insurer-designated checkups</h2></div>
    <div><p>We are a Samsung Life designated checkup clinic, so you can have checkups needed for insurance enrollment or review here.</p></div>
  </div>
  <div class="detail">
    <div><span class="tag">Partner clinic</span><h2>Korea University Hospital partner clinic</h2></div>
    <div><p>We are a partner clinic of Korea University Hospital. Please call us for details.</p></div>
  </div>
  <div class="detail">
    <div><span class="tag">Additional tests</span><h2>Endoscopy · Ultrasound</h2></div>
    <div><p>If needed, you can add gastroscopy or colonoscopy (sedation available) and abdominal, thyroid, carotid, cardiac or breast ultrasound.</p>
      <p><a href="clinic.html#ultrasound" style="color:var(--blue);font-weight:600">More about ultrasound →</a></p></div>
  </div>
</div></section>

<section class="section alt anchor" id="equipment"><div class="wrap">
  {section_head("Facilities", "From testing to recovery, all on one floor")}
  <div class="gallery">{gallery()}</div>
</div></section>

<section class="section anchor" id="prepare"><div class="wrap split">
  <div>
    {section_head("How to prepare", "Please check before your checkup")}
    <ul class="checklist">
      <li>Do not eat after 9 p.m. the night before. A little water is fine.</li>
      <li>Please bring your ID (foreign residents: alien registration card or passport).</li>
      <li>Tell our staff in advance about any medication you take, such as blood pressure medicine.</li>
      <li>Do not take diabetes medication or insulin on the morning of the test; please talk to our staff first.</li>
      <li>Do not drive on the day of a sedated endoscopy.</li>
    </ul>
  </div>
  <div class="panel">
    <h3>Checkup inquiries</h3>
    <p style="color:var(--muted)">Checkups start from 08:00 on weekdays. Please call to book and to check which tests are available.</p>
    <div class="hero-actions"><a class="btn primary" href="tel:{CLINIC["phone"]}">{icon("phone")}{CLINIC["phone"]}</a></div>
  </div>
</div></section>
'''

def info():
    q = KO["map_query"]
    return page_hero("Visiting us", "Visiting us", "Opening hours, directions and non-covered fees.",
                     [("hours", "Opening hours"), ("location", "Directions"), ("fees", "Non-covered fees"), ("docs", "Certificates")]) + f'''
<section class="section anchor" id="hours"><div class="wrap split">
  {section_head("Opening hours", "When we are open", "Closed on Sundays and public holidays. Temporary closures are announced in News.")}
  <div class="panel">{hours_table()}</div>
</div></section>

<section class="section alt anchor" id="location"><div class="wrap split">
  <div>
    {section_head("Directions", CLINIC["address"])}
    <ul class="info-list">
      <li>{icon("pin")}<span><strong>Location</strong>{CLINIC["building"]}</span></li>
      <li>{icon("train")}<span><strong>Subway</strong>{CLINIC["transit"]}</span></li>
      <li>{icon("car")}<span><strong>Parking</strong>{CLINIC["parking"]}</span></li>
      <li>{icon("phone")}<span><strong>Phone</strong>{CLINIC["phone"]} ({CLINIC["phone_intl"]})</span></li>
    </ul>
    <p style="color:var(--muted);margin-top:12px">Korean address for taxis and map apps: {KO["address"]}</p>
    <div class="map-links">
      <a class="btn primary" href="https://map.naver.com/p/search/{q}" target="_blank" rel="noopener">{icon("map")}Naver Map</a>
      <a class="btn ghost" href="https://map.kakao.com/?q={q}" target="_blank" rel="noopener">Kakao Map</a>
    </div>
  </div>
  <figure class="framed"><img src="assets/img/room-reception.jpg" alt="{CLINIC["name"]} reception" loading="lazy"></figure>
</div></section>

<section class="section anchor" id="fees"><div class="wrap">
  {section_head("Non-covered fees", "Fees not covered by national health insurance", "Listed in accordance with Article 45 of the Korean Medical Service Act. (Unit: KRW)")}
  <div class="fees">
    <div><h3 class="fee-title">Vaccines and tests</h3>{fee_table(FEES_EXAM, "Price")}</div>
    <div><h3 class="fee-title">Certificates and documents</h3>{fee_table(FEES_DOCS, "Maximum price")}</div>
  </div>
</div></section>

<section class="section alt anchor" id="docs"><div class="wrap">
  {section_head("Certificates", "Requesting documents")}
  <div class="notice"><strong>In person:</strong> please bring your ID. <strong>On someone's behalf:</strong> a copy of the patient's ID, your own ID, and a family relationship certificate or a letter of authorization are required.</div>
</div></section>
'''

def notice_list():
    return page_hero("News", "News", "Schedule changes and news from the clinic.") + f'''
<section class="section"><div class="wrap"><ul class="notice-list">{notice_items()}</ul></div></section>
'''

def notice_post(d, t, body_fn):
    return f'''<section class="page-hero"><div class="wrap">
  <div class="eyebrow"><a href="notice.html" style="color:inherit">News</a></div><h1>{t}</h1>
  <p><time datetime="{d}">{d.replace("-", ".")}</time></p>
</div></section>
<section class="section"><div class="wrap"><article class="post">{body_fn()}
  <p class="post-back"><a class="btn ghost" href="notice.html">Back to list</a></p>
</article></div></section>
'''

PAGES = [
    ("index.html", "Home", "My Heart Internal Medicine Clinic near Jungang Station, Ansan: internal medicine specialists, a female internist, gastroscopy and colonoscopy (sedation available), ultrasound and national health screening.", home),
    ("about.html", "About Us", "Welcome message, our doctors and facilities at My Heart Internal Medicine Clinic, Ansan.", about),
    ("clinic.html", "Services", "General internal medicine, chronic disease care, gastroscopy and colonoscopy, ultrasound, thyroid FNA and vaccinations in Ansan.", clinic),
    ("checkup.html", "Health Checkups", "National health screening, insurer-designated checkups, endoscopy and ultrasound add-ons and how to prepare.", checkup),
    ("info.html", "Visiting Us", "Opening hours, directions from Jungang Station Exit 1, parking, non-covered fees and certificates.", info),
    ("notice.html", "News", "News and announcements from My Heart Internal Medicine Clinic.", notice_list),
] + [(fn, t, sm, (lambda d=d, t=t, b=b: notice_post(d, t, b))) for fn, d, t, sm, _, b in NOTICES]

def build(preview_dir=None):
    OUT.mkdir(exist_ok=True)
    for fn, title, desc, body_fn in PAGES:
        html = page(fn, title, desc, body_fn())
        (OUT / fn).write_text(html, encoding="utf-8")
        if preview_dir:
            (Path(preview_dir) / "en").mkdir(parents=True, exist_ok=True)
            (Path(preview_dir) / "en" / fn).write_text(html, encoding="utf-8")
    return [p[0] for p in PAGES]

if __name__ == "__main__":
    print("built en/", build())
