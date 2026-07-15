import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# 데이터 읽기
df = pd.read_csv("processed/population_processed.csv")

# 시점을 숫자로 변환
df["시점"] = df["시점"].astype(int)

# 분석용 변수 생성
df["t"] = df["시점"] - df["시점"].min()


# 회귀모델 생성
model = LinearRegression()

# 독립변수(X), 종속변수(y)
X = df[["t"]]
y = df["통합청주시"]

# 모델 학습
model.fit(X, y)

# 예측값 계산
df["예측인구"] = model.predict(X).round().astype(int)


# 그래프
plt.figure(figsize=(10, 5))

# 실제 인구
plt.plot(df["시점"], df["통합청주시"], label="Actual Population")

# 예측 인구
plt.plot(df["시점"], df["예측인구"], "--", label="Predicted Population")

plt.xlabel("Year")
plt.ylabel("Population")
plt.title("Cheongju Population Trend")
plt.legend()

plt.show()

# 미래 연도 생성 (2026~2035)
future_years = pd.DataFrame({
    "시점": range(2026, 2036)
})

# t 계산
future_years["t"] = future_years["시점"] - df["시점"].min()

# 미래 인구 예측
future_years["예측인구"] = (
    model.predict(future_years[["t"]])
    .round()
    .astype(int)
)

print(future_years)

# 파일 저장

future_years.to_csv(
    "processed/population_forecast.csv",
    index=False,
    encoding="utf-8-sig"
)

print("저장 완료!")