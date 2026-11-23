import streamlit as st
from datetime import date, time
import hashlib
from PIL import Image

st.set_page_config(page_title="운명의 정원", page_icon="🔮", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Playfair+Display:wght@500;700&display=swap');
.stApp {background: linear-gradient(135deg,#100d1c,#211633,#171221); color:#f4eee5; font-family:'Gowun Dodum',sans-serif;}
.block-container {padding-top:2rem;padding-bottom:3rem;max-width:1200px;}
h1,h2,h3 {color:#e8c98b !important;font-family:'Playfair Display',serif;}
p,label,span {color:#e8e0d5;}
[data-testid="stMetric"] {background:rgba(230,201,139,.08);border:1px solid rgba(230,201,139,.25);padding:20px;border-radius:18px;}
[data-testid="stMetricValue"] {color:#e8c98b !important;}
.stTabs [data-baseweb="tab"] {background:transparent;color:#d7c6e5;border-radius:10px;padding:12px 20px;}
.stTabs [aria-selected="true"] {background:#4a3563 !important;color:#f4d69c !important;}
div.stButton>button {background:linear-gradient(90deg,#8a65a9,#c49a64);color:white;border:none;border-radius:12px;height:3rem;font-weight:bold;}
div.stButton>button:hover {border:1px solid #f3d9a0;color:white;transform:translateY(-2px);}
div[data-testid="stExpander"] {background:rgba(255,255,255,.03);border:1px solid rgba(220,190,150,.15);border-radius:15px;}
.card {background:rgba(255,255,255,.045);border:1px solid rgba(218,188,135,.22);border-radius:18px;padding:24px;margin:12px 0;}
.card-title {color:#e8c98b;font-size:1.1rem;font-weight:bold;margin-bottom:10px;}
.card-text {color:#eee4d7;line-height:1.8;}
.small {color:#b9a9c7;font-size:.85rem;}
hr {border-color:rgba(220,190,150,.2);}
</style>
""", unsafe_allow_html=True)

def zodiac(d):
    signs=[("염소자리",(1,1),(1,19)),("물병자리",(1,20),(2,18)),("물고기자리",(2,19),(3,20)),
    ("양자리",(3,21),(4,19)),("황소자리",(4,20),(5,20)),("쌍둥이자리",(5,21),(6,20)),
    ("게자리",(6,21),(7,22)),("사자자리",(7,23),(8,22)),("처녀자리",(8,23),(9,22)),
    ("천칭자리",(9,23),(10,22)),("전갈자리",(10,23),(11,21)),("사수자리",(11,22),(12,21)),
    ("염소자리",(12,22),(12,31))]
    md=(d.month,d.day)
    for name,start,end in signs:
        if start<=md<=end: return name
    return "염소자리"

def chinese_zodiac(year):
    animals=["쥐","소","호랑이","토끼","용","뱀","말","양","원숭이","닭","개","돼지"]
    return animals[(year-4)%12]+"띠"

def element(year):
    return {0:"금",1:"금",2:"수",3:"수",4:"목",5:"목",6:"화",7:"화",8:"토",9:"토"}[year%10]

def stable_score(seed,low=60,high=98):
    n=int(hashlib.sha256(seed.encode()).hexdigest()[:8],16)
    return low+n%(high-low+1)

def person_info(name,dob,birth_time):
    return {"별자리":zodiac(dob),"띠":chinese_zodiac(dob.year),"오행 참고":element(dob)+"의 기운",
            "생일 숫자":1+((dob.year+dob.month+dob.day-1)%9),
            "출생 시간":birth_time.strftime("%H:%M") if birth_time else "미입력"}

def show_card(title,text):
    st.markdown(f'<div class="card"><div class="card-title">{title}</div><div class="card-text">{text}</div></div>',unsafe_allow_html=True)

def compatibility_text(score):
    if score>=90: return "아주 좋은 조합으로 해석되는 궁합이에요. 서로의 차이를 이해하고 함께하는 경험을 쌓을수록 관계가 풍부해질 수 있다는 의미로 풀이해 볼 수 있어요."
    if score>=80: return "서로에게 긍정적인 영향을 주는 조합으로 해석할 수 있어요. 대화와 배려를 통해 좋은 관계를 만들어갈 가능성을 상징하는 결과예요."
    if score>=70: return "서로 다른 부분을 알아가는 과정이 중요한 조합이에요. 상대방의 생각을 존중하고 소통한다면 편안한 관계를 만들어갈 수 있어요."
    return "서로의 차이를 발견하고 이해하는 과정에 의미가 있는 조합이에요. 점수보다 실제 대화와 행동으로 관계를 만들어가는 것이 중요해요."

def attachment_quiz(label):
    st.markdown(f"### {label}의 관계 성향")
    q1=st.radio("상대방의 연락이 늦어지면?",["크게 신경 쓰지 않는다","걱정되거나 확인하고 싶어진다","혼자 시간을 보내고 싶어진다"],key=f"{label}_q1")
    q2=st.radio("갈등이 생기면?",["대화를 통해 풀려고 한다","상대의 마음이 변했을까 걱정한다","일단 거리를 두고 생각한다"],key=f"{label}_q2")
    q3=st.radio("관계가 가까워질수록?",["친밀함과 개인 시간을 균형 있게 유지한다","애정 표현과 확인이 더 필요하다","혼자만의 공간이 중요하다"],key=f"{label}_q3")
    answers=[q1,q2,q3]
    anxious=sum(("걱정" in x or "확인" in x or "변했을까" in x) for x in answers)
    avoidant=sum(("거리" in x or "혼자" in x) for x in answers)
    secure=3-anxious-avoidant
    if secure>=anxious and secure>=avoidant: return "안정적인 소통을 선호하는 응답"
    if anxious>avoidant: return "확인과 표현을 중요하게 생각하는 응답"
    if avoidant>anxious: return "개인 시간과 공간을 중요하게 생각하는 응답"
    return "혼합된 관계 성향 응답"

face_interpretations={
"얼굴형":{"둥근형":"전통 관상에서는 둥근 얼굴을 부드러움과 원만함의 상징으로 해석하기도 했어요.","계란형":"계란형 얼굴은 균형과 조화를 상징하는 형태로 풀이되곤 해요.","각진형":"각진 얼굴형은 단단함과 결단력의 이미지로 연결되기도 합니다.","긴형":"긴 얼굴형은 차분함과 신중함의 이미지로 표현되기도 해요."},
"눈매":{"둥글고 큰 눈":"둥근 눈은 부드럽고 친근한 이미지와 연결되기도 해요.","길고 가는 눈":"길게 뻗은 눈매는 차분하고 세련된 분위기를 상징하는 표현으로 쓰입니다.","올라간 눈매":"올라간 눈매는 또렷하고 강렬한 인상이라는 이미지와 연결됩니다.","내려간 눈매":"내려간 눈매는 편안하고 온화한 분위기를 상징하는 표현으로 쓰이기도 해요."},
"눈썹":{"일자 눈썹":"일자 눈썹은 깔끔하고 단정한 인상과 연결됩니다.","아치형 눈썹":"아치형 눈썹은 부드럽고 우아한 분위기를 상징하는 표현으로 쓰이기도 해요.","진한 눈썹":"진한 눈썹은 또렷하고 강한 인상이라는 이미지와 연결됩니다.","얇은 눈썹":"얇은 눈썹은 섬세하고 정돈된 분위기를 상징하기도 합니다."},
"코":{"둥근 코끝":"둥근 코끝은 부드럽고 친근한 인상을 상징하는 이미지로 풀이되기도 해요.","높고 곧은 코":"높고 곧은 코는 얼굴의 중심이 뚜렷한 인상이라는 표현과 연결됩니다.","작은 코":"작은 코는 섬세하고 아담한 인상이라는 이미지로 표현되기도 해요.","넓은 코":"넓은 코는 안정감 있는 인상이라는 전통적 이미지로 풀이되기도 합니다."},
"입":{"작은 입":"작은 입은 정돈되고 섬세한 인상이라는 이미지와 연결됩니다.","도톰한 입술":"도톰한 입술은 부드럽고 따뜻한 분위기를 상징하는 표현으로 쓰이기도 해요.","얇은 입술":"얇은 입술은 단정하고 깔끔한 인상이라는 이미지로 연결되기도 합니다.","넓은 입":"넓은 입은 밝고 활기찬 분위기를 상징하는 표현으로 쓰이기도 해요."}
}

def face_result(features):
    interpretations=[face_interpretations[k][v] for k,v in features.items()]
    keywords=[]
    shape=features["얼굴형"]
    keywords.append({"둥근형":"부드러운 이미지","각진형":"또렷한 이미지","긴형":"차분한 이미지","계란형":"균형 있는 이미지"}[shape])
    eye=features["눈매"]
    keywords.append({"둥글고 큰 눈":"친근한 분위기","길고 가는 눈":"세련된 분위기","올라간 눈매":"강렬한 분위기","내려간 눈매":"편안한 분위기"}[eye])
    return interpretations,keywords

st.markdown("""<div style="text-align:center;padding:20px 0 10px;">
<div style="font-size:45px;">🔮</div><h1 style="font-size:42px;">운명의 정원</h1>
<p style="color:#bba9cf;font-size:17px;">두 사람의 별과 전통 해석을 통해 관계를 돌아보는 공간</p></div>""",unsafe_allow_html=True)
st.markdown("---")
tab1,tab2=st.tabs(["✨ 생년월일 궁합","🌙 전통 관상 콘텐츠"])

with tab1:
    st.markdown("## ✦ 두 사람의 정보")
    mode=st.radio("관계 유형",["커플","커플 희망","친구"],horizontal=True)
    col1,col2=st.columns(2)
    with col1:
        st.markdown("### 🌷 나")
        name1=st.text_input("이름 또는 별명",value="나",key="person1")
        dob1=st.date_input("생년월일",value=date(2008,1,1),min_value=date(1900,1,1),max_value=date.today(),key="date1")
        unknown1=st.checkbox("태어난 시간 모름",value=True,key="unknown1")
        bt1=None if unknown1 else st.time_input("태어난 시간",value=time(12,0),key="time1")
    with col2:
        st.markdown("### 🌙 상대방")
        name2=st.text_input("이름 또는 별명",value="상대방",key="person2")
        dob2=st.date_input("생년월일",value=date(2008,1,1),min_value=date(1900,1,1),max_value=date.today(),key="date2")
        unknown2=st.checkbox("태어난 시간 모름",value=True,key="unknown2")
        bt2=None if unknown2 else st.time_input("태어난 시간",value=time(12,0),key="time2")
    st.markdown("---")
    st.markdown("## ✦ 관계 성향 알아보기")
    with st.expander(f"{name1}의 관계 성향",expanded=False): att1=attachment_quiz("나")
    with st.expander(f"{name2}의 관계 성향",expanded=False): att2=attachment_quiz("상대방")
    if st.button("✨ 두 사람의 궁합 확인하기",use_container_width=True,type="primary"):
        p1=person_info(name1,dob1,bt1);p2=person_info(name2,dob2,bt2)
        score=stable_score(f"{dob1}|{dob2}|{mode}")
        st.session_state["result"]={"p1":p1,"p2":p2,"score":score,"name1":name1 or "나","name2":name2 or "상대방","mode":mode,"att1":att1,"att2":att2}
    if "result" in st.session_state:
        r=st.session_state["result"];p1=r["p1"];p2=r["p2"];score=r["score"]
        st.markdown("---")
        st.markdown("<div style='text-align:center'><h2>✦ 두 사람의 궁합 결과 ✦</h2><p class='small'>별과 생년월일을 활용한 오락용 해석</p></div>",unsafe_allow_html=True)
        c1,c2,c3=st.columns([1,1.2,1])
        with c1: st.markdown(f"<div class='card' style='text-align:center'><h3>{r['name1']}</h3><div style='font-size:35px'>🌷</div><p>{p1['별자리']}</p><p>{p1['띠']}</p><p>{p1['오행 참고']}</p></div>",unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='card' style='text-align:center'><div class='small'>궁합 참고 점수</div><div style='font-size:52px;color:#e8c98b;font-weight:bold'>{score}%</div><div style='font-size:24px'>💞</div></div>",unsafe_allow_html=True)
            st.progress(score/100)
        with c3: st.markdown(f"<div class='card' style='text-align:center'><h3>{r['name2']}</h3><div style='font-size:35px'>🌙</div><p>{p2['별자리']}</p><p>{p2['띠']}</p><p>{p2['오행 참고']}</p></div>",unsafe_allow_html=True)
        show_card("💫 궁합 풀이",compatibility_text(score))
        show_card("🌷 성향 조합",f"{r['name1']}은(는) {p1['별자리']} · {p1['띠']}이고, {r['name2']}은(는) {p2['별자리']} · {p2['띠']}로 표시됩니다. 전통 조합을 재미로 해석해 볼 수 있어요. 실제 관계는 서로의 행동과 대화로 만들어집니다.")
        c1,c2=st.columns(2)
        with c1: show_card("🌿 나의 관계 성향",r["att1"])
        with c2: show_card("🌿 상대방의 관계 성향",r["att2"])
        st.markdown("## ✦ 관계를 위한 조언")
        for i,item in enumerate(["서로 편안하게 느끼는 연락 빈도를 이야기해 보세요.","서운한 점이 생겼을 때 추측보다 대화를 선택해 보세요.","함께 보내는 시간뿐 아니라 각자의 시간도 존중해 주세요.","고마웠던 행동을 구체적으로 표현해 보세요."],1): st.markdown(f"**{i}.** {item}")
        st.markdown("## ✦ 더 알아보기")
        topic=st.selectbox("궁금한 내용을 선택하세요",["이상형","데이트 아이디어","관계에서 주의할 점","친밀감","애정 표현","재회에 대해 생각해 보기"])
        contents={"이상형":"이상형은 생년월일보다 각자의 가치관과 경험에 따라 달라져요. 서로의 관심사를 존중하고 편안하게 소통할 수 있는 사람인지 생각해 보세요.","데이트 아이디어":"함께 전시를 보거나 산책하기, 보드게임하기, 서로 좋아하는 음악을 소개하기처럼 부담 없이 대화가 생기는 활동을 추천해요.","관계에서 주의할 점":"상대방의 마음을 혼자 추측하지 말고 직접 물어보세요. 연락 빈도, 개인 시간, 갈등 해결 방식에 대한 생각을 이야기하면 오해를 줄일 수 있어요.","친밀감":"친밀감은 점수로 정해지는 것이 아니에요. 서로 고민을 편하게 이야기할 수 있는지, 약속을 지키는지, 함께 있을 때 존중받는지를 살펴보세요.","애정 표현":"애정 표현은 말뿐 아니라 행동에서도 드러나요. 서로의 이야기를 기억하고, 약속을 지키며, 상대방의 경계를 존중하는 행동을 확인해 보세요.","재회에 대해 생각해 보기":"재회 여부는 운세로 예측할 수 없어요. 헤어진 이유가 해결되었는지, 서로 다시 관계를 원하는지, 이전 문제를 바꿀 구체적인 행동이 있는지를 생각해 보세요."}
        show_card(topic,contents[topic])

with tab2:
    st.markdown("## 🌙 전통 관상 콘텐츠")
    show_card("전통 관상이란?","과거에는 얼굴 특징을 통해 운세나 성향을 해석하는 관상 문화가 존재했습니다. 이 페이지는 전통적 해석을 현대적인 콘텐츠로 재구성한 오락용 서비스입니다. 실제 얼굴로 성격이나 미래를 판단하는 과학적 방법은 아닙니다.")
    col1,col2=st.columns(2)
    with col1:
        st.markdown("### 🌷 나의 사진")
        photo1=st.file_uploader("사진 업로드",type=["jpg","jpeg","png"],key="face1")
        if photo1: st.image(Image.open(photo1),caption="나의 사진",use_container_width=True)
    with col2:
        st.markdown("### 🌙 상대방 사진")
        photo2=st.file_uploader("사진 업로드",type=["jpg","jpeg","png"],key="face2")
        if photo2: st.image(Image.open(photo2),caption="상대방 사진",use_container_width=True)
    st.markdown("---")
    st.markdown("## ✦ 얼굴 특징 선택")
    st.caption("사진을 보며 해당하는 특징을 직접 선택해 주세요. 선택한 특징을 바탕으로 전통 관상 스타일의 콘텐츠를 보여줍니다.")
    col1,col2=st.columns(2)
    with col1:
        st.markdown("### 나")
        face1={"얼굴형":st.selectbox("얼굴형",["둥근형","계란형","각진형","긴형"],key="my_face"),
               "눈매":st.selectbox("눈매",["둥글고 큰 눈","길고 가는 눈","올라간 눈매","내려간 눈매"],key="my_eye"),
               "눈썹":st.selectbox("눈썹",["일자 눈썹","아치형 눈썹","진한 눈썹","얇은 눈썹"],key="my_brow"),
               "코":st.selectbox("코",["둥근 코끝","높고 곧은 코","작은 코","넓은 코"],key="my_nose"),
               "입":st.selectbox("입",["작은 입","도톰한 입술","얇은 입술","넓은 입"],key="my_mouth")}
    with col2:
        st.markdown("### 상대방")
        face2={"얼굴형":st.selectbox("얼굴형",["둥근형","계란형","각진형","긴형"],key="partner_face"),
               "눈매":st.selectbox("눈매",["둥글고 큰 눈","길고 가는 눈","올라간 눈매","내려간 눈매"],key="partner_eye"),
               "눈썹":st.selectbox("눈썹",["일자 눈썹","아치형 눈썹","진한 눈썹","얇은 눈썹"],key="partner_brow"),
               "코":st.selectbox("코",["둥근 코끝","높고 곧은 코","작은 코","넓은 코"],key="partner_nose"),
               "입":st.selectbox("입",["작은 입","도톰한 입술","얇은 입술","넓은 입"],key="partner_mouth")}
    st.markdown("---")
    if st.button("🔮 두 사람의 관상 콘텐츠 확인하기",use_container_width=True,type="primary"):
        if not photo1 or not photo2: st.error("두 사람의 사진을 모두 업로드해 주세요.")
        else:
            i1,k1=face_result(face1);i2,k2=face_result(face2)
            st.session_state["face_result"]={"face1":face1,"face2":face2,"interpretations1":i1,"interpretations2":i2,"keywords1":k1,"keywords2":k2}
    if "face_result" in st.session_state:
        fr=st.session_state["face_result"]
        st.markdown("---")
        st.markdown("<div style='text-align:center'><h2>✦ 관상 콘텐츠 결과 ✦</h2><p class='small'>전통적 얼굴 특징 해석을 바탕으로 한 오락 콘텐츠</p></div>",unsafe_allow_html=True)
        col1,col2=st.columns(2)
        with col1:
            st.markdown("### 🌷 나의 인상")
            show_card("인상 키워드"," · ".join(fr["keywords1"]))
            for i,text in enumerate(fr["interpretations1"],1): show_card(f"특징 {i}",text)
        with col2:
            st.markdown("### 🌙 상대방의 인상")
            show_card("인상 키워드"," · ".join(fr["keywords2"]))
            for i,text in enumerate(fr["interpretations2"],1): show_card(f"특징 {i}",text)
        st.markdown("## ✦ 두 사람의 인상 조합")
        combined=list(dict.fromkeys(fr["keywords1"]+fr["keywords2"]))
        show_card("🌟 이미지 조합",f"두 사람에게서 선택된 인상 키워드는 {', '.join(combined)}입니다. 서로 다른 분위기가 함께 있을 때 새로운 매력이 생긴다는 식으로 재미있게 해석해 볼 수 있어요.")
        show_card("💬 함께 이야기해 볼 질문","• 서로의 첫인상은 어땠나요?<br>• 처음 만났을 때와 지금의 인상은 어떻게 달라졌나요?<br>• 서로에게 가장 잘 어울린다고 생각하는 분위기는 무엇인가요?<br>• 상대방의 외모에서 가장 기억에 남는 특징은 무엇인가요?")
        st.caption("이 결과는 사진을 AI가 자동 분석한 결과가 아닙니다. 사용자가 직접 선택한 특징에 따른 전통적 해석 콘텐츠입니다.")

st.markdown("---")
st.markdown("""<div style="text-align:center;color:#9c8ba9;font-size:13px;">✦ 운명의 정원 ✦<br>본 서비스는 오락 및 자기성찰을 위한 콘텐츠입니다.<br>실제 사주 명리학 계산, 과학적 성격 분석, 미래 예측을 제공하지 않습니다.</div>""",unsafe_allow_html=True)
