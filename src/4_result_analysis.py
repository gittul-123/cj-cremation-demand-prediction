import pandas as pd


# 데이터 불러오기
df = pd.read_csv(
    "processed/cremation_demand_forecast.csv"
)


# 화장 수요 증가율 계산

df["화장수요증가율"] = (
    df["예상화장건수"]
    .pct_change()
    * 100
)


# 첫 번째 값 처리

df["화장수요증가율"] = (
    df["화장수요증가율"]
    .fillna(0)
)


# 최대 수요 연도 확인

max_index = (
    df["예상화장건수"]
    .idxmax()
)


max_year = df.loc[max_index, "시점"]

max_demand = df.loc[
    max_index,
    "예상화장건수"
]


# 최소 수요 연도 확인

min_index = (
    df["예상화장건수"]
    .idxmin()
)

min_year = df.loc[
    min_index,
    "시점"
]

min_demand = df.loc[
    min_index,
    "예상화장건수"
]


# 평균 화장 수요

avg_demand = (
    df["예상화장건수"]
    .mean()
)

# 전체 기간 증가율

first = df.iloc[0]["예상화장건수"]

last = df.iloc[-1]["예상화장건수"]

total_growth = (
    (last - first)
    / first
    * 100
)



print("===================")
print("화장 수요 분석 결과")
print("===================")



start_year = int(df.iloc[0]["시점"])
end_year = int(df.iloc[-1]["시점"])

print(
    f"예측 기간: {start_year} ~ {end_year}"
)

print()

print(
    f"최소 예상 화장 건수: {min_demand:.0f}건 ({min_year})"
)

print(
    f"최대 예상 화장 건수: {max_demand:.0f}건 ({max_year})"
)

print(
    f"평균 예상 화장 건수: {avg_demand:.0f}건"
)

print(
    f"전체 기간 증가율: {total_growth:.2f}%"
)



# 결과 저장

df.to_csv(
    "processed/cremation_analysis_result.csv",
    index=False,
    encoding="utf-8-sig"
)


print(
    "분석 결과 저장 완료"
)