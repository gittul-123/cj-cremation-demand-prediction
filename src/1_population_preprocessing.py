import pandas as pd

# 데이터 불러오기
df = pd.read_csv(r"C:\Users\Administrator\Desktop\py4e\py_project\raw\cj_n_cw.csv", encoding="cp949")

# 첫 번째 설명 행 제거
df = df.iloc[1:].copy()


# 숫자형으로 변환(-를 NaN으로)
df["청주시"] = pd.to_numeric(df["청주시"], errors="coerce")
df["청원군"] = pd.to_numeric(df["청원군"], errors="coerce")

# 청원군의 NaN을 0으로 처리
df["청원군"] = df["청원군"].fillna(0)

# 통합 청주시 인구 생성
df["통합청주시"] = df["청주시"] + df["청원군"]

# 필요한 열만 선택
df = df[["시점", "통합청주시"]]

# 결과 확인
print(df.head())
print(df.tail())


# 전처리된 데이터 저장
df.to_csv(r"C:\Users\Administrator\Desktop\py4e\py_project\processed\population_processed.csv", index=False, encoding="utf-8-sig")