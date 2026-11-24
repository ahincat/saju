
import streamlit as st
import random
import hashlib
from datetime import date

# ==========================================
# 페이지 설정
# ==========================================
st.set_page_config(
    page_title="운명의 정원",
    page_icon="🔮",
    layout="wide"
)

# ==========================================
# 디자인
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&family=Noto+Sans+KR:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #100b22, #21143b, #100b22);
    color: #f5eaff;
}

h1, h2, h3 {
    font-family: 'Gowun Batang', serif !important;
    color: #e9d5ff !important;
}

p, label, div {
    color: #f5eaff;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.07);
    border: 1px solid #9b7bc7;
    border-radius: 15px;
    padding: 15px;
}

.stButton > button {
    background: linear-gradient(90deg, #7652a8, #a17bd0);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.5rem;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #a17bd0, #c3a3ed);
    color: white;
}

div[data-testid="stTabs"] button {
    font-size: 18px;
}

.tarot-card {
    background: linear-gradient(180deg, #34204e, #1b1230);
    border: 1px solid #c6a5ec;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    min-height: 300px;
}

.tarot-emoji {
    font-size: 65px;
}

.tarot-title {
    font-size: 24px;
    font-weight: bold;
    color: #e8caff;
}

.tarot-position {
    color: #c9a9ed;
    font-size: 16px;
}

.tarot-meaning {
    font-size: 17px;
    line-height: 1.8;
    margin-top: 15px;
}

hr {
    border-color: #5e467d;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 제목
# ==========================================
st.title("🌙 운명의 정원")
st.markdown(
    "✨ 당신의 운명과 마음을 들여다보는 신비로운 공간 ✨"
)
st.markdown("---")

# ==========================================
# 탭
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "💫 생년월일 궁합",
    "🔮 얼굴 관상",
    "🃏 타로"
])

# ==========================================
# TAB 1. 생년월일 궁합
# ==========================================
with tab1:

    st.header("💫 두 사람의 궁합 알아보기")
    st.write("두 사람의 생년월일을 통해 재미로 궁합을 알아보세요.")

    col1, col2 = st.columns(2)

    with col1:
        name1 = st.text_input("첫 번째 사람 이름", key="name1")
        birth1 = st.date_input(
            "첫 번째 사람 생년월일",
            value=date(2008, 1, 1),
            key="birth1",
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

    with col2:
        name2 = st.text_input("두 번째 사람 이름", key="name2")
        birth2 = st.date_input(
            "두 번째 사람 생년월일",
            value=date(2008, 1, 1),
            key="birth2",
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

    relation = st.selectbox(
        "두 사람의 관계",
        ["친구", "짝사랑", "연인", "가족", "새로운 인연"]
    )

    if st.button("💜 궁합 확인하기", key="compatibility_button"):

        if not name1.strip() or not name2.strip():
            st.warning("두 사람의 이름을 모두 입력해주세요!")

        else:
            seed_text = (
                str(name1) + str(birth1) +
                str(name2) + str(birth2) +
                str(relation)
            )

            hash_value = hashlib.sha256(
                seed_text.encode()
            ).hexdigest()

            score = int(hash_value[:8], 16) % 101

            st.markdown("---")
            st.subheader(f"💞 {name1} & {name2}의 궁합")

            st.metric("궁합 점수", f"{score}점")

            st.progress(score / 100)

            if score >= 90:
                result = "✨ 서로에게 특별한 에너지를 주는 관계!"
                advice = "함께할 때 좋은 시너지를 낼 수 있는 관계예요. 서로의 장점을 발견하고 응원해 보세요."
            elif score >= 75:
                result = "💜 아주 잘 맞는 관계!"
                advice = "서로를 이해하려는 마음이 관계를 더욱 깊게 만들어 줄 거예요."
            elif score >= 60:
                result = "🌷 편안하게 발전할 수 있는 관계!"
                advice = "서로 다른 점을 인정하고 대화한다면 좋은 관계를 만들어 갈 수 있어요."
            elif score >= 40:
                result = "🌙 서로 알아가는 과정이 필요한 관계!"
                advice = "처음에는 다르게 느껴질 수 있지만, 서로를 이해하는 과정이 중요해요."
            else:
                result = "🌱 새로운 방식으로 이해해 볼 관계!"
                advice = "점수보다 실제로 서로를 존중하고 편안하게 느끼는지가 더 중요해요."

            st.markdown(f"### {result}")
            st.write(advice)

            st.info(
                "💌 궁합 점수는 이름과 생년월일을 이용한 재미용 계산 결과이며, "
                "실제 관계를 결정하는 기준은 아니에요."
            )

# ==========================================
# TAB 2. 얼굴 관상
# ==========================================
with tab2:

    st.header("🔮 나의 관상 알아보기")
    st.write("얼굴의 특징을 선택하고 재미로 관상 해석을 확인해 보세요.")

    st.caption(
        "※ 실제 성격이나 운명을 얼굴로 판단할 수는 없으며, "
        "전통적인 관상 표현을 활용한 재미용 콘텐츠입니다."
    )

    face_shape = st.selectbox(
        "얼굴형",
        ["둥근형", "계란형", "각진형", "긴형", "하트형"]
    )

    eyes = st.selectbox(
        "눈 모양",
        ["큰 눈", "작은 눈", "둥근 눈", "올라간 눈", "처진 눈", "가늘고 긴 눈"]
    )

    eyebrows = st.selectbox(
        "눈썹",
        ["진한 눈썹", "얇은 눈썹", "일자 눈썹", "아치형 눈썹", "짧은 눈썹"]
    )

    nose = st.selectbox(
        "코",
        ["높은 코", "낮은 코", "둥근 코끝", "날렵한 코", "작은 코"]
    )

    mouth = st.selectbox(
        "입 모양",
        ["큰 입", "작은 입", "도톰한 입술", "얇은 입술", "웃는 입"]
    )

    if st.button("✨ 내 관상 풀이 보기", key="face_button"):

        face_interpretations = {
            "둥근형": "당신의 얼굴은 부드럽고 친근한 분위기를 상징해요. 주변 사람들에게 편안한 인상을 주는 이미지로 표현되곤 해요.",
            "계란형": "당신의 얼굴은 균형과 조화를 상징해요. 여러 분위기를 자연스럽게 소화하는 이미지로 표현돼요.",
            "각진형": "당신의 얼굴은 뚜렷하고 힘 있는 인상을 상징해요. 단단한 분위기와 개성이 돋보이는 이미지예요.",
            "긴형": "당신의 얼굴은 차분하고 성숙한 분위기를 상징해요. 깊이 있는 인상을 주는 이미지로 표현돼요.",
            "하트형": "당신의 얼굴은 사랑스럽고 독특한 분위기를 상징해요. 개성 있고 눈에 띄는 이미지예요."
        }

        eye_interpretations = {
            "큰 눈": "당신의 눈은 호기심과 표현력을 상징해요. 감정이 풍부한 이미지로 표현돼요.",
            "작은 눈": "당신의 눈은 집중력과 섬세함을 상징해요. 신중한 분위기를 나타내는 이미지예요.",
            "둥근 눈": "당신의 눈은 순수함과 부드러움을 상징해요. 밝고 친근한 분위기를 표현해요.",
            "올라간 눈": "당신의 눈은 생동감과 자신감을 상징해요. 강렬하고 개성 있는 이미지예요.",
            "처진 눈": "당신의 눈은 온화함과 따뜻함을 상징해요. 부드럽고 편안한 분위기를 표현해요.",
            "가늘고 긴 눈": "당신의 눈은 차분함과 세련된 분위기를 상징해요. 신비로운 이미지로 표현돼요."
        }

        eyebrow_interpretations = {
            "진한 눈썹": "당신의 눈썹은 뚜렷한 개성과 존재감을 상징해요.",
            "얇은 눈썹": "당신의 눈썹은 섬세하고 부드러운 분위기를 상징해요.",
            "일자 눈썹": "당신의 눈썹은 단정하고 담백한 이미지를 상징해요.",
            "아치형 눈썹": "당신의 눈썹은 우아하고 유연한 분위기를 상징해요.",
            "짧은 눈썹": "당신의 눈썹은 귀엽고 개성적인 인상을 상징해요."
        }

        nose_interpretations = {
            "높은 코": "당신의 코는 선명하고 또렷한 인상을 상징해요.",
            "낮은 코": "당신의 코는 부드럽고 자연스러운 분위기를 상징해요.",
            "둥근 코끝": "당신의 코는 따뜻하고 친근한 이미지를 상징해요.",
            "날렵한 코": "당신의 코는 세련되고 깔끔한 분위기를 상징해요.",
            "작은 코": "당신의 코는 아기자기하고 섬세한 이미지를 상징해요."
        }

        mouth_interpretations = {
            "큰 입": "당신의 입은 활발하고 표현력 있는 분위기를 상징해요.",
            "작은 입": "당신의 입은 섬세하고 차분한 이미지를 상징해요.",
            "도톰한 입술": "당신의 입은 따뜻하고 풍부한 표현을 상징해요.",
            "얇은 입술": "당신의 입은 깔끔하고 단정한 분위기를 상징해요.",
            "웃는 입": "당신의 입은 밝고 긍정적인 분위기를 상징해요."
        }

        st.markdown("---")
        st.subheader("🌸 당신의 관상 풀이")

        st.markdown(f"**🌷 얼굴형**")
        st.write(face_interpretations[face_shape])

        st.markdown(f"**👁️ 눈**")
        st.write(eye_interpretations[eyes])

        st.markdown(f"**🌿 눈썹**")
        st.write(eyebrow_interpretations[eyebrows])

        st.markdown(f"**✨ 코**")
        st.write(nose_interpretations[nose])

        st.markdown(f"**💗 입**")
        st.write(mouth_interpretations[mouth])

        st.markdown("---")

        st.success(
            "🌙 당신만의 매력은 하나의 특징으로 정의되지 않아요. "
            "이 해석은 재미로 즐기고, 실제 당신의 매력은 스스로 발견해 보세요!"
        )

# ==========================================
# TAB 3. 타로
# ==========================================
with tab3:

    st.header("🃏 마음을 비추는 타로")
    st.write(
        "궁금한 질문을 떠올리고 카드를 뽑아보세요. "
        "과거, 현재, 미래의 흐름을 상징적으로 해석해 드려요."
    )

    st.caption(
        "타로는 미래를 확정적으로 알려주는 것이 아니라 "
        "생각과 감정을 돌아보는 재미용 콘텐츠예요."
    )

    question = st.text_input(
        "🔮 어떤 고민이 있나요?",
        placeholder="예: 앞으로 나에게 어떤 변화가 찾아올까?",
        key="tarot_question"
    )

    tarot_cards = {
        "바보": {
            "emoji": "🌈",
            "upright": "새로운 시작과 자유로운 가능성을 상징해요. 익숙한 길에서 벗어나 새로운 경험을 해볼 수 있는 시기라는 메시지예요.",
            "reversed": "새로운 시작 앞에서 망설이거나 계획을 다시 점검할 필요가 있다는 메시지예요. 서두르지 않고 준비해도 괜찮아요."
        },
        "마법사": {
            "emoji": "✨",
            "upright": "자신의 능력과 아이디어를 활용할 수 있는 시기를 상징해요. 작은 행동이 새로운 결과로 이어질 수 있다는 메시지예요.",
            "reversed": "생각은 많지만 실행이 어려울 수 있다는 메시지예요. 목표를 작게 나누어 시작해 보세요."
        },
        "여사제": {
            "emoji": "🌙",
            "upright": "조용히 자신의 마음을 들여다보는 시간을 상징해요. 주변의 소리보다 자신의 생각과 감정에 귀 기울여 보세요.",
            "reversed": "혼란스러운 마음이나 놓치고 있는 감정이 있을 수 있다는 메시지예요. 잠시 쉬면서 생각을 정리해 보세요."
        },
        "여황제": {
            "emoji": "🌷",
            "upright": "풍요로움과 성장, 따뜻한 돌봄을 상징해요. 자신과 주변을 소중히 돌보는 시간이 도움이 될 수 있어요.",
            "reversed": "다른 사람을 챙기느라 자신을 놓치고 있지는 않은지 돌아보라는 메시지예요."
        },
        "황제": {
            "emoji": "👑",
            "upright": "안정과 책임감, 계획을 세우는 힘을 상징해요. 차분하게 기준을 세우고 행동해 보세요.",
            "reversed": "너무 엄격한 기준이나 통제에서 벗어나 유연함을 가져보라는 메시지예요."
        },
        "연인": {
            "emoji": "💞",
            "upright": "관계와 선택, 서로를 이해하는 마음을 상징해요. 중요한 것은 상대와 나 모두의 마음을 존중하는 선택이에요.",
            "reversed": "관계에서 서로의 생각이 다를 수 있다는 메시지예요. 솔직하고 편안한 대화가 도움이 될 수 있어요."
        },
        "전차": {
            "emoji": "🏇",
            "upright": "목표를 향해 나아가는 추진력을 상징해요. 자신이 원하는 방향을 정하고 꾸준히 움직여 보세요.",
            "reversed": "너무 급하게 나아가고 있지는 않은지 살펴보라는 메시지예요. 속도를 조절해도 괜찮아요."
        },
        "힘": {
            "emoji": "🦁",
            "upright": "용기와 인내, 부드러운 강인함을 상징해요. 무조건 버티기보다 자신을 이해하는 힘을 발휘해 보세요.",
            "reversed": "자신감이 잠시 흔들릴 수 있다는 메시지예요. 작은 성공을 통해 스스로를 믿는 마음을 키워보세요."
        },
        "은둔자": {
            "emoji": "🕯️",
            "upright": "혼자 생각을 정리하고 자신을 돌아보는 시간을 상징해요. 조용한 시간이 새로운 깨달음을 줄 수 있어요.",
            "reversed": "혼자 너무 많은 고민을 하고 있을 수 있다는 메시지예요. 믿을 수 있는 사람과 이야기를 나눠보세요."
        },
        "운명의 수레바퀴": {
            "emoji": "🎡",
            "upright": "변화와 새로운 흐름을 상징해요. 예상하지 못한 상황에서도 새로운 기회를 발견할 수 있다는 메시지예요.",
            "reversed": "변화가 생각보다 느리게 느껴질 수 있어요. 지금 할 수 있는 일에 집중해 보세요."
        },
        "별": {
            "emoji": "⭐",
            "upright": "희망과 회복, 새로운 가능성을 상징해요. 자신에게 긍정적인 기대를 가져도 좋다는 메시지예요.",
            "reversed": "희망이 잘 보이지 않는 순간에도 작은 가능성을 찾아보라는 메시지예요. 잠시 쉬어가는 것도 괜찮아요."
        },
        "태양": {
            "emoji": "☀️",
            "upright": "기쁨과 활력, 밝은 에너지를 상징해요. 즐거운 순간을 충분히 누리고 자신을 표현해 보세요.",
            "reversed": "좋은 일이 있어도 충분히 즐기지 못하고 있을 수 있어요. 작은 행복도 소중히 바라보세요."
        }
    }

    if st.button("🌟 카드 3장 뽑기", key="tarot_button"):

        drawn = random.sample(list(tarot_cards.keys()), 3)

        orientations = [
            random.choice([True, False])
            for _ in range(3)
        ]

        st.session_state.tarot_drawn = drawn
        st.session_state.tarot_orientations = orientations
        st.session_state.tarot_question = question

    if "tarot_drawn" in st.session_state:

        st.markdown("---")

        saved_question = st.session_state.tarot_question

        if saved_question:
            st.markdown(f"### 💭 질문: {saved_question}")
        else:
            st.markdown("### 🌙 오늘의 메시지")

        positions = ["과거", "현재", "미래"]

        drawn_cards = st.session_state.tarot_drawn
        orientations = st.session_state.tarot_orientations

        cols = st.columns(3)

        for i in range(3):

            card_name = drawn_cards[i]
            reversed_card = orientations[i]
            card = tarot_cards[card_name]

            direction = "역방향" if reversed_card else "정방향"

            interpretation = (
                card["reversed"]
                if reversed_card
                else card["upright"]
            )

            with cols[i]:

                st.markdown(
                    f"""
                    <div class="tarot-card">
                        <div class="tarot-position">
                            {positions[i]}
                        </div>
                        <div class="tarot-emoji">
                            {card["emoji"]}
                        </div>
                        <div class="tarot-title">
                            {card_name}
                        </div>
                        <div>
                            {direction}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("**카드 해석**")
                st.write(interpretation)

        st.markdown("---")
        st.subheader("✨ 전체 메시지")

        if orientations[0] and orientations[1] and orientations[2]:
            st.write(
                "지나온 경험에서 배움을 얻고, 현재의 마음을 돌아보며, "
                "앞으로의 가능성을 천천히 열어가 보세요. "
                "지금의 선택과 행동이 미래를 만들어가는 중요한 과정이에요."
            )
        elif not orientations[0] and orientations[1] and orientations[2]:
            st.write(
                "과거의 아쉬움에 머무르기보다는 현재 할 수 있는 일에 집중해 보세요. "
                "작은 변화가 새로운 가능성으로 이어질 수 있어요."
            )
        elif orientations[0] and not orientations[1] and orientations[2]:
            st.write(
                "과거의 경험을 바탕으로 지금의 마음을 정리하고, "
                "앞으로의 가능성을 차분하게 바라보세요."
            )
        else:
            st.write(
                "지금은 잠시 멈추어 자신을 돌아보는 시간일 수 있어요. "
                "급하게 답을 내리기보다 자신에게 필요한 것이 무엇인지 생각해 보세요."
            )

        st.info(
            "🔮 타로는 재미와 자기성찰을 위한 상징적 해석입니다. "
            "실제 미래나 타인의 마음을 확정적으로 알려주는 것은 아니에요."
        )

        if st.button("🔄 다시 뽑기", key="tarot_reset"):
            del st.session_state.tarot_drawn
            del st.session_state.tarot_orientations
            del st.session_state.tarot_question
            st.rerun()

# ==========================================
# 하단
# ==========================================
st.markdown("---")

st.markdown(
    "<div style='text-align:center; color:#c9a9ed;'>"
    "🌙 운명의 정원에서 오늘도 당신의 빛을 찾아보세요 🌙"
    "</div>",
    unsafe_allow_html=True
)
