#!/usr/bin/env python3
"""내마음내과 홈페이지 정적 페이지 생성기.

공통 머리글/바닥글과 병원 정보(CLINIC)를 한 곳에서 관리하고
`python3 build.py` 를 실행하면 같은 폴더에 *.html 페이지를 만듭니다.
새 공지는 아래 NOTICES 맨 위에 추가하면 됩니다.
"""
from pathlib import Path

ROOT = Path(__file__).parent

# ── 병원 기본 정보: 여기만 고치면 모든 페이지에 반영됩니다 ──────────────
CLINIC = {
    "name": "내마음내과",
    "name_full": "내마음내과의원",
    "slogan": "당신의 건강, 늘 가까이에서",
    "phone": "031-480-6870",
    "address": "경기도 안산시 단원구 예술대학로 17 안산중앙노블레스 5층",
    "building": "안산중앙노블레스 건물(하나은행 건물) 5층",
    "transit": "4호선 중앙역 1번 출구에서 500m 이내",
    "parking": "건물 지하주차장 이용 가능 (1시간 30분 무료)",
    "owner": "김용욱",
    "biz_no": "134-92-01762",
    "domain": "https://myheartinternalmed.kr",
    "map_query": "내마음내과의원 안산",
}
CLOSED = ' class="closed"'
CURRENT = ' aria-current="page"'

# 진료시간 (요일, 시간, 부가 설명, 휴진 여부)
HOURS = [
    ("평일", "08:00 ~ 18:00", "점심시간 13:00 ~ 14:00", False),
    ("토요일", "08:00 ~ 13:00", "", False),
    ("일요일", "휴진", "", True),
    ("공휴일", "휴진", "", True),
]

NAV = [
    ("about.html", "병원소개"),
    ("clinic.html", "진료과목"),
    ("checkup.html", "건강검진센터"),
    ("info.html", "이용안내"),
    ("notice.html", "공지사항"),
]

# ── 아이콘 ────────────────────────────────────────────────────────────
def icon(name):
    paths = {
        "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2" />',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        "steth": '<path d="M6 3v5a5 5 0 0 0 10 0V3"/><path d="M11 13v3a4 4 0 0 0 8 0v-2"/><circle cx="19" cy="12" r="2"/>',
        "pulse": '<path d="M3 12h4l2-5 4 10 2-5h6"/>',
        "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
        "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
        "syringe": '<path d="M18 2l4 4M17 7l-9.5 9.5L4 20l3.5-3.5M14 4l6 6M10 8l2 2M7 11l2 2"/>',
        "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 11h6M9 15h4"/>',
        "thyroid": '<path d="M8 6c-3 0-4 4-4 7s1.5 5 4 5 3-2 4-4c1 2 1.5 4 4 4s4-2 4-5-1-7-4-7c-2 0-3 2-4 4-1-2-2-4-4-4z"/>',
        "scope": '<path d="M4 20c4 0 4-6 8-6s4 3 6 3"/><circle cx="19" cy="17" r="2"/><path d="M4 20V8a4 4 0 0 1 8 0"/>',
        "wave": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M7 12c1-3 2-3 3 0s2 3 3 0 2-3 3 0"/><path d="M9 20h6M12 16v4"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
        "map": '<path d="M9 4l-5 2v14l5-2 6 2 5-2V4l-5 2z"/><path d="M9 4v14M15 6v14"/>',
        "car": '<path d="M5 16V11l2-5h10l2 5v5"/><path d="M3 16h18v3H3z"/><circle cx="7.5" cy="13" r="1"/><circle cx="16.5" cy="13" r="1"/>',
        "train": '<rect x="6" y="3" width="12" height="13" rx="3"/><path d="M6 10h12M9 20l-2 2M15 20l2 2M9 16l-1 4M15 16l1 4"/>',
    }
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')

LOGO_MARK = ('<svg viewBox="0 0 40 40" aria-hidden="true">'
             '<circle cx="11" cy="7" r="3.2" fill="none" stroke="#1670E0" stroke-width="2.6"/>'
             '<path d="M20 34 C9 26 5 20 5 15 a7.5 7.5 0 0 1 15-1 a7.5 7.5 0 0 1 15 1 c0 5-4 11-15 19z" '
             'fill="none" stroke="#1670E0" stroke-width="3.2" stroke-linejoin="round"/>'
             '<path d="M13 19 c3 6 11 6 14 0" fill="none" stroke="#3FC9DC" stroke-width="3" stroke-linecap="round"/>'
             '</svg>')

def logo(white=False):
    src = "assets/img/logo-white.png" if white else "assets/img/logo.png"
    return f'<a class="logo" href="./"><img src="{src}" alt="{CLINIC["name"]}" width="291" height="87"></a>'

def hours_table():
    rows = ""
    for d, t, note, closed in HOURS:
        extra = f'<span class="h-note">{note}</span>' if note else ""
        rows += f'<tr><th scope="row">{d}</th><td{CLOSED if closed else ""}><strong>{t}</strong>{extra}</td></tr>'
    return f'<table class="hours">{rows}</table>'

def li(items):
    return "".join(f"<li>{x}</li>" for x in items)

# ── 공통 틀 ───────────────────────────────────────────────────────────
HEAD_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap">')

def header(current):
    def is_current(href):
        return href == current or (href == "notice.html" and current.startswith("notice-"))
    links = "".join(f'<a href="{h}"{CURRENT if is_current(h) else ""}>{l}</a>' for h, l in NAV)
    return f'''<header class="site-header">
  <div class="wrap">
    {logo()}
    <button class="menu-btn" type="button" aria-label="메뉴 열기" aria-expanded="false" aria-controls="site-nav">{icon("menu")}</button>
    <nav class="nav" id="site-nav" aria-label="주요 메뉴" hidden>{links}</nav>
    <a class="header-call" href="tel:{CLINIC["phone"]}">{icon("phone")}{CLINIC["phone"]}</a>
  </div>
</header>'''

def footer():
    return f'''<footer class="site-footer">
  <div class="wrap">
    {logo(white=True)}
    <dl>
      <dt>상호</dt><dd>{CLINIC["name_full"]}</dd>
      <dt>대표자</dt><dd>{CLINIC["owner"]}</dd>
      <dt>주소</dt><dd>{CLINIC["address"]}</dd>
      <dt>전화</dt><dd>{CLINIC["phone"]}</dd>
      <dt>사업자등록번호</dt><dd>{CLINIC["biz_no"]}</dd>
    </dl>
    <p class="legal">© {CLINIC["name_full"]}. 본 홈페이지의 의료 정보는 일반적인 안내이며, 정확한 진단과 치료는 내원하여 의료진과 상담하시기 바랍니다.</p>
  </div>
</footer>
<nav class="mbar" aria-label="빠른 연결">
  <a class="call" href="tel:{CLINIC["phone"]}">{icon("phone")}전화하기</a>
  <a href="info.html#hours">{icon("clock")}진료시간</a>
  <a href="info.html#location">{icon("pin")}오시는 길</a>
</nav>
<script>
(function(){{
  var b=document.querySelector('.menu-btn'),n=document.getElementById('site-nav');
  if(!b||!n)return;
  b.addEventListener('click',function(){{var o=n.hidden;n.hidden=!o;b.setAttribute('aria-expanded',String(o));}});
}})();
</script>'''

def page(filename, title, description, body, full=True):
    """full=True: 실제 배포용(완전한 HTML). full=False: 미리보기용(문서 틀 없이)."""
    page_title = CLINIC["name"] if filename == "index.html" else f'{title} | {CLINIC["name"]}'
    meta = (f'<title>{page_title}</title>'
            f'<meta name="description" content="{description}">'
            f'<meta property="og:title" content="{page_title}">'
            f'<meta property="og:description" content="{description}">'
            f'<meta property="og:image" content="{CLINIC["domain"]}/assets/img/doctors-banner-800.jpg">'
            f'<link rel="icon" href="assets/img/favicon.png"><link rel="canonical" href="{CLINIC["domain"]}/{"" if filename == "index.html" else filename}">'
            f'{HEAD_FONTS}<link rel="stylesheet" href="assets/style.css">')
    content = f'{header(filename)}\n<main>\n{body}\n</main>\n{footer()}'
    if not full:
        return f'{meta}\n{content}\n'
    return (f'<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{meta}\n</head>\n<body>\n{content}\n</body>\n</html>\n')

def page_hero(eyebrow, title, lead, subnav=None):
    sub = ""
    if subnav:
        sub = '<div class="subnav"><div class="wrap">' + "".join(
            f'<a href="#{a}">{l}</a>' for a, l in subnav) + "</div></div>"
    return f'''<section class="page-hero"><div class="wrap">
  <div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{lead}</p>
</div></section>{sub}'''

def section_head(eyebrow, title, lead=""):
    p = f"<p>{lead}</p>" if lead else ""
    return f'<div class="section-head"><div class="eyebrow">{eyebrow}</div><h2>{title}</h2>{p}</div>'

# ── 의료진 ───────────────────────────────────────────────────────────
DOCTORS = [
    {
        "id": "kimyw", "name": "김용욱", "role": "대표원장", "room": "제1진료실",
        "spec": "내과 전문의", "photo": "assets/img/doctor-kimyw.jpg",
        "career": [], "societies": [], "awards": [],
    },
    {
        "id": "kimjw", "name": "김지우", "role": "원장", "room": "제2진료실",
        "spec": "내과 전문의 · 소화기내시경 세부전문의", "photo": "assets/img/doctor-kimjw.jpg",
        "career": [
            "연세대학교 의과대학 졸업",
            "연세대학교 신촌세브란스병원 인턴 수료",
            "연세대학교 신촌세브란스병원 레지던트 수료",
            "연세대학교 신촌세브란스병원 소화기내과 전임의 수료",
            "연세대학교 의과대학 내과학교실 의학 석사/박사 수료",
            "소화기내시경 세부전문의",
            "대한간학회 복부초음파 세부전문의",
            "유방촬영용장치 운용인력",
        ],
        "societies": [
            "대한내과학회 정회원", "대한소화기내시경학회 정회원", "대한장연구학회 평생회원",
            "대한소화기학회 평생회원", "대한간학회 정회원", "대한고혈압학회 평생회원",
            "대한당뇨병학회 정회원", "대한내분비학회 정회원", "대한임상순환기학회 평생회원",
            "대한임상초음파학회 평생회원", "한국심초음파학회 평생회원",
        ],
        "awards": [
            "대한소화기학회 우수논문상 수상 (2019)",
            "Yoshikazu Uchida lab, School of Medicine, University of California, San Francisco (UCSF) 연구 (2016)",
        ],
    },
]

def doctor_card(d, full=True):
    detail = ""
    if full:
        blocks = [("약력", d["career"]), ("학회 활동", d["societies"]), ("수상 및 연구", d["awards"])]
        detail = "".join(f'<h4>{t}</h4><ul>{li(xs)}</ul>' for t, xs in blocks if xs)
    return f'''<article class="doctor" id="dr-{d["id"]}">
  <img class="doc-photo" src="{d["photo"]}" alt="{d["role"]} {d["name"]}" width="640" height="640" loading="lazy">
  <div class="doc-body">
    <div class="role">{d["room"]} · {d["role"]}</div>
    <h3>{d["name"]} <small>{d["role"]}</small></h3>
    <p class="spec">{d["spec"]}</p>
    {detail}
  </div>
</article>'''

# ── 내부시설 ─────────────────────────────────────────────────────────
ROOMS = [
    ("room-reception", "접수데스크"), ("room-xray", "X-ray실"), ("room-iv", "수액실"),
    ("room-lab", "기초 검사실"), ("room-recovery", "회복실"), ("room-endoscopy", "내시경실"),
    ("room-ultrasound", "초음파실"),
]

def gallery():
    return "".join(
        f'<figure><img src="assets/img/{f}.jpg" alt="내마음내과 {n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
        for f, n in ROOMS)

# ── 진료과목 ─────────────────────────────────────────────────────────
SERVICES = [
    ("general", "steth", "일반 내과", "감기, 장염, 소화불량 등 일상의 급성 질환을 진료합니다."),
    ("chronic", "pulse", "만성질환 관리", "고혈압, 당뇨병, 고지혈증을 꾸준히 관리합니다."),
    ("endoscopy", "scope", "소화기 내시경", "소화기내시경 세부전문의가 내시경 검사를 합니다."),
    ("ultrasound", "wave", "초음파 검사", "복부, 갑상선, 경동맥, 심장, 유방 초음파 검사를 합니다."),
    ("thyroid", "thyroid", "갑상선 질환", "갑상선 기능 검사, 초음파, 세침흡인세포검사(FNA)로 진단하고 관리합니다."),
    ("checkup", "clipboard", "건강검진", "국가건강검진과 보험사 지정 검진을 받으실 수 있습니다."),
    ("vaccine", "syringe", "예방접종", "독감, 폐렴구균, 대상포진, 간염 등 성인 예방접종을 합니다."),
    ("iv", "drop", "수액 치료", "의료진 상담 후 필요한 경우 수액을 처방합니다."),
]

CLINIC_DETAIL = {
    "general": (["감기, 독감, 몸살", "급성 장염, 복통, 소화불량", "두통, 어지럼증", "피로 등 원인을 알기 어려운 증상"],
                "갑작스럽게 생긴 증상은 원인을 확인하고 필요한 검사와 치료를 안내합니다."),
    "chronic": (["고혈압", "당뇨병", "고지혈증(이상지질혈증)", "지방간"],
                "만성질환은 꾸준한 관리가 중요합니다. 정기적인 검사로 수치를 확인하고, 생활습관과 약 복용을 함께 점검합니다."),
    "endoscopy": (["위내시경", "진정(수면) 내시경", "내시경 후 회복실 이용"],
                  "소화기내시경 세부전문의가 내시경 검사를 하며, 진정 내시경 후에는 회복실에서 충분히 쉬신 뒤 귀가하실 수 있습니다."),
    "ultrasound": (["상복부: 간암, 간경화, 지방간, 췌장암, 담석 등", "갑상선: 갑상선암, 갑상선결절, 갑상선염 등",
                    "경동맥: 뇌졸중, 동맥경화, 심근경색 등", "심장: 심근경색, 심장부정맥, 심장질환 등",
                    "유방: 유방암, 유방종양, 물혹 등"],
                   "Philips Affiniti 70 초음파 장비로 검사합니다. 여성 전문의가 유방·심장 초음파 검사를 진행합니다."),
    "thyroid": (["갑상선 기능 항진증·저하증", "갑상선 결절 경과 관찰", "갑상선 초음파 검사", "갑상선 세침흡인세포검사(FNA)"],
                "피로, 체중 변화, 두근거림 같은 증상이 갑상선과 관련이 있을 수 있습니다."),
    "checkup": (["국가건강검진", "삼성생명 검진 지정기관", "고려대학교병원 위탁기관"],
                "자세한 내용은 건강검진센터 메뉴에서 확인하세요."),
    "vaccine": (["인플루엔자(독감)", "폐렴구균", "대상포진(싱그릭스)", "자궁경부암(가다실9)", "A형·B형 간염", "Td·Tdap, MMR, 수두, 수막구균(멘비오)"],
                "접종 비용은 이용안내의 비급여 진료비에서 확인하실 수 있습니다."),
    "iv": (["탈수, 장염 후 회복", "피로 회복"],
           "의료진 상담 후 필요한 경우에만 처방하며, 별도의 수액실에서 편하게 맞으실 수 있습니다."),
}

# 진료과목별 추가 설명 (진료과목 페이지에만 표시)
CLINIC_EXTRA = {
    "thyroid": """<div class="sub-blocks">
  <div class="sub-block">
    <span class="tag">결절과 암을 확인하는</span>
    <h3>갑상선 초음파 검사</h3>
    <p>손으로 만져지지 않는 결절이 있는지 확인하고, 갑상선암 고위험군을 선별하거나 갑상선암 수술 후 재발·전이 여부를 살펴볼 때 시행하는 검사입니다.</p>
    <p>결절이 있는 경우 물혹(낭성)인지 단단한 혹(고형성)인지 구분하는 데에도 쓰입니다.</p>
  </div>
  <div class="sub-block">
    <span class="tag">결절을 더 정확히 확인하는</span>
    <h3>갑상선 세침흡인세포검사(FNA)</h3>
    <p>초음파에서 결절이 발견되거나 악성이 의심될 때, 아주 가는 바늘로 결절에서 세포를 채취해 검사합니다.</p>
    <p>결절이 암일 가능성을 평가하는 표준 검사이며, 별도의 준비 없이 짧은 시간 안에 진행할 수 있습니다.</p>
  </div>
</div>""",
}

def svc_cards():
    return "".join(
        f'<a class="svc" href="clinic.html#{k}"><span class="ico">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></a>'
        for k, ic, t, d in SERVICES)

# ── 비급여 진료비 ────────────────────────────────────────────────────
FEES_EXAM = [
    ("독감검사", "30,000"), ("동맥경화도검사", "30,000"), ("진정내시경 관리료 2", "40,000"),
    ("진정내시경 관리료 3", "90,000"), ("갑상선초음파", "50,000"), ("경동맥초음파", "50,000"),
    ("대상포진 - 싱그릭스", "250,000"), ("가다실9", "210,000"), ("독감주사", "30,000"),
    ("Td", "30,000"), ("Tdap", "50,000"), ("폐렴구균", "130,000"), ("MMR", "30,000"),
    ("A형간염 주사", "70,000"), ("B형간염 주사", "35,000"), ("수두", "40,000"), ("멘비오", "160,000"),
]
FEES_DOCS = [
    ("일반진단서", "20,000"), ("건강진단서", "20,000"), ("근로능력평가용 진단서", "10,000"),
    ("사망진단서", "10,000"), ("장애 정도 심사용 진단서 - 신체적장애", "15,000"),
    ("장애 정도 심사용 진단서 - 정신적장애", "40,000"), ("후유장애진단서", "100,000"),
    ("병무용 진단서", "20,000"), ("국민연금 장애심사용 진단서", "15,000"),
    ("상해진단서 (3주 미만)", "100,000"), ("상해진단서 (3주 이상)", "150,000"),
    ("영문 일반진단서", "20,000"), ("통원확인서", "3,000"), ("진료확인서", "3,000"),
    ("채용 신체검사서 - 공무원", "30,000"), ("채용 신체검사서 - 일반", "30,000"),
    ("식품위생 분야 종사자 건강진단결과서 (구 보건증)", "25,000"),
    ("진료기록사본 (1~5매)", "1매당 1,000"), ("진료기록사본 (6매 이상)", "1매당 100"),
    ("진료기록(영상) - CD", "10,000"), ("제증명서 사본", "10,000"),
]

def fee_table(rows, col):
    body = "".join(f'<tr><td>{n}</td><td class="num">{p}</td></tr>' for n, p in rows)
    return (f'<div class="table-wrap"><table class="table"><thead><tr><th>항목</th>'
            f'<th class="num">{col}</th></tr></thead><tbody>{body}</tbody></table></div>')

# ── 공지사항: 새 글은 맨 위에 추가하세요 ──────────────────────────────
def notice_female_doctor():
    d = DOCTORS[1]
    return f'''<p>안녕하세요, 내마음내과입니다.</p>
<p>내마음내과 <strong>제2진료실</strong>에서 여성 전문의 <strong>김지우 원장님</strong>이 진료합니다.
여성 의료진에게 진료받기를 원하셨던 분들도 편하게 내원해 주세요.</p>
<figure class="post-figure"><img src="assets/img/notice-female-doctor.jpg" alt="여성 전문의 진료실시. 제2진료실 김지우 원장님 약력" width="768" height="1024"></figure>
<h2>김지우 원장 약력</h2><ul>{li(d["career"])}</ul>
<h2>학회 활동</h2><ul>{li(d["societies"])}</ul>
<h2>수상 및 연구</h2><ul>{li(d["awards"])}</ul>
<p>진료시간은 <a href="info.html#hours">이용안내</a>에서 확인하시거나 전화({CLINIC["phone"]})로 문의해 주세요.</p>'''

def notice_ultrasound():
    return f'''<p>내마음내과에 <strong>Philips Affiniti 70</strong> 초음파 장비를 도입하여, 여성 전문의 김지우 원장님이 유방·심장 초음파 검사를 진행합니다.</p>
<figure class="post-figure"><img src="assets/img/notice-ultrasound.jpg" alt="여성전문의 유방·심장 초음파 검사, Philips Affiniti 70 도입" width="556" height="556"></figure>
<h2>장비 소개</h2>
<p>대학병원에서도 사용하는 초음파 진단장비로 복부, 심장, 유방, 갑상선, 경동맥, 근골격계 등 여러 분야의 검사에 쓰입니다.</p>
<p>미세혈류감지 기능(Micro CPA)과 빔포밍(Beam forming), 퓨어웨이브(PureWave) 기술을 갖추고 있어 영상화가 까다로운 비만이나 간질환 환자분도 선명한 영상을 얻을 수 있습니다.</p>
<h2>초음파 검사의 종류</h2>
<ul>{li(CLINIC_DETAIL["ultrasound"][0])}</ul>
<p>검사 예약과 비용은 전화({CLINIC["phone"]})로 문의해 주세요.</p>'''

def notice_obesity():
    return f'''<p>안녕하세요, 내마음내과입니다.</p>
<p>체중 관리가 필요하신 분들을 위해 <strong>비만 진료 상담</strong>을 하고 있으며, 위고비, 마운자로 등 <strong>비만 약물치료</strong> 상담도 받으실 수 있습니다.</p>
<h2>진료 내용</h2>
<ul>
  <li>체성분 검사와 혈액검사로 현재 상태 확인</li>
  <li>고혈압, 당뇨병, 고지혈증, 지방간 등 동반 질환 확인</li>
  <li>식사와 운동 등 생활습관 상담</li>
  <li>전문의 진료 후 필요한 경우 약물치료</li>
</ul>
<h2>비만 약물치료 안내</h2>
<ul>
  <li><strong>위고비(성분명 세마글루타이드)</strong>: GLP-1 계열 주사제로, 주 1회 투여합니다.</li>
  <li><strong>마운자로(성분명 티르제파타이드)</strong>: GLP-1과 GIP 두 가지 호르몬에 작용하는 주사제로, 주 1회 투여합니다.</li>
</ul>
<p>두 약물 모두 전문의약품으로, 의사의 진료와 처방이 있어야 사용할 수 있습니다. 체질량지수(BMI)와 동반 질환 등 처방 기준에 맞는지 확인한 뒤 처방하며, 메스꺼움, 구토, 설사, 변비 등의 부작용이 나타날 수 있습니다. 치료 효과와 부작용은 개인에 따라 다르므로 진료 시 충분히 상담해 주세요.</p>
<p>상담 문의는 전화({CLINIC["phone"]})로 해 주세요.</p>'''

NOTICES = [
    # (파일명, 날짜, 제목, 요약, 썸네일, 본문 함수)
    ("notice-1.html", "2026-10-02", "여성 전문의 진료실시",
     "제2진료실에서 여성 전문의 김지우 원장님이 진료합니다.", "notice-female-doctor.jpg", notice_female_doctor),
    ("notice-3.html", "2026-10-02", "비만 진료 상담 안내",
     "위고비, 마운자로 등 비만 약물치료 상담을 받으실 수 있습니다.", None, notice_obesity),
    ("notice-2.html", "2026-10-02", "여성전문의 유방·심장 초음파 검사",
     "Philips Affiniti 70 초음파 장비로 유방·심장 초음파 검사를 합니다.", "notice-ultrasound.jpg", notice_ultrasound),
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

# 홈 화면 영상 (YouTube)
VIDEO_ID = "fgRDbwQsFFI"
VIDEO_TITLE = "당뇨병, 고혈압, 이상지질혈증 왜 항상 같이 올까? 올바른 관리법 총 정리 | 내과 전문의 김지우 원장"

# ── 페이지 본문 ──────────────────────────────────────────────────────
def home():
    docs = "".join(f'''<a class="doc-teaser" href="about.html#dr-{d["id"]}">
  <img src="{d["photo"]}" alt="{d["role"]} {d["name"]}" width="640" height="640" loading="lazy">
  <span><span class="role">{d["room"]}</span><strong>{d["role"]} {d["name"]}</strong><span class="spec">{d["spec"]}</span></span>
</a>''' for d in DOCTORS)
    return f'''<section class="hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">{CLINIC["slogan"]}</div>
      <h1>내 마음을 듣는 진료,<br><em>내마음내과</em>입니다</h1>
      <p class="lead">내과 전문의 두 명이 진료하며, 여성 전문의 진료도 받으실 수 있습니다. 내시경, 초음파, 건강검진까지 한 곳에서 살펴드립니다.</p>
      <div class="badges">
        <span class="badge">{icon("shield")}삼성생명 검진 지정기관</span>
        <span class="badge">{icon("shield")}고려대학교병원 위탁기관</span>
      </div>
      <div class="hero-actions">
        <a class="btn primary" href="tel:{CLINIC["phone"]}">{icon("phone")}전화 문의 {CLINIC["phone"]}</a>
        <a class="btn ghost" href="info.html#hours">진료시간 보기</a>
      </div>
    </div>
    <figure class="hero-photo"><img src="assets/img/doctors-banner-800.jpg" srcset="assets/img/doctors-banner-800.jpg 800w, assets/img/doctors-banner.jpg 1254w" sizes="(max-width:860px) 360px, 440px" alt="내마음내과 대표원장 김용욱, 원장 김지우" width="800" height="800"></figure>
  </div>
</section>

<section class="quick"><div class="wrap"><div class="quick-grid">
  <div class="quick-card"><h3>{icon("clock")}진료시간</h3>{hours_table()}</div>
  <div class="quick-card"><h3>{icon("phone")}전화 상담</h3>
    <a class="big" href="tel:{CLINIC["phone"]}">{CLINIC["phone"]}</a>
    <p>진료와 검진 문의는 전화로 편하게 해 주세요.</p>
    <a class="more" href="info.html#fees">비급여 진료비 보기 →</a></div>
  <div class="quick-card"><h3>{icon("pin")}오시는 길</h3>
    <p>{CLINIC["building"]}</p><p>{CLINIC["transit"]}</p><p>{CLINIC["parking"]}</p>
    <a class="more" href="info.html#location">위치 자세히 보기 →</a></div>
</div></div></section>

<section class="section"><div class="wrap">
  {section_head("진료과목", "내마음내과 진료 안내", "일상의 급성 질환부터 만성질환 관리, 내시경과 초음파 검사, 건강검진까지 진료합니다.")}
  <div class="svc-grid">{svc_cards()}</div>
</div></section>

<section class="section alt"><div class="wrap">
  {section_head("의료진", "내과 전문의가 진료합니다")}
  <div class="doc-teasers">{docs}</div>
</div></section>

<section class="section"><div class="wrap">
  {section_head("건강 영상", "김지우 원장이 알려드리는 만성질환 관리", "당뇨병, 고혈압, 이상지질혈증은 왜 함께 올까요? 올바른 관리법을 영상으로 확인해 보세요.")}
  <div class="video">
    <iframe src="https://www.youtube-nocookie.com/embed/{VIDEO_ID}" title="{VIDEO_TITLE}" loading="lazy"
      allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>
  <p class="video-src">출처: 건강의학전문채널 하이닥 · <a href="https://youtu.be/{VIDEO_ID}" target="_blank" rel="noopener">YouTube에서 보기</a></p>
</div></section>

<section class="section alt"><div class="wrap">
  <div class="section-head row"><div><div class="eyebrow">공지사항</div><h2>내마음내과 소식</h2></div>
    <a class="link-more" href="notice.html">전체 보기 →</a></div>
  <ul class="notice-list compact">{notice_items(4, compact=True)}</ul>
</div></section>

<section class="section"><div class="wrap split">
  <div>
    {section_head("건강검진센터", "가까운 곳에서 받는 정기 검진")}
    <ul class="checklist">
      <li>국가건강검진</li><li>삼성생명 검진 지정기관</li><li>고려대학교병원 위탁기관</li>
      <li>내시경실, 초음파실, X-ray실, 회복실 완비</li>
    </ul>
    <div class="hero-actions"><a class="btn primary" href="checkup.html">건강검진 안내</a></div>
  </div>
  <div class="panel">
    <h3>검진 전 확인해 주세요</h3>
    <ul class="checklist">
      <li>검사 전날 저녁 9시 이후 금식(물은 소량 가능)</li>
      <li>신분증 지참</li>
      <li>복용 중인 약이 있으면 미리 알려 주세요</li>
    </ul>
  </div>
</div></section>
'''

GREETING = [
    "안녕하세요.",
    "내마음내과를 방문해 주셔서 감사합니다.",
    "좋은 시설과 최선의 진료로 환자 한 분 한 분의 만족을 넘어선 행복의료 서비스를 제공하도록 노력하겠습니다. 따뜻한 마음과 정성을 다해 진료하겠습니다.",
    "감사합니다.",
]

def about():
    paras = "".join(f"<p>{p}</p>" for p in GREETING)
    return page_hero("병원소개", "병원 소개", CLINIC["slogan"],
                     [("greeting", "인사말"), ("doctors", "의료진 안내"), ("facility", "내부시설")]) + f'''
<section class="section anchor" id="greeting"><div class="wrap">
  {section_head("인사말", "내 마음을 듣는 진료를 하겠습니다")}
  <div class="greeting">{paras}<p class="sign">대표원장 {CLINIC["owner"]}</p></div>
</div></section>

<section class="section alt anchor" id="doctors"><div class="wrap">
  {section_head("의료진 안내", "내마음내과 의료진")}
  <div class="doctors">{"".join(doctor_card(d) for d in DOCTORS)}</div>
</div></section>

<section class="section anchor" id="facility"><div class="wrap">
  {section_head("내부시설", "편안하고 깨끗한 진료 공간")}
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
    return page_hero("진료과목", "진료과목 안내", "급성 질환부터 만성질환 관리, 내시경과 초음파 검사, 건강검진까지 진료합니다.",
                     [(k, t) for k, _, t, _ in SERVICES]) + f'''
<section class="section"><div class="wrap">{blocks}
  <p class="notice" style="margin-top:24px">진료 내용과 치료 결과는 개인의 상태에 따라 다를 수 있습니다. 증상이 있으시면 내원하여 의료진과 상담해 주세요.</p>
</div></section>
'''

def checkup():
    return page_hero("건강검진센터", "건강검진 안내", "가까운 곳에서 정기 검진을 받고, 결과를 전문의와 함께 확인하세요.",
                     [("types", "검진 종류"), ("equipment", "검진 시설"), ("prepare", "검진 전 준비사항")]) + f'''
<section class="section anchor" id="types"><div class="wrap">
  <div class="detail">
    <div><span class="tag">국민건강보험공단</span><h2>국가건강검진</h2></div>
    <div><p>국민건강보험공단에서 안내받은 건강검진을 받으실 수 있습니다. 검진 대상 여부는 공단 홈페이지나 앱에서 확인하실 수 있습니다.</p></div>
  </div>
  <div class="detail">
    <div><span class="tag">지정기관</span><h2>보험사 지정 검진</h2></div>
    <div><p>내마음내과는 삼성생명 검진 지정기관입니다. 보험 가입이나 심사에 필요한 검진을 받으실 수 있습니다.</p></div>
  </div>
  <div class="detail">
    <div><span class="tag">위탁기관</span><h2>고려대학교병원 위탁기관</h2></div>
    <div><p>내마음내과는 고려대학교병원 위탁기관입니다. 자세한 내용은 전화로 문의해 주세요.</p></div>
  </div>
  <div class="detail">
    <div><span class="tag">추가 검사</span><h2>내시경 · 초음파</h2></div>
    <div><p>필요에 따라 위내시경(진정 내시경 가능)과 복부, 갑상선, 경동맥, 심장, 유방 초음파 검사를 함께 받으실 수 있습니다.</p>
      <p><a href="clinic.html#ultrasound" style="color:var(--blue);font-weight:600">초음파 검사 자세히 보기 →</a></p></div>
  </div>
</div></section>

<section class="section alt anchor" id="equipment"><div class="wrap">
  {section_head("검진 시설", "검사부터 회복까지 한 층에서")}
  <div class="gallery">{gallery()}</div>
</div></section>

<section class="section anchor" id="prepare"><div class="wrap split">
  <div>
    {section_head("검진 전 준비사항", "검진 전에 꼭 확인해 주세요")}
    <ul class="checklist">
      <li>검사 전날 저녁 9시 이후 금식해 주세요. 물은 소량 드셔도 됩니다.</li>
      <li>신분증을 꼭 지참해 주세요.</li>
      <li>혈압약 등 복용 중인 약은 미리 의료진에게 알려 주세요.</li>
      <li>당뇨약과 인슐린은 검사 당일 아침에 투약하지 말고 의료진과 상의해 주세요.</li>
      <li>진정 내시경을 받으시는 날은 운전을 하지 마세요.</li>
    </ul>
  </div>
  <div class="panel">
    <h3>검진 문의</h3>
    <p style="color:var(--muted)">평일 08:00부터 검진하실 수 있습니다. 예약과 가능 항목은 전화로 확인해 주세요.</p>
    <div class="hero-actions"><a class="btn primary" href="tel:{CLINIC["phone"]}">{icon("phone")}{CLINIC["phone"]}</a></div>
  </div>
</div></section>
'''

def info():
    q = CLINIC["map_query"]
    return page_hero("이용안내", "이용안내", "진료시간, 오시는 길, 비급여 진료비를 안내합니다.",
                     [("hours", "진료시간"), ("location", "오시는 길"), ("fees", "비급여 진료비"), ("docs", "제증명 발급")]) + f'''
<section class="section anchor" id="hours"><div class="wrap split">
  {section_head("진료시간", "진료시간 안내", "일요일과 공휴일은 휴진합니다. 임시 휴진은 공지사항으로 알려드립니다.")}
  <div class="panel">{hours_table()}</div>
</div></section>

<section class="section alt anchor" id="location"><div class="wrap split">
  <div>
    {section_head("오시는 길", CLINIC["address"])}
    <ul class="info-list">
      <li>{icon("pin")}<span><strong>위치</strong>{CLINIC["building"]}</span></li>
      <li>{icon("train")}<span><strong>지하철</strong>{CLINIC["transit"]}</span></li>
      <li>{icon("car")}<span><strong>주차</strong>{CLINIC["parking"]}</span></li>
      <li>{icon("phone")}<span><strong>전화</strong>{CLINIC["phone"]}</span></li>
    </ul>
    <div class="map-links">
      <a class="btn primary" href="https://map.naver.com/p/search/{q}" target="_blank" rel="noopener">{icon("map")}네이버 지도</a>
      <a class="btn ghost" href="https://map.kakao.com/?q={q}" target="_blank" rel="noopener">카카오맵</a>
    </div>
  </div>
  <figure class="framed"><img src="assets/img/room-reception.jpg" alt="내마음내과 접수데스크" loading="lazy"></figure>
</div></section>

<section class="section anchor" id="fees"><div class="wrap">
  {section_head("비급여 진료비", "비급여 진료비용 안내", "의료법 제45조에 따라 비급여 진료비용을 안내합니다. (단위: 원)")}
  <div class="fees">
    <div><h3 class="fee-title">접종 및 검사</h3>{fee_table(FEES_EXAM, "금액")}</div>
    <div><h3 class="fee-title">제증명 서류</h3>{fee_table(FEES_DOCS, "상한금액")}</div>
  </div>
</div></section>

<section class="section alt anchor" id="docs"><div class="wrap">
  {section_head("제증명 발급", "서류 발급 안내")}
  <div class="notice"><strong>본인 방문 시</strong> 신분증을 지참해 주세요. <strong>대리 발급 시</strong> 환자 신분증 사본, 대리인 신분증, 가족관계증명서 또는 위임장이 필요합니다.</div>
</div></section>
'''

def notice_list():
    return page_hero("공지사항", "공지사항", "진료 일정 변경과 새로운 소식을 알려드립니다.") + f'''
<section class="section"><div class="wrap"><ul class="notice-list">{notice_items()}</ul></div></section>
'''

def notice_post(d, t, body_fn):
    return f'''<section class="page-hero"><div class="wrap">
  <div class="eyebrow"><a href="notice.html" style="color:inherit">공지사항</a></div><h1>{t}</h1>
  <p><time datetime="{d}">{d.replace("-", ".")}</time></p>
</div></section>
<section class="section"><div class="wrap"><article class="post">{body_fn()}
  <p class="post-back"><a class="btn ghost" href="notice.html">목록으로</a></p>
</article></div></section>
'''

PAGES = [
    ("index.html", "홈", f'{CLINIC["name"]}: {CLINIC["slogan"]}. 안산 중앙역 내과 전문의 진료, 여성 전문의, 내시경·초음파, 건강검진.', home),
    ("about.html", "병원소개", "내마음내과 인사말, 의료진 안내, 내부시설.", about),
    ("clinic.html", "진료과목", "일반 내과, 만성질환, 소화기 내시경, 초음파, 갑상선, 건강검진, 예방접종 안내.", clinic),
    ("checkup.html", "건강검진센터", "국가건강검진, 삼성생명 지정 검진, 검진 시설과 준비사항 안내.", checkup),
    ("info.html", "이용안내", "진료시간, 오시는 길, 주차, 비급여 진료비, 제증명 발급 안내.", info),
    ("notice.html", "공지사항", "내마음내과 공지사항과 새로운 소식.", notice_list),
] + [(fn, t, sm, (lambda d=d, t=t, b=b: notice_post(d, t, b))) for fn, d, t, sm, _, b in NOTICES]

if __name__ == "__main__":
    import sys
    preview_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    for fn, title, desc, body_fn in PAGES:
        (ROOT / fn).write_text(page(fn, title, desc, body_fn()), encoding="utf-8")
        if preview_dir and fn == "index.html":
            preview_dir.mkdir(parents=True, exist_ok=True)
            (preview_dir / fn).write_text(page(fn, title, desc, body_fn(), full=False), encoding="utf-8")
    print("built", [p[0] for p in PAGES])
