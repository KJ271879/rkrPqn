import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("간단한 가계부 프로그램")

# 초기화: 세션 상태에 데이터프레임 저장
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["날짜", "종류", "금액", "메모"])

# 입력 폼
with st.form("entry_form"):
    date = st.date_input("날짜")
    kind = st.selectbox("종류", ["수입", "지출"])
    amount = st.number_input("금액", min_value=0)
    memo = st.text_input("메모")
    submitted = st.form_submit_button("기록 추가")

if submitted:
    new_entry = {"날짜": date, "종류": kind, "금액": amount, "메모": memo}
    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_entry])], ignore_index=True)
    st.success("기록이 추가되었습니다!")

df = st.session_state.df

if not df.empty:
    st.subheader("가계부 내역")
    st.dataframe(df)

    # 수입/지출 합계
    income_sum = df.loc[df["종류"] == "수입", "금액"].sum()
    expense_sum = df.loc[df["종류"] == "지출", "금액"].sum()
    balance = income_sum - expense_sum

    st.write(f"총 수입: {income_sum:,} 원")
    st.write(f"총 지출: {expense_sum:,} 원")
    st.write(f"순이익: {balance:,} 원")

    # 날짜별 수입/지출 합산
    pivot_df = df.pivot_table(index="날짜", columns="종류", values="금액", aggfunc='sum', fill_value=0).reset_index()

    # 날짜별 수입, 지출 그래프
    fig, ax = plt.subplots()
    ax.bar(pivot_df["날짜"] - pd.Timedelta(days=0.2), pivot_df.get("수입", 0), width=0.4, label="수입", color="green")
    ax.bar(pivot_df["날짜"] + pd.Timedelta(days=0.2), pivot_df.get("지출", 0), width=0.4, label="지출", color="red")
    ax.set_xlabel("날짜")
    ax.set_ylabel("금액")
    ax.legend()
    st.pyplot(fig)

else:
    st.info("가계부 내역이 없습니다. 기록을 추가해보세요.")
