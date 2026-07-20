import pandas as pd
import math

# 결과 파일 불러오기
df = pd.read_csv("processed/cremation_analysis_result.csv")


# 화장로 1기당 연간 처리능력(제3차 청주시 장사시설 지역 수급계획 기준)
capacity_per_furnace = 1448


# 필요한 화장로 수 계산
df["필요화장로수"] = (
    df["예상화장건수"] / capacity_per_furnace
).apply(math.ceil)


# 현재 운영 중인 화장로 수(제3차 청주시 장사시설 지역 수급계획 기준, 일반시신 8로+개장유골 1로)
CURRENT_FURNACES = 9

# 추가로 필요한 화장로 수 계산
df["추가필요화장로"] = df["필요화장로수"] - CURRENT_FURNACES

# 음수는 0으로 처리(추가 증설 불필요)
df.loc[df["추가필요화장로"] < 0, "추가필요화장로"] = 0


print(
    df[
        [
            "시점",
            "예상화장건수",
            "필요화장로수",
            "추가필요화장로"
        ]
    ]
)



# 결과 저장
df.to_csv(
    "processed/facility_plan.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\n시설 계획 결과가 저장되었습니다.")