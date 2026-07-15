"""
청주시 장사시설 수요 예측 모델

목적:
인구 예측, 조사망률, 화장률 데이터를 활용하여
미래 화장 수요를 추정한다.

입력 데이터:
- population_forecast.csv
- cj_chosa.csv
- cj_cremation_rate.csv

처리 과정:
- 화장률 미래 예측
- 예상 사망자 수 계산
- 예상 화장 건수 산출

결과:
- cremation_demand_forecast.csv
- cremation_demand_forecast.png
"""

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"


# 미래 인구 예측 데이터
population = pd.read_csv(
    "processed/population_forecast.csv"
)

# 조사망률 데이터
mortality = pd.read_csv(
    "data/cj_chosa.csv",
    encoding="cp949"
)

# 조사망률 컬럼명 변경
mortality = mortality.rename(
    columns={"조사망률(인구천명당)": "조사망률"}
)


# 화장률 데이터
cremation = pd.read_csv(
    "data/cj_cremation_rate.csv",
    encoding="cp949"
)


print("인구 예측 데이터")
print(population.head())

print("\n조사망률 데이터")
print(mortality.head())

print("\n화장률 데이터")
print(cremation.head())


from sklearn.linear_model import LinearRegression


# 화장률 예측용 데이터 준비
X = cremation[["시점"]]
y = cremation["청주시화장률"]


# 모델 생성 및 학습
cremation_model = LinearRegression()
cremation_model.fit(X, y)


# 미래 연도 생성
future_years = pd.DataFrame({
    "시점": range(2025, 2036)
})


# 화장률 예측
future_cremation = cremation_model.predict(future_years)


# 화장률 상한
future_cremation = future_cremation.clip(0, 99)

# 결과 저장
cremation_forecast = future_years.copy()
cremation_forecast["예측화장률"] = future_cremation


print(cremation_forecast)


# 데이터 병합
demand_df = population.merge(
    mortality[["시점", "조사망률"]],
    on="시점",
    how="inner"
)

demand_df = demand_df.merge(
    cremation_forecast,
    on="시점",
    how="inner"
)


# 예상 사망자 수 계산
demand_df["예상사망자수"] = (
    demand_df["예측인구"]
    * demand_df["조사망률"]
    / 1000
)

# 예상 화장 건수 계산
demand_df["예상화장건수"] = (
    demand_df["예상사망자수"]
    * demand_df["예측화장률"]
    / 100
)

# 정수 처리
demand_df["예상사망자수"] = demand_df["예상사망자수"].round()
demand_df["예상화장건수"] = demand_df["예상화장건수"].round()


print(demand_df)


# 최종 결과에서 불필요한 변수 제거
demand_df = demand_df.drop(columns=["t"])



# 결과 저장
demand_df.to_csv(
    "processed/cremation_demand_forecast.csv",
    index=False,
    encoding="utf-8-sig"
)




plt.figure(figsize=(10, 5))

plt.plot(
    demand_df["시점"],
    demand_df["예상화장건수"],
    marker="o"
)

plt.title("청주시 예상 화장 건수 추이")
plt.xlabel("연도")
plt.ylabel("예상 화장 건수")

plt.grid()

plt.savefig(
    "processed/cremation_demand_forecast.png",
    dpi=300,
    bbox_inches="tight"
)


plt.show()
