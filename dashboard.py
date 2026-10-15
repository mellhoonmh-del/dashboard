import pandas as pd
import streamlit as st

# 1. 웹 앱 제목과 설명 설정
st.title("📚 공부 습관 대시보드")
st.write(
    "파이썬 기초 프로젝트: 학생들의 공부 시간과 성적 데이터를 분석하는 대시보드입니다."
)


# 2. 데이터 불러오기 함수 (캐시 기능 사용)
@st.cache_data
def load_data():
    # study.csv 파일을 읽어옵니다. (열: 학생ID, 공부시간, 스마트폰, 점수)
    df = pd.read_csv("study.csv")
    return df


# 파일이 없을 경우를 대비한 예외 처리 (실습 시 참고용)
try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "⚠️ 'study.csv' 파일을 찾을 수 없습니다. 파이썬 파일과 같은 폴더에 CSV 파일을 넣어주세요!"
    )
    # 테스트를 위한 가상 데이터 생성
    data = {
        "학생ID": ["A01", "A02", "A03", "A04", "A05"],
        "공부시간": [2, 6, 3, 8, 5],
        "스마트폰": [4, 1, 5, 2, 3],
        "점수": [55, 90, 65, 95, 78],
    }
    df = pd.DataFrame(data)

# 3. 핵심 요약 지표(st.metric)를 한 줄(3개의 열)에 표시
st.subheader("📊 전체 요약 지표")
col1, col2, col3 = st.columns(3)

total_students = len(df)  # 전체 학생 수 계산
avg_score = df["점수"].mean()  # 평균 점수 계산
avg_study_time = df["공부시간"].mean()  # 평균 공부시간 계산

# 각 열에 지표 배치
col1.metric("전체 학생 수", f"{total_students}명")
col2.metric("평균 점수", f"{avg_score:.1f}점")
col3.metric("평균 공부시간", f"{avg_study_time:.1f}시간")

st.markdown("---")

# 4. 슬라이더로 '최소 공부시간' 필터 만들기
st.subheader("🔍 조건별 학생 필터링")
min_val = int(df["공부시간"].min())
max_val = int(df["공부시간"].max())

# st.slider로 최소 공부시간 선택받기
selected_min_time = st.slider(
    "원하는 최소 공부시간을 선택하세요 (시간)",
    min_value=min_val,
    max_value=max_val,
    value=min_val,
)

# 선택한 시간 이상인 학생들만 데이터프레임에서 필터링
filtered_df = df[df["공부시간"] >= selected_min_time]

st.write(
    f"조건에 만족하는 학생은 총 **{len(filtered_df)}명**입니다."
)  # 필터링된 학생 수 안내
st.dataframe(filtered_df)  # 필터링된 데이터 표 출력

st.markdown("---")

# 5. 기본 차트를 활용한 시각화
st.subheader("📈 데이터 시각화")

# 화면을 두 개의 열로 나누어 차트 배치
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**[산점도] 공부시간 vs 점수**")
    # Streamlit 기본 산점도 함수 사용
    st.scatter_chart(filtered_df, x="공부시간", y="점수")

with chart_col2:
    st.markdown("**[막대 그래프] 학생별 점수**")
    # 학생ID를 인덱스로 지정하여 막대 그래프 생성
    bar_data = filtered_df.set_index("학생ID")["점수"]
    st.bar_chart(bar_data)