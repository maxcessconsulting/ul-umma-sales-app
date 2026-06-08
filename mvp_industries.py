from __future__ import annotations

from copy import deepcopy

from pure_model import Competitor, ModelInput, calculate, default_input


INDUSTRIES = {
    "restaurant": {
        "name": "음식점 / 해장국",
        "target_daily_sales_thousand": 1799.0284318788188,
        "multiplier": 1.0,
        "mvp_note": "울엄마해장 엑셀 로직을 기준으로 변환한 계산기입니다.",
    },
    "pizza": {
        "name": "피자",
        "target_daily_sales_thousand": 720.7044352263048,
        "multiplier": 0.6002665113788707,
        "mvp_note": "피자마루 엑셀 기본값에 맞춰 보정한 MVP 계산기입니다.",
    },
    "chicken": {
        "name": "치킨",
        "target_daily_sales_thousand": 1505.5666228034672,
        "multiplier": 1.6044753361895954,
        "mvp_note": "푸라닭/치킨 업종 엑셀 기본값에 맞춰 보정한 MVP 계산기입니다.",
    },
}


def empty_traffic() -> list[list[float]]:
    return [[0.0] * 12 for _ in range(11)]


def pizza_default_input() -> ModelInput:
    data = ModelInput(
        store_name="피자마루",
        survey_month=6,
        weekday="금",
        region="충청권",
        admin_unit="시 단위",
        apartment_households=498,
        total_households=498,
        resident_population=1249,
        worker_population=910,
        annual_income=5124,
        deposit=30000,
        goodwill=20000,
        monthly_rent=2500,
        management_fee=0,
        business_days=26,
        cogs_rate=0.35,
        royalty_rate=0.025,
        franchise_fee=5000,
        education_fee=5000,
        guarantee_deposit=3000,
    )
    data.traffic = empty_traffic()
    data.traffic[1] = [18, 2, 0, 8, 2, 24, 8, 20, 4, 10, 4, 10]
    data.traffic[2] = [6, 42, 16, 22, 24, 12, 6, 28, 0, 46, 18, 22]
    data.traffic[7] = [4, 14, 4, 6, 0, 6, 10, 16, 4, 0, 6, 12]
    data.traffic[8] = [6, 6, 12, 8, 18, 20, 10, 30, 4, 4, 12, 8]
    data.direct_competitors = [
        Competitor("피자마루", 36, 1, 2, 2, 3, 1, 1, 5, 3, 0, 2),
        Competitor("미스터피자", 25, 158, 2, 2, 2, 2, 1, 7, 3, 0, 3),
    ]
    data.indirect_competitors = []
    return data


def chicken_default_input() -> ModelInput:
    data = ModelInput(
        store_name="푸라닭 개금",
        survey_month=8,
        weekday="수",
        region="부산 경남",
        admin_unit="시 단위",
        apartment_households=2174,
        total_households=3005,
        resident_population=7224,
        worker_population=863,
        annual_income=5124,
        deposit=30000,
        goodwill=20000,
        monthly_rent=2500,
        management_fee=0,
        business_days=26,
        cogs_rate=0.45,
        royalty_rate=0.025,
        franchise_fee=5000,
        education_fee=5000,
        guarantee_deposit=3000,
    )
    data.traffic = empty_traffic()
    data.traffic[4] = [0, 0, 4, 8, 2, 4, 0, 6, 4, 6, 6, 14]
    data.traffic[5] = [6, 6, 4, 10, 4, 0, 2, 18, 2, 12, 10, 8]
    data.traffic[8] = [4, 10, 22, 14, 8, 2, 14, 10, 8, 8, 4, 4]
    data.traffic[9] = [10, 2, 18, 12, 4, 2, 6, 8, 8, 6, 12, 4]
    data.direct_competitors = [
        Competitor("푸라닭 개금", 11, 1, 2, 3, 1, 1, 1, 4, 3, 0, 3),
        Competitor("문진옥숯불바베큐", 10, 92, 2, 2, 3, 1, 1, 7, 3, 0, 1),
        Competitor("멕시카나치킨", 12, 144, 1, 3, 1, 1, 1, 6, 3, 0, 1),
        Competitor("썬더치킨", 32, 249, 1, 2, 3, 2, 2, 21, 3, 0, 1),
        Competitor("치킨상파전", 9, 266, 2, 2, 2, 1, 1, 7, 2, 0, 2),
        Competitor("착한 맛집", 5, 177, 1, 2, 2, 1, 1, 2.5, 3, 0, 1),
    ]
    data.indirect_competitors = []
    return data


def get_default_input(industry_code: str) -> ModelInput:
    if industry_code == "restaurant":
        return default_input()
    if industry_code == "pizza":
        return pizza_default_input()
    if industry_code == "chicken":
        return chicken_default_input()
    raise ValueError(f"지원하지 않는 업종입니다: {industry_code}")


def calculate_industry(industry_code: str, data: ModelInput) -> dict:
    result = calculate(data)
    multiplier = INDUSTRIES[industry_code]["multiplier"]
    if multiplier == 1.0:
        result["industry_name"] = INDUSTRIES[industry_code]["name"]
        result["mvp_note"] = INDUSTRIES[industry_code]["mvp_note"]
        return result

    result = deepcopy(result)
    for key in [
        "traffic_potential_total",
        "household_potential_total",
        "worker_potential_total",
        "candidate_traffic_sales",
        "candidate_household_sales",
        "candidate_worker_sales",
        "daily_sales_thousand",
        "monthly_sales_thousand",
        "monthly_sales_ex_vat_thousand",
        "cogs_thousand",
        "royalty_thousand",
        "contribution_profit_thousand",
    ]:
        result[key] *= multiplier
    result["industry_name"] = INDUSTRIES[industry_code]["name"]
    result["mvp_note"] = INDUSTRIES[industry_code]["mvp_note"]
    result["mvp_multiplier"] = multiplier
    return result
