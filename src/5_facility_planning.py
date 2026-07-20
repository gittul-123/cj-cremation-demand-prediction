import pandas as pd
import math
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows)
plt.rcParams["font.family"] = "Malgun Gothic"

# 마이너스(-) 깨짐 방지
plt.rcParams["axes.unicode_minus"] = False




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


# 필요 화장로 수 변화 그래프

plt.figure(figsize=(8, 5))

plt.plot(
    df["시점"],
    df["필요화장로수"],
    marker="o",
    markersize=7,
    linewidth=2,
    label="필요 화장로 수"
)

# 현재 운영 중인 화장로 수 표시

plt.axhline(
    y=CURRENT_FURNACES,
    linestyle="--",
    label="현재 운영 화장로(9기)"
    )

plt.legend(loc="best")


plt.title("연도별 필요 화장로 수")
plt.xlabel("연도")
plt.ylabel("필요 화장로 수")

plt.grid(True)

plt.savefig(
    "processed/facility_plan.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\n시설 계획 결과가 저장되었습니다.")