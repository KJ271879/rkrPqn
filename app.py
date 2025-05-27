import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("간단한 가계부 프로그램")

# 세션 상태에 DataFrame 초기화
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["날짜", "종류", "금액", "메모"])

# 입력 폼 만들기
with st.form("entry_form"):
    date = st.date_input("날짜")
    kind = st.selectbox("종류", ["수입", "지출"])
    amount = st.number_input("금액", min_value=0, step=1000)
    memo = st.text_input("메모")
    submitted = st.form_submit_button("기록 추가")

if submitted:
    # 새 항목 추가
    new_entry = {"날짜": date, "종류": kind, "금액": amount, "메모": memo}
    # 기존 데이터프레임에 새 행 추가
    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_entry])], ignore_index=True)
    st.success("기록이 추가되었습니다!")

df = st.session_state.df

if not df.empty:
    st.subheader("가계부 내역")
    st.dataframe(df)

    # 수입, 지출 합계 계산
    income_sum = df.loc[df["종류"] == "수입", "금액"].sum()
    expense_sum = df.loc[df["종류"] == "지출", "금액"].sum()
    balance = income_sum - expense_sum

    st.markdown(f"**총 수입:** {income_sum:,} 원")
    st.markdown(f"**총 지출:** {expense_sum:,} 원")
    st.markdown(f"**순이익:** {balance:,} 원")

    # 날짜별 수입/지출 집계
    pivot_df = df.pivot_table(index="날짜", columns="종류", values="금액", aggfunc='sum', fill_value=0).reset_index()
    pivot_df["날짜"] = pd.to_datetime(pivot_df["날짜"])

    # 막대 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 5))
    width = 0.4  # 바 너비
    ax.bar(pivot_df["날짜"] - pd.Timedelta(days=width/2), pivot_df.get("수입", 0), width=width, label="수입", color="green")
    ax.bar(pivot_df["날짜"] + pd.Timedelta(days=width/2), pivot_df.get("지출", 0), width=width, label="지출", color="red")

    ax.set_xlabel("날짜")
    ax.set_ylabel("금액")
    ax.set_title("날짜별 수입 및 지출")
    ax.legend()
    fig.autofmt_xdate()  # x축 라벨 회전

    st.pyplot(fig)
else:
    st.info("가계부 내역이 없습니다. 기록을 추가해보세요.")
