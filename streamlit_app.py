from __future__ import annotations

import streamlit as st

from mvp_industries import INDUSTRIES, calculate_industry, get_default_input
from pure_model import AGE_COLUMNS, TIME_LABELS, Competitor


st.set_page_config(page_title="울엄마해장 입지 평가 매출예측", layout="wide")

st.title("울엄마해장 입지 평가 매출예측")
st.caption("엑셀 파일을 실행하지 않고, 변환된 파이썬 계산 로직으로 산출합니다.")

industry_labels = {meta["name"]: code for code, meta in INDUSTRIES.items()}
selected_industry_name = st.sidebar.selectbox("업종 선택", list(industry_labels.keys()))
industry_code = industry_labels[selected_industry_name]
base = get_default_input(industry_code)
st.info(INDUSTRIES[industry_code]["mvp_note"])

with st.sidebar:
    st.header("기본 입력")
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    regions = ["서울 경기", "충청권", "호남권", "대구경북", "부산 경남", "강원권"]
    admin_units = ["시 단위", "군 단위"]
    operation_types = ["직영점", "가맹점", "위탁운영"]
    base.store_name = st.text_input("후보점명", base.store_name, key=f"{industry_code}_store_name")
    base.survey_month = st.number_input("조사월", min_value=1, max_value=12, value=base.survey_month, key=f"{industry_code}_survey_month")
    st.number_input("조사일", min_value=1, max_value=31, value=7, key=f"{industry_code}_survey_day")
    base.weekday = st.selectbox("요일", weekdays, index=weekdays.index(base.weekday), key=f"{industry_code}_weekday")
    st.checkbox("24시간 영업", value=False, key=f"{industry_code}_is_24h")
    base.region = st.selectbox("지역 권역", regions, index=regions.index(base.region), key=f"{industry_code}_region")
    base.admin_unit = st.selectbox("행정 단위", admin_units, index=admin_units.index(base.admin_unit), key=f"{industry_code}_admin_unit")
    base.operation_type = st.selectbox("운영 형태", operation_types, index=operation_types.index(base.operation_type), key=f"{industry_code}_operation_type")

tab_market, tab_traffic, tab_competitors, tab_investment, tab_result = st.tabs(
    ["상권 입력", "통행량 입력", "경쟁점 입력", "투자손익 입력", "계산 결과"]
)

with tab_market:
    st.subheader("조사치 입력 장표 - 배후 세대수")
    col1, col2, col3 = st.columns(3)
    with col1:
        base.apartment_households = st.number_input("아파트 세대수", value=float(base.apartment_households), step=10.0, key=f"{industry_code}_apartment_households")
        base.total_households = st.number_input("주택계", value=float(base.total_households), step=10.0, key=f"{industry_code}_total_households")
    with col2:
        single_households = max(base.total_households - base.apartment_households, 0)
        st.number_input("단독/다세대", value=float(single_households), step=10.0, disabled=True, key=f"{industry_code}_single_households")
        base.resident_population = st.number_input("주거인구", value=float(base.resident_population), step=10.0, key=f"{industry_code}_resident_population")
    with col3:
        base.worker_population = st.number_input("직장인구", value=float(base.worker_population), step=10.0, key=f"{industry_code}_worker_population")
        base.annual_income = st.number_input("가구당 연간 소득(만원)", value=float(base.annual_income), step=10.0, key=f"{industry_code}_annual_income")

with tab_traffic:
    st.subheader("조사치 입력 장표 - 통행량 조사")
    traffic_rows = [
        {"시간": TIME_LABELS[idx], **{AGE_COLUMNS[col]: base.traffic[idx][col] for col in range(len(AGE_COLUMNS))}}
        for idx in range(len(TIME_LABELS))
    ]
    edited_traffic = st.data_editor(traffic_rows, use_container_width=True, hide_index=True, num_rows="fixed", key=f"{industry_code}_traffic")
    if hasattr(edited_traffic, "to_dict"):
        edited_traffic = edited_traffic.to_dict("records")
    base.traffic = [
        [float(row.get(col, 0) or 0) for col in AGE_COLUMNS]
        for row in edited_traffic
    ]


def competitor_rows(items: list[Competitor]) -> list[dict]:
    return [
        {
            "점명": item.name,
            "면적(평)": item.area,
            "거리": item.distance,
            "입지": item.location,
            "시계성": item.visibility,
            "접근성": item.accessibility,
            "층": item.floor,
            "면(각)": item.sides,
            "전면 길이": item.frontage,
            "집기 설비": item.facility,
            "주차": item.parking,
            "가격": item.price,
        }
        for item in items
    ]


def rows_to_competitors(rows) -> list[Competitor]:
    if hasattr(rows, "to_dict"):
        rows = rows.to_dict("records")
    converted = []
    for row in rows:
        name = str(row.get("점명", "") or "").strip()
        if not name:
            continue
        converted.append(
            Competitor(
                name=name,
                area=float(row.get("면적(평)", 0) or 0),
                distance=float(row.get("거리", 0) or 0),
                location=float(row.get("입지", 0) or 0),
                visibility=float(row.get("시계성", 0) or 0),
                accessibility=float(row.get("접근성", 0) or 0),
                floor=float(row.get("층", 0) or 0),
                sides=float(row.get("면(각)", 0) or 0),
                frontage=float(row.get("전면 길이", 0) or 0),
                facility=float(row.get("집기 설비", 0) or 0),
                parking=float(row.get("주차", 0) or 0),
                price=float(row.get("가격", 0) or 0),
            )
        )
    return converted


with tab_competitors:
    st.subheader("조사치 입력 장표 - 직접 경쟁점")
    direct_rows = st.data_editor(
        competitor_rows(base.direct_competitors),
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key=f"{industry_code}_direct_competitors",
    )
    st.subheader("조사치 입력 장표 - 간접 경쟁점")
    indirect_rows = st.data_editor(
        competitor_rows(base.indirect_competitors),
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key=f"{industry_code}_indirect_competitors",
    )
    base.direct_competitors = rows_to_competitors(direct_rows)
    base.indirect_competitors = rows_to_competitors(indirect_rows)

with tab_investment:
    st.subheader("조사치 입력 장표 - 투자금액")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        base.deposit = st.number_input("임차보증금(천원)", value=float(base.deposit), step=100.0, key=f"{industry_code}_deposit")
    with col2:
        base.goodwill = st.number_input("영업권(천원)", value=float(base.goodwill), step=100.0, key=f"{industry_code}_goodwill")
    with col3:
        base.monthly_rent = st.number_input("월임대료(천원)", value=float(base.monthly_rent), step=100.0, key=f"{industry_code}_monthly_rent")
    with col4:
        base.management_fee = st.number_input("관리비(천원)", value=float(base.management_fee), step=10.0, key=f"{industry_code}_management_fee")

    st.subheader("투자손익 - 노란색 입력칸")
    col1, col2, col3 = st.columns(3)
    with col1:
        base.royalty_rate = st.number_input("로열티율", value=float(base.royalty_rate), min_value=0.0, max_value=1.0, step=0.005, format="%.3f", key=f"{industry_code}_royalty_rate")
        base.franchise_fee = st.number_input("가입비(천원)", value=float(base.franchise_fee), step=100.0, key=f"{industry_code}_franchise_fee")
    with col2:
        base.business_days = st.number_input("영업일수", value=float(base.business_days), min_value=1.0, max_value=31.0, step=1.0, key=f"{industry_code}_business_days")
        base.education_fee = st.number_input("교육비(천원)", value=float(base.education_fee), step=100.0, key=f"{industry_code}_education_fee")
    with col3:
        base.cogs_rate = st.number_input("평균 매출원가율", value=float(base.cogs_rate), min_value=0.0, max_value=1.0, step=0.01, format="%.2f", key=f"{industry_code}_cogs_rate")
        base.guarantee_deposit = st.number_input("보증금(천원)", value=float(base.guarantee_deposit), step=100.0, key=f"{industry_code}_guarantee_deposit")
    base.opening_promo_fee = st.number_input("개점홍보비(천원)", value=float(base.opening_promo_fee), step=100.0, key=f"{industry_code}_opening_promo_fee")

result = calculate_industry(industry_code, base)

with tab_result:
    st.subheader("계산 결과")
    metric_cols = st.columns(4)
    metric_cols[0].metric("예상 일매출액", f"{result['daily_sales_thousand']:,.2f} 천원")
    metric_cols[1].metric("월간 평균 매출액", f"{result['monthly_sales_thousand']:,.2f} 천원")
    metric_cols[2].metric("상권 유형", result["trade_area_label"])
    metric_cols[3].metric("1일 후보점 전면 통행량", f"{result['daily_traffic']:,.2f} 명")

    st.subheader("손익 요약")
    profit_cols = st.columns(4)
    profit_cols[0].metric("월 매출, VAT 제외", f"{result['monthly_sales_ex_vat_thousand']:,.2f} 천원")
    profit_cols[1].metric("매출원가", f"{result['cogs_thousand']:,.2f} 천원")
    profit_cols[2].metric("로열티", f"{result['royalty_thousand']:,.2f} 천원")
    profit_cols[3].metric("공헌이익", f"{result['contribution_profit_thousand']:,.2f} 천원")

    st.subheader("계산 분해")
    st.dataframe(
        [
            {"항목": "주고객 비율", "값": f"{result['main_customer_ratio'] * 100:,.2f}%"},
            {"항목": "후보점 경쟁력 점수", "값": f"{result['candidate_score']:,.2f}"},
            {"항목": "경쟁점 총점", "값": f"{result['total_competition_score']:,.2f}"},
            {"항목": "후보점 통행인 매출", "값": f"{result['candidate_traffic_sales']:,.2f} 원"},
            {"항목": "후보점 세대수 매출", "값": f"{result['candidate_household_sales']:,.2f} 원"},
            {"항목": "후보점 직장인구 매출", "값": f"{result['candidate_worker_sales']:,.2f} 원"},
            {"항목": "월별 보정지수", "값": f"{result['month_index']:,.6f}"},
            {"항목": "요일별 보정지수", "값": f"{result['weekday_index']:,.6f}"},
            {"항목": "초기 투자금", "값": f"{result['initial_investment_thousand']:,.2f} 천원"},
        ],
        use_container_width=True,
        hide_index=True,
    )
