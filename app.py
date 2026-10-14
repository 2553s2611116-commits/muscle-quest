import streamlit as st
from datetime import date, timedelta
from collections import Counter
import pandas as pd
import json
import uuid

st.set_page_config(page_title="MUSCLE QUEST", page_icon="⚔️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp {background:#080a0c;color:#f4f6f8}
.block-container {max-width:1100px;padding:1rem 1rem 4rem}
.quest-card {background:linear-gradient(135deg,#171d20,#0d1012);border:1px solid #2a3438;border-radius:18px;padding:20px;margin-bottom:12px}
.quest-label {color:#b5ff7d;font-size:11px;font-weight:800;letter-spacing:.16em}
.quest-number {font-size:30px;font-weight:800;margin:5px 0}
.muted {color:#a1abb1;font-size:13px}
.tag {display:inline-block;padding:4px 8px;border-radius:999px;background:#1d2920;color:#c3ff98;font-size:12px;margin:2px 3px 2px 0}
div.stButton>button {border-radius:12px;min-height:42px;font-weight:650}
div.stButton>button[kind="primary"] {background:#b5ff7d;color:#10140d;border:0}
div[data-testid="stProgressBar"]>div>div {background:#b5ff7d}
[data-testid="stMetric"] {background:#111619;padding:12px;border:1px solid #263034;border-radius:14px}
hr {border-color:#283034}
@media(max-width:600px){.block-container{padding:.7rem .6rem 4rem}h1{font-size:1.8rem!important}}
</style>
""", unsafe_allow_html=True)

EXERCISES = [
{"name":"푸시업","type":"맨몸","body":"가슴","main":["대흉근"],"sub":["삼두근","전면 삼각근"],"level":"초급","equipment":"없음","form":"머리부터 골반까지 몸통을 일직선으로 유지한다. 팔꿈치를 편안한 각도로 굽히고 반동 없이 밀어 올린다.","tip":"가슴뿐 아니라 삼두근과 어깨 앞쪽 근육도 함께 참여한다.","related":["인클라인 푸시업","벤치 프레스","체스트 프레스"]},
{"name":"인클라인 푸시업","type":"맨몸","body":"가슴","main":["대흉근"],"sub":["삼두근","전면 삼각근"],"level":"초급","equipment":"튼튼하고 미끄럽지 않은 지지대","form":"손을 안정적인 높은 지지대에 두고 몸통을 곧게 유지한다.","tip":"손을 높은 곳에 두면 일반 푸시업보다 부담을 줄일 수 있다.","related":["푸시업","체스트 프레스"]},
{"name":"벤치 프레스","type":"기구","body":"가슴","main":["대흉근"],"sub":["삼두근","전면 삼각근"],"level":"중급","equipment":"벤치, 바벨","form":"발을 안정적으로 두고 바를 통제하며 내린다. 처음에는 가벼운 중량과 보조자의 도움을 고려한다.","tip":"가슴과 함께 삼두근, 어깨 앞쪽 근육도 사용되는 복합 운동이다.","related":["푸시업","체스트 프레스"]},
{"name":"체스트 프레스","type":"기구","body":"가슴","main":["대흉근"],"sub":["삼두근","전면 삼각근"],"level":"초급","equipment":"체스트 프레스 머신","form":"좌석을 조절해 손잡이가 가슴 중간 부근에 오도록 하고 천천히 민다.","tip":"머신은 움직임 경로가 비교적 일정하지만 좌석 조절과 통제된 동작은 중요하다.","related":["벤치 프레스","푸시업"]},
{"name":"덤벨 플라이","type":"기구","body":"가슴","main":["대흉근"],"sub":["전면 삼각근"],"level":"중급","equipment":"덤벨, 벤치","form":"팔꿈치를 약간 굽힌 상태를 유지하고 어깨가 불편하지 않은 범위에서 움직인다.","tip":"팔을 모으는 동작에 가슴 근육이 관여한다. 과도하게 깊게 내리지 않는다.","related":["체스트 프레스","푸시업"]},
{"name":"랫 풀다운","type":"기구","body":"등","main":["광배근"],"sub":["이두근","능형근"],"level":"초급","equipment":"랫 풀다운 머신","form":"몸통을 과하게 젖히지 말고 바를 윗가슴 방향으로 당긴다.","tip":"광배근은 팔을 몸통 쪽으로 당기는 움직임에 관여한다.","related":["시티드 로우","풀업"]},
{"name":"시티드 로우","type":"기구","body":"등","main":["광배근","능형근"],"sub":["이두근","승모근"],"level":"초급","equipment":"시티드 로우 머신","form":"허리를 안정적으로 유지하고 팔꿈치를 몸통 뒤쪽으로 당긴다.","tip":"등을 당기는 운동에는 어깨뼈를 움직이는 근육도 함께 참여한다.","related":["랫 풀다운","풀업"]},
{"name":"풀업","type":"맨몸","body":"등","main":["광배근"],"sub":["이두근","능형근"],"level":"상급","equipment":"풀업 바","form":"반동을 최소화하고 통제 가능한 범위에서 몸을 당긴다. 필요하면 보조 밴드를 사용한다.","tip":"풀업은 등과 팔의 당기는 힘이 함께 필요한 복합 운동이다.","related":["랫 풀다운","시티드 로우"]},
{"name":"원암 덤벨 로우","type":"기구","body":"등","main":["광배근","능형근"],"sub":["이두근","승모근"],"level":"중급","equipment":"덤벨, 안정적인 벤치","form":"몸통을 안정적으로 지지하고 팔꿈치를 엉덩이 방향으로 당긴다.","tip":"좌우를 따로 수행할 수 있어 양쪽 움직임을 확인하기 좋다.","related":["시티드 로우","랫 풀다운"]},
{"name":"숄더 프레스","type":"기구","body":"어깨","main":["삼각근"],"sub":["삼두근"],"level":"중급","equipment":"숄더 프레스 머신 또는 덤벨","form":"허리를 과하게 꺾지 말고 통제 가능한 범위에서 밀어 올린다.","tip":"삼각근은 앞·옆·뒤 부분으로 나뉘며 동작에 따라 기여도가 달라진다.","related":["사이드 레터럴 레이즈","리어 델트 플라이"]},
{"name":"사이드 레터럴 레이즈","type":"기구","body":"어깨","main":["측면 삼각근"],"sub":["극상근"],"level":"초급","equipment":"덤벨","form":"반동을 줄이고 가벼운 중량으로 팔을 통제하며 들어 올린다.","tip":"측면 삼각근은 팔을 옆으로 들어 올리는 동작에 관여한다.","related":["숄더 프레스","리어 델트 플라이"]},
{"name":"리어 델트 플라이","type":"기구","body":"어깨","main":["후면 삼각근"],"sub":["능형근","승모근"],"level":"초급","equipment":"덤벨 또는 리어 델트 머신","form":"몸통을 안정시키고 팔을 옆뒤 방향으로 움직인다.","tip":"후면 삼각근은 팔을 뒤쪽으로 움직이는 동작에 관여한다.","related":["사이드 레터럴 레이즈","시티드 로우"]},
{"name":"바이셉 컬","type":"기구","body":"팔","main":["이두근"],"sub":["상완근","상완요골근"],"level":"초급","equipment":"덤벨","form":"팔꿈치를 크게 흔들지 않고 천천히 팔을 굽힌다.","tip":"이두근은 팔꿈치를 굽히고 아래팔을 회전하는 데 관여한다.","related":["해머 컬","랫 풀다운"]},
{"name":"해머 컬","type":"기구","body":"팔","main":["상완근","상완요골근"],"sub":["이두근"],"level":"초급","equipment":"덤벨","form":"손바닥이 서로 마주 보는 자세를 유지하고 반동을 줄인다.","tip":"중립 그립은 상완근과 아래팔 근육의 참여를 돕는다.","related":["바이셉 컬"]},
{"name":"트라이셉 푸시다운","type":"기구","body":"팔","main":["삼두근"],"sub":[],"level":"초급","equipment":"케이블 머신","form":"팔꿈치를 몸 가까이 두고 팔을 펴는 동작을 통제한다.","tip":"삼두근은 팔꿈치를 펴는 데 중요한 역할을 한다.","related":["푸시업","벤치 프레스"]},
{"name":"스쿼트","type":"맨몸","body":"하체","main":["대퇴사두근","둔근"],"sub":["햄스트링","내전근"],"level":"초급","equipment":"없음","form":"발바닥을 안정적으로 유지하고 통증 없는 범위에서 앉았다 일어난다.","tip":"스쿼트는 무릎과 엉덩관절이 함께 움직이는 복합 운동이다.","related":["레그 프레스","글루트 브리지","카프 레이즈"]},
{"name":"레그 프레스","type":"기구","body":"하체","main":["대퇴사두근","둔근"],"sub":["햄스트링"],"level":"초급","equipment":"레그 프레스 머신","form":"허리와 골반이 패드에서 뜨지 않는 범위에서 움직인다.","tip":"발 위치와 가동 범위에 따라 근육의 기여도가 달라질 수 있다.","related":["스쿼트","글루트 브리지"]},
{"name":"글루트 브리지","type":"맨몸","body":"하체","main":["둔근"],"sub":["햄스트링"],"level":"초급","equipment":"매트","form":"발을 바닥에 둔 채 골반을 들어 올리고 허리를 과하게 꺾지 않는다.","tip":"둔근은 엉덩관절을 펴는 동작에 관여한다.","related":["스쿼트","레그 프레스"]},
{"name":"루마니안 데드리프트","type":"기구","body":"하체","main":["햄스트링","둔근"],"sub":["척추기립근"],"level":"중급","equipment":"덤벨 또는 바벨","form":"엉덩이를 뒤로 보내며 고관절을 접고 등을 안정적으로 유지한다. 가벼운 중량으로 자세부터 익힌다.","tip":"힙 힌지 동작으로 햄스트링과 둔근이 참여한다.","related":["글루트 브리지","스쿼트"]},
{"name":"카프 레이즈","type":"맨몸","body":"하체","main":["비복근","가자미근"],"sub":[],"level":"초급","equipment":"없음 또는 안정적인 지지대","form":"균형을 잡고 뒤꿈치를 천천히 올렸다 내린다.","tip":"종아리 근육은 발목을 아래로 미는 움직임에 관여한다.","related":["스쿼트","레그 프레스"]},
{"name":"플랭크","type":"맨몸","body":"코어","main":["복직근","복횡근"],"sub":["둔근"],"level":"초급","equipment":"매트","form":"머리부터 골반까지 정렬하고 호흡을 참지 않는다. 자세가 무너지기 전에 끝낸다.","tip":"코어 근육은 몸통을 안정시키는 데 관여한다.","related":["데드 버그","버드 독"]},
{"name":"데드 버그","type":"기능성","body":"코어","main":["복횡근"],"sub":["복직근"],"level":"초급","equipment":"매트","form":"허리와 골반의 안정성을 유지하며 팔다리를 천천히 움직인다.","tip":"천천히 팔다리를 움직이며 몸통을 안정시키는 연습에 활용된다.","related":["플랭크","버드 독"]},
{"name":"버드 독","type":"기능성","body":"코어","main":["척추기립근","복횡근"],"sub":["둔근"],"level":"초급","equipment":"매트","form":"네발 자세에서 반대쪽 팔과 다리를 뻗으며 골반이 기울지 않게 한다.","tip":"몸통 안정성과 팔다리 협응을 연습할 수 있다.","related":["데드 버그","플랭크"]},
{"name":"가벼운 관절 가동 운동","type":"재활·가동성","body":"전신","main":["관절 주변 근육"],"sub":[],"level":"초급","equipment":"없음","form":"반동 없이 편안한 범위에서 천천히 움직인다. 통증이 생기면 중단한다.","tip":"가동성 운동은 움직임 범위를 편안하게 사용하는 연습에 도움을 줄 수 있다.","related":["버드 독","데드 버그"]},
]

TIPS = [
{"title":"근육은 회복하는 동안에도 적응한다","category":"기초","body":"훈련뿐 아니라 휴식과 수면, 충분한 영양도 근육의 적응 과정에 중요하다.","fact":"운동량을 늘리는 것만큼 회복을 고려하는 것도 중요하다."},
{"title":"대흉근은 가슴 앞쪽에 있다","category":"가슴","body":"대흉근은 팔을 몸 안쪽으로 모으거나 앞으로 움직이는 동작에 관여한다.","fact":"푸시업과 벤치 프레스에서는 삼두근과 어깨 근육도 함께 작용한다."},
{"title":"광배근은 당기는 움직임에 관여한다","category":"등","body":"광배근은 팔을 몸통 쪽으로 당기거나 뒤로 움직이는 데 관여한다.","fact":"랫 풀다운과 풀업은 대표적인 당기기 운동이다."},
{"title":"삼각근은 세 부분으로 나뉜다","category":"어깨","body":"삼각근은 앞쪽, 가운데, 뒤쪽 부분으로 구분할 수 있다.","fact":"숄더 프레스와 레터럴 레이즈는 강조되는 움직임이 다르다."},
{"title":"이두근과 삼두근은 역할이 다르다","category":"팔","body":"이두근은 팔꿈치를 굽히는 데, 삼두근은 팔꿈치를 펴는 데 중요하다.","fact":"당기기 운동과 밀기 운동에서도 두 근육이 보조적으로 참여할 수 있다."},
{"title":"코어는 복근만을 뜻하지 않는다","category":"코어","body":"코어에는 복부와 등, 골반 주변의 여러 근육이 포함된다.","fact":"플랭크와 데드 버그는 몸통 안정성을 연습하는 데 활용된다."},
{"title":"대퇴사두근은 무릎 펴기에 중요하다","category":"하체","body":"허벅지 앞쪽의 대퇴사두근은 무릎을 펴는 동작에 중요한 역할을 한다.","fact":"스쿼트와 레그 프레스는 대퇴사두근을 사용하는 복합 운동이다."},
{"title":"둔근은 엉덩관절 움직임에 관여한다","category":"하체","body":"둔근은 엉덩관절을 펴거나 골반을 안정시키는 데 관여한다.","fact":"글루트 브리지와 스쿼트에서 둔근이 참여한다."},
{"title":"근육과 힘줄은 서로 다르다","category":"기초","body":"근육은 힘을 만들고 힘줄은 근육의 힘을 뼈에 전달한다.","fact":"통증을 참으며 운동하기보다 원인을 확인하는 것이 중요하다."},
{"title":"가동 범위는 통제할 수 있어야 한다","category":"기초","body":"운동 범위는 개인의 능력과 관절 상태에 맞춰 통제 가능한 수준으로 설정한다.","fact":"더 깊거나 크게 움직인다고 언제나 더 좋은 운동이 되는 것은 아니다."},
]

ACHIEVEMENTS = [
("first_save","첫 번째 장비","운동을 처음 저장하기",10),
("first_routine","초보 모험가","첫 루틴 만들기",15),
("first_session","첫 훈련 완료","루틴을 처음 완료하기",30),
("first_tip","지식의 조각","근육학 TIP 발견하기",5),
("five_tips","도서관 탐험가","TIP 5개 발견하기",20),
("five_sessions","꾸준한 모험가","훈련 5회 완료하기",40),
("five_saves","수집가","운동 5개 저장하기",20),
]

DEFAULT_DATA = {
    "xp": 0, "saved": [], "routines": [], "logs": [], "tips": [], "achievements": [],
    "routine_counter": 1, "log_counter": 1
}

if "mq_data" not in st.session_state:
    st.session_state.mq_data = json.loads(json.dumps(DEFAULT_DATA))
data = st.session_state.mq_data

def exercise(name):
    return next((e for e in EXERCISES if e["name"] == name), None)

def award(key):
    if key in data["achievements"]:
        return
    item = next((a for a in ACHIEVEMENTS if a[0] == key), None)
    if item:
        data["achievements"].append(key)
        data["xp"] += item[3]

def check_achievements():
    if data["saved"]: award("first_save")
    if len(data["saved"]) >= 5: award("five_saves")
    if data["routines"]: award("first_routine")
    if data["logs"]: award("first_session")
    if len(data["logs"]) >= 5: award("five_sessions")
    if data["tips"]: award("first_tip")
    if len(data["tips"]) >= 5: award("five_tips")

def level_info(xp):
    level, remain = 1, max(0, int(xp))
    while remain >= level * 100:
        remain -= level * 100
        level += 1
    return level, remain, level * 100

def muscle_counts(names):
    main, sub = Counter(), Counter()
    for name in names:
        ex = exercise(name)
        if ex:
            main.update(ex["main"])
            sub.update(ex["sub"])
    return main, sub

def suggestions(names):
    main, sub = muscle_counts(names)
    covered = set(main) | set(sub)
    choices = []
    for ex in EXERCISES:
        if ex["name"] in names: continue
        new = set(ex["main"]) - covered
        overlap = set(ex["main"]) & set(main)
        score = 2*len(new) - len(overlap)
        choices.append((score, len(new), ex, overlap))
    return sorted(choices, key=lambda x:(x[0],x[1]), reverse=True), main, sub

def export_data():
    return json.dumps(data, ensure_ascii=False, indent=2)

st.title("⚔️ MUSCLE QUEST")
st.caption("TRAIN · COLLECT · LEVEL UP")
st.caption("로그인 없이 사용하는 버전 · 데이터는 현재 브라우저 세션에 저장돼.")

with st.sidebar:
    st.markdown("## ⚔️ MUSCLE QUEST")
    page = st.radio("메뉴", ["길드 홈","운동 도감","루틴 모드","운동 저장소","운동 기록","근육 분석","근육학 TIP","업적","백업 / 복원"])
    st.divider()
    st.markdown("### 데이터 백업")
    st.download_button("내 기록 JSON 다운로드", data=export_data(), file_name="muscle_quest_backup.json", mime="application/json", use_container_width=True)
    uploaded = st.file_uploader("백업 파일 불러오기", type=["json"], key="restore_file")
    if uploaded is not None and st.button("백업 복원", use_container_width=True):
        try:
            loaded = json.load(uploaded)
            required = set(DEFAULT_DATA)
            if not required.issubset(loaded.keys()):
                st.error("이 앱에서 만든 백업 파일이 아닌 것 같아.")
            else:
                st.session_state.mq_data = loaded
                st.success("복원했어!")
                st.rerun()
        except Exception:
            st.error("파일을 읽지 못했어. 올바른 JSON 백업인지 확인해 줘.")

level, remain, needed = level_info(data["xp"])
st.markdown(f'<div class="quest-card"><div class="quest-label">PLAYER STATUS</div><div class="quest-number">LV. {level} ⚔️</div><div class="muted">{data["xp"]} TOTAL XP · {len(data["saved"])} SAVED · {len(data["tips"])}/{len(TIPS)} TIPS FOUND</div></div>', unsafe_allow_html=True)
st.progress(remain/needed, text=f"다음 레벨까지 {needed-remain} XP")

if page == "길드 홈":
    st.title("길드 홈")
    today = date.today().isoformat()
    c1,c2,c3 = st.columns(3)
    c1.metric("레벨", level); c2.metric("경험치", f"{data['xp']} XP"); c3.metric("훈련 기록", len(data["logs"]))
    st.subheader("📜 오늘의 퀘스트")
    quests = [
        ("운동 하나 저장하기",bool(data["saved"]),"운동 도감에서 마음에 드는 운동을 저장해 봐."),
        ("나만의 루틴 만들기",bool(data["routines"]),"루틴 모드에서 새 루틴을 만들어 봐."),
        ("지식 발견하기",bool(data["tips"]),"근육학 TIP을 열어 하나 발견해 봐."),
        ("오늘 훈련하기",any(x["date"]==today for x in data["logs"]),"루틴 모드에서 세트 기록을 저장해 봐.")
    ]
    for title,done,desc in quests:
        with st.container(border=True):
            st.write(("✅ " if done else "⬜ ")+title); st.caption(desc)
    st.subheader("🧭 추천 시작 경로")
    st.write("1. 운동 도감에서 운동을 저장한다.")
    st.write("2. 루틴 모드에서 운동을 조합한다.")
    st.write("3. 세트별 중량과 반복 횟수를 기록한다.")
    st.write("4. 근육 분석으로 루틴의 균형을 확인한다.")

elif page == "운동 도감":
    st.title("운동 도감")
    c1,c2=st.columns(2)
    bf=c1.selectbox("부위",["전체"]+sorted({e["body"] for e in EXERCISES}))
    tf=c2.selectbox("유형",["전체"]+sorted({e["type"] for e in EXERCISES}))
    q=st.text_input("운동 / 근육 검색",placeholder="예: 푸시업, 광배근")
    for ex in EXERCISES:
        searchable=" ".join([ex["name"],ex["body"],ex["type"],ex["equipment"],*ex["main"],*ex["sub"]])
        if bf!="전체" and ex["body"]!=bf: continue
        if tf!="전체" and ex["type"]!=tf: continue
        if q and q.lower() not in searchable.lower(): continue
        with st.container(border=True):
            st.markdown(f"### {ex['name']}")
            st.markdown(f'<span class="tag">{ex["body"]}</span><span class="tag">{ex["type"]}</span><span class="tag">{ex["level"]}</span>',unsafe_allow_html=True)
            st.write("**주요 근육:** "+", ".join(ex["main"]))
            st.write("**보조 근육:** "+(", ".join(ex["sub"]) or "별도 표시 없음"))
            with st.expander("자세 · 장비 · TIP"):
                st.write("**장비:** "+ex["equipment"]); st.write("**자세:** "+ex["form"]); st.info(ex["tip"]); st.write("관련 운동: "+", ".join(ex["related"]))
            a,b=st.columns(2)
            if a.button("★ 저장 해제" if ex["name"] in data["saved"] else "☆ 운동 저장",key="save_"+ex["name"],use_container_width=True):
                if ex["name"] in data["saved"]: data["saved"].remove(ex["name"])
                else: data["saved"].append(ex["name"])
                check_achievements(); st.rerun()
            if b.button("루틴에 추가",key="quick_"+ex["name"],use_container_width=True):
                st.session_state.quick_add=ex["name"]
                st.session_state.navigation="루틴 모드"
                st.rerun()

elif page == "루틴 모드":
    st.title("루틴 모드")
    with st.expander("＋ 새 루틴 만들기",expanded=not bool(data["routines"])):
        with st.form("create_routine"):
            name=st.text_input("루틴 이름",placeholder="예: 상체 A")
            category=st.selectbox("분류",["상체","하체","전신","가슴·삼두","등·이두","자유 구성"])
            create=st.form_submit_button("루틴 생성",type="primary")
        if create:
            if name.strip():
                data["routines"].append({"id":uuid.uuid4().hex,"name":name.strip(),"category":category,"items":[]})
                check_achievements(); st.success("루틴 생성 완료!"); st.rerun()
            else: st.warning("루틴 이름을 입력해 줘.")
    if not data["routines"]:
        st.info("아직 루틴이 없어. 위에서 첫 루틴을 만들어 봐.")
    else:
        routines={r["id"]:r for r in data["routines"]}
        rid=st.selectbox("편집할 루틴",list(routines),format_func=lambda x:f"{routines[x]['name']} · {routines[x]['category']}")
        routine=routines[rid]
        st.markdown(f"## ⚔️ {routine['name']}")
        with st.form("add_routine_exercise"):
            names=[e["name"] for e in EXERCISES]
            quick=st.session_state.get("quick_add")
            default=names.index(quick) if quick in names else 0
            exname=st.selectbox("추가할 운동",names,index=default)
            c1,c2=st.columns(2)
            sets=c1.number_input("목표 세트",1,20,3)
            reps=c2.number_input("목표 반복",1,100,10)
            add=st.form_submit_button("운동 추가",type="primary",use_container_width=True)
        if add:
            routine["items"].append({"id":uuid.uuid4().hex,"name":exname,"sets":int(sets),"reps":int(reps)})
            st.session_state.pop("quick_add",None); st.rerun()
        if routine["items"]:
            for idx,item in enumerate(list(routine["items"])):
                ex=exercise(item["name"])
                with st.container(border=True):
                    st.markdown(f"**{idx+1}. {item['name']}** · {item['sets']}세트 × {item['reps']}회")
                    st.caption("주요 근육: "+", ".join(ex["main"]))
                    a,b,c=st.columns(3)
                    if a.button("↑",key="up_"+item["id"],disabled=idx==0,use_container_width=True):
                        routine["items"][idx-1],routine["items"][idx]=routine["items"][idx],routine["items"][idx-1]; st.rerun()
                    if b.button("↓",key="down_"+item["id"],disabled=idx==len(routine["items"])-1,use_container_width=True):
                        routine["items"][idx+1],routine["items"][idx]=routine["items"][idx],routine["items"][idx+1]; st.rerun()
                    if c.button("삭제",key="delete_"+item["id"],use_container_width=True):
                        routine["items"]=[i for i in routine["items"] if i["id"]!=item["id"]]; st.rerun()
            names_in=[i["name"] for i in routine["items"]]
            main,_=muscle_counts(names_in)
            repeated={k:v for k,v in main.items() if v>=2}
            st.subheader("근육 겹침 미리보기")
            if repeated:
                for muscle,count in repeated.items(): st.write(f"- **{muscle}**: 주요 근육으로 {count}개 운동에 포함")
                st.caption("중복 자체가 나쁜 것은 아니야. 전체 세트와 회복 상태도 고려해.")
            else: st.success("주요 근육이 반복되는 부위가 많지 않아.")
            recs,_,_=suggestions(names_in)
            st.subheader("보완 운동 추천")
            for _,new_n,e,overlap in recs[:3]:
                st.write(f"**{e['name']}** · {e['body']} · 주요 근육: {', '.join(e['main'])}")
                if new_n: st.caption(f"새로운 주요 근육 {new_n}개를 포함할 수 있어.")
            st.divider(); st.subheader("오늘의 세트 기록")
            with st.form("workout_log"):
                log_date=st.date_input("훈련 날짜",value=date.today())
                vals=[]
                for item in routine["items"]:
                    st.markdown(f"**{item['name']}** · 목표 {item['sets']}세트 × {item['reps']}회")
                    for sn in range(1,item["sets"]+1):
                        c1,c2,c3=st.columns([1,1,1])
                        w=c1.number_input("중량 kg",0.0,1000.0,0.0,0.5,key=f"w_{rid}_{item['id']}_{sn}")
                        r=c2.number_input("실제 반복",0,300,item["reps"],key=f"r_{rid}_{item['id']}_{sn}")
                        done=c3.checkbox("완료",value=True,key=f"d_{rid}_{item['id']}_{sn}")
                        vals.append({"exercise":item["name"],"set":sn,"weight":float(w),"reps":int(r),"done":bool(done)})
                submit=st.form_submit_button("훈련 기록 저장 · +30 XP",type="primary",use_container_width=True)
            if submit:
                if not any(v["done"] for v in vals): st.warning("완료한 세트가 하나 이상 있어야 해.")
                else:
                    data["logs"].append({"id":uuid.uuid4().hex,"routine_id":rid,"routine_name":routine["name"],"date":log_date.isoformat(),"sets":vals,"xp":30})
                    data["xp"]+=30; check_achievements(); st.success("훈련 기록 저장 완료! +30 XP"); st.rerun()
        else: st.info("운동을 추가하면 루틴 분석과 훈련 기록을 사용할 수 있어.")
        if st.button("이 루틴 삭제",key="delete_routine"):
            data["routines"]=[r for r in data["routines"] if r["id"]!=rid]; st.rerun()

elif page == "운동 저장소":
    st.title("운동 저장소")
    if not data["saved"]: st.info("저장된 운동이 없어. 운동 도감에서 운동을 저장해 봐.")
    for name in data["saved"]:
        ex=exercise(name)
        if ex:
            with st.container(border=True):
                st.markdown(f"### ★ {name}"); st.caption(f"{ex['body']} · {ex['type']} · {ex['level']}")
                st.write("주요 근육: "+", ".join(ex["main"])); st.write(ex["form"])
                if st.button("저장 해제",key="unsave_"+name):
                    data["saved"].remove(name); st.rerun()

elif page == "운동 기록":
    st.title("운동 기록")
    if not data["logs"]: st.info("아직 기록이 없어. 루틴 모드에서 훈련을 저장해 봐.")
    else:
        dates=sorted({x["date"] for x in data["logs"]},reverse=True)
        chosen_date=st.date_input("조회 날짜",value=date.fromisoformat(dates[0]))
        matches=[x for x in data["logs"] if x["date"]==chosen_date.isoformat()]
        if not matches: st.caption("이 날짜에는 기록이 없어.")
        for log in matches:
            with st.container(border=True):
                st.markdown(f"### {log['routine_name']}")
                st.caption(f"{log['date']} · +{log['xp']} XP")
                df=pd.DataFrame([{"운동":v["exercise"],"세트":v["set"],"중량(kg)":v["weight"],"반복":v["reps"],"완료":"완료" if v["done"] else "미완료"} for v in log["sets"]])
                st.dataframe(df,use_container_width=True,hide_index=True)
                if st.button("이 기록 삭제",key="del_log_"+log["id"]):
                    data["logs"]=[x for x in data["logs"] if x["id"]!=log["id"]]
                    st.warning("기록을 삭제했어. 이미 획득한 XP는 회수되지 않아."); st.rerun()
        st.subheader("최근 30일 훈련")
        cutoff=date.today()-timedelta(days=29)
        counts=Counter(x["date"] for x in data["logs"] if cutoff.isoformat()<=x["date"]<=date.today().isoformat())
        chart=pd.DataFrame([{"날짜":(cutoff+timedelta(days=i)).isoformat(),"훈련 횟수":counts.get((cutoff+timedelta(days=i)).isoformat(),0)} for i in range(30)])
        st.bar_chart(chart.set_index("날짜"))

elif page == "근육 분석":
    st.title("근육 분석")
    selected=st.multiselect("분석할 운동",[e["name"] for e in EXERCISES])
    if selected:
        recs,main,sub=suggestions(selected)
        st.subheader("근육 사용 지도")
        for muscle in sorted(set(main)|set(sub)):
            n=main.get(muscle,0); sn=sub.get(muscle,0)
            st.write(f"**{muscle}** · 주요 {n}개 운동 / 보조 {sn}개 운동")
            st.progress(min(1.0,(n+sn)/max(1,len(selected))))
        repeated={k:v for k,v in main.items() if v>=2}
        st.subheader("반복되는 주요 근육")
        if repeated:
            for m,n in repeated.items(): st.write(f"- **{m}**: {n}개 운동")
            st.info("근육 중복이 무조건 나쁜 것은 아니야. 전체 세트와 회복 상태도 고려해.")
        else: st.success("주요 근육이 반복되는 부위가 많지 않아.")
        st.subheader("보완 운동 추천")
        for _,new_n,e,overlap in recs[:6]:
            with st.container(border=True):
                st.markdown(f"### {e['name']}"); st.caption(f"{e['body']} · {e['type']} · {e['level']}")
                st.write("주요 근육: "+", ".join(e["main"]))
                if new_n: st.write(f"새로운 주요 근육 {new_n}개를 포함할 수 있어.")
                st.caption(e["tip"])
    else: st.info("분석할 운동을 선택해 줘.")

elif page == "근육학 TIP":
    st.title("근육학 TIP")
    st.caption("게임의 지식 도감처럼 하나씩 발견해 봐.")
    cats=["전체"]+sorted({t["category"] for t in TIPS})
    cat=st.selectbox("분류",cats); q=st.text_input("TIP 검색")
    st.write(f"📚 발견 {len(data['tips'])}/{len(TIPS)}"); st.progress(len(data["tips"])/len(TIPS))
    for tip in TIPS:
        if cat!="전체" and tip["category"]!=cat: continue
        if q and q.lower() not in (tip["title"]+tip["body"]+tip["fact"]+tip["category"]).lower(): continue
        found=tip["title"] in data["tips"]
        with st.container(border=True):
            st.caption(("📖 발견 완료" if found else "🔒 미발견")+" · "+tip["category"])
            st.markdown(f"### {tip['title']}"); st.write(tip["body"])
            with st.expander("한 단계 더 알아보기"):
                st.write(tip["fact"])
                if not found and st.button("TIP 발견 · +5 XP",key="discover_"+tip["title"],type="primary"):
                    data["tips"].append(tip["title"]); data["xp"]+=5; check_achievements(); st.rerun()

elif page == "업적":
    st.title("업적 도감")
    check_achievements()
    for key,name,desc,reward in ACHIEVEMENTS:
        done=key in data["achievements"]
        with st.container(border=True):
            st.markdown(("🏆 " if done else "🔒 ")+f"**{name}**")
            st.caption(desc); st.write(f"보상: +{reward} XP")
            if done: st.success("달성 완료")

elif page == "백업 / 복원":
    st.title("백업 / 복원")
    st.warning("로그인과 온라인 데이터베이스를 없앴기 때문에, 브라우저를 새로 열거나 세션이 끝나면 기록이 사라질 수 있어. 정기적으로 백업 파일을 다운로드해 줘.")
    st.download_button("전체 기록 백업 다운로드",data=export_data(),file_name="muscle_quest_backup.json",mime="application/json",type="primary")
    restore=st.file_uploader("백업 파일 선택",type=["json"],key="restore_main")
    if restore and st.button("선택한 백업 복원"):
        try:
            loaded=json.load(restore)
            if not set(DEFAULT_DATA).issubset(loaded): st.error("지원하지 않는 백업 형식이야.")
            else:
                st.session_state.mq_data=loaded; st.success("복원 완료!"); st.rerun()
        except Exception: st.error("파일을 읽지 못했어.")

st.divider()
st.caption("MUSCLE QUEST · 운동 정보는 일반적인 교육용 안내야. 통증이 생기면 중단하고 필요하면 전문가에게 상담해.")
