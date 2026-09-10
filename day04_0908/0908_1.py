#v1
#v2
#v3
#v4

# raw_trade_data.csv 파일 활용
# HS코드가 85로 시작하는
# 반도체 + 국가명 미국 또는 베트남 + 수출금액 0보다 큰수 (실제 수출실적이 있는)
# 행만 다중 조건으로 필터링 한 뒤, 수출금액 상위 10건을 화면에 보여주고 report.csv로 저장
# streamlit 사용: streamlit run 0908_1.py

import os
import pandas as pd
import streamlit as st


# 17번째 줄을 아래 코드로 대체해 봐
current_dir = os.path.dirname(__file__) # 현재 파일(0908_1.py)의 폴더 위치 가져오기
DEFAULT_CSV_PATH = os.path.join(current_dir, "..", "common", "raw_trade_data.csv")

# 기본 파일 경로 설정 (데이터를 불러올 원본 경로와 저장할 결과 파일 경로)
REPORT_OUTPUT_PATH = "report.csv"

def load_and_filter_data(csv_path=DEFAULT_CSV_PATH):
    """
    무역 데이터를 불러와서 특정 조건에 맞게 필터링한 뒤,
    수출금액 기준 내림차순으로 정렬하여 상위 10개의 데이터를 반환하는 함수입니다.
    """
    # 지정된 경로에 CSV 파일이 실제로 존재하는지 확인합니다.
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
        
    # Pandas를 사용하여 CSV 파일을 데이터프레임(표 형태)으로 읽어옵니다.
    df = pd.read_csv(csv_path)
    
    # 조건 1: HScode가 '85'로 시작하는 데이터 (반도체류)
    # 데이터를 정확히 비교하기 위해 문자열(str)로 변환하고 양옆의 공백을 제거(strip)합니다.
    df['hs_code_str'] = df['hs_code'].astype(str).str.strip()
    cond_hscode = df['hs_code_str'].str.startswith('85')
    
    # 조건 2: 국가명이 '미국'이거나 '베트남'인 데이터
    cond_country = df['국가명'].isin(['미국', '베트남'])
    
    # 조건 3: 수출금액이 0보다 큰 데이터 (유효한 수출 건만 추출)
    cond_amount = df['수출금액'] > 0
    
    # 위에서 만든 3가지 조건을 모두 만족(&)하는 데이터만 필터링합니다.
    filtered_df = df[cond_hscode & cond_country & cond_amount]
    
    # 수출금액을 기준으로 내림차순(ascending=False, 큰 값이 위로 오게) 정렬한 후, 상위 10개(head)만 추출합니다.
    top_10 = filtered_df.sort_values(by='수출금액', ascending=False).head(10)
    
    # 필터링을 위해 임시로 만들었던 'hs_code_str' 열은 이제 필요 없으므로 삭제합니다.
    top_10 = top_10.drop(columns=['hs_code_str'])
    
    return top_10

def main():
    # 현재 코드가 Streamlit(웹 대시보드) 환경에서 실행 중인지, 
    # 아니면 일반 터미널 환경에서 실행 중인지 확인합니다.
    try:
        is_streamlit = st.runtime.exists()
    except (ImportError, AttributeError):
        is_streamlit = False

    if is_streamlit:
        # --- [STREAMLIT 대시보드 모드] ---
        # 웹 브라우저 탭의 제목과 아이콘, 레이아웃 등 웹 페이지의 기본 설정을 합니다.
        st.set_page_config(
            page_title="반도체 수출 실적 대시보드",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # HTML과 CSS를 활용하여 대시보드의 제목 폰트 크기, 색상, 디자인을 커스텀합니다.
        st.markdown("""
            <style>
            .main-title {
                font-size: 2.2rem;
                font-weight: 700;
                color: #1E3A8A;
                margin-bottom: 0.5rem;
                border-bottom: 3px solid #3B82F6;
                padding-bottom: 0.5rem;
            }
            .sub-title {
                font-size: 1.1rem;
                color: #4B5563;
                margin-bottom: 1.5rem;
            }
            </style>
        """, unsafe_allow_html=True)

        # 커스텀한 CSS 스타일을 적용하여 메인 제목과 부제목을 화면에 출력합니다.
        st.markdown("<div class='main-title'>🔌 HScode 85 (반도체류) 수출 실적 분석</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>미국 및 베트남 대상 수출금액 상위 10건 내역을 분석하고 시각화합니다.</div>", unsafe_allow_html=True)

        # --- [사이드바(왼쪽 메뉴) 설정] ---
        st.sidebar.header("🔍 필터 및 설정")
        # 데이터 파일 경로를 사용자가 직접 수정할 수 있도록 입력창을 만듭니다.
        csv_input_path = st.sidebar.text_input("데이터 CSV 경로", value=DEFAULT_CSV_PATH)
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("💡 인터랙티브 옵션")
        # 분석할 국가를 여러 개 선택할 수 있는 멀티셀렉트 박스를 만듭니다.
        selected_countries = st.sidebar.multiselect(
            "대상 국가 선택",
            options=["미국", "베트남", "중국", "일본", "독일"],
            default=["미국", "베트남"]
        )
        # 최소 수출금액과 조회할 상위 건수를 조절할 수 있는 입력창과 슬라이더를 만듭니다.
        min_amount = st.sidebar.number_input("최소 수출금액", value=0, min_value=0)
        hscode_prefix = st.sidebar.text_input("HS Code 시작값", value="85")
        top_n = st.sidebar.slider("표시할 상위 건수", min_value=5, max_value=20, value=10)

        try:
            # 1. 고정된 기준(미국/베트남, 상위 10건 등)으로 분석한 '공식 보고서' 데이터를 먼저 생성하여 로컬 파일로 저장합니다.
            standard_top_10 = load_and_filter_data(csv_input_path)
            script_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 실행 중인 파일의 폴더 경로
            standard_report_path = os.path.join(script_dir, REPORT_OUTPUT_PATH)
            standard_top_10.to_csv(standard_report_path, index=False, encoding='utf-8-sig')
            
            # 2. 사용자가 사이드바에서 조작한 조건(인터랙티브 옵션)에 맞춰 데이터를 실시간으로 다시 분석합니다.
            raw_df = pd.read_csv(csv_input_path)
            raw_df['hs_code_str'] = raw_df['hs_code'].astype(str).str.strip()
            
            # 사용자가 선택한 조건들로 필터링 로직을 다시 적용합니다.
            cond_hs = raw_df['hs_code_str'].str.startswith(hscode_prefix)
            cond_co = raw_df['국가명'].isin(selected_countries)
            cond_am = raw_df['수출금액'] > min_amount
            
            # 조건에 맞는 데이터만 추려내어 복사(copy)합니다.
            interactive_filtered = raw_df[cond_hs & cond_co & cond_am].copy()
            # 사용자가 슬라이더로 설정한 개수(top_n)만큼만 잘라냅니다.
            interactive_top = interactive_filtered.sort_values(by='수출금액', ascending=False).head(top_n)
            interactive_top = interactive_top.drop(columns=['hs_code_str'])
            
            # --- [데이터 시각화 및 주요 지표 표시] ---
            # 화면을 3개의 열(column)로 나누어 핵심 수치를 눈에 띄게 보여줍니다.
            col1, col2, col3 = st.columns(3)
            with col1:
                total_export = interactive_top['수출금액'].sum()
                st.metric(
                    label=f"상위 {len(interactive_top)}건 총 수출액", 
                    value=f"${total_export:,.0f}" # 숫자에 천 단위 콤마를 찍어서 표시합니다.
                )
            with col2:
                avg_weight = interactive_top['중량'].mean()
                st.metric(
                    label="평균 중량", 
                    value=f"{avg_weight:,.2f} kg"
                )
            with col3:
                st.metric(
                    label="조회된 데이터 수", 
                    value=f"{len(interactive_top)} 건"
                )

            # 필터링된 데이터프레임을 웹 화면에 표 형태로 깔끔하게 출력합니다.
            st.subheader(f"📋 수출금액 상위 {len(interactive_top)}건 상세 내역")
            styled_df = interactive_top.style.format({
                '수출금액': '${:,.0f}',
                '중량': '{:,.2f} kg'
            })
            st.dataframe(styled_df, use_container_width=True)

            # 공식 보고서가 성공적으로 저장되었음을 알리는 메시지를 띄웁니다.
            st.success(f"✅ 필터링된 공식 상위 10건 데이터가 로컬 파일 `{standard_report_path}`로 자동 저장되었습니다.")

            # 사용자가 현재 웹에서 보고 있는 조건의 데이터를 CSV로 다운로드할 수 있는 버튼을 제공합니다.
            csv_data = interactive_top.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 현재 필터링된 데이터 다운로드 (CSV)",
                data=csv_data,
                file_name="filtered_trade_report.csv",
                mime="text/csv"
            )

            # --- [그래프 시각화] ---
            if not interactive_top.empty:
                st.subheader("📊 국가 및 날짜별 수출금액 시각화")
                # 국가별 총 수출금액을 계산하기 위해 그룹화(groupby)합니다.
                country_summary = interactive_top.groupby('국가명')['수출금액'].sum().reset_index()
                
                # 차트를 나란히 배치하기 위해 열을 2개로 나눕니다.
                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    st.write("**국가별 수출금액 합계 (막대 그래프)**")
                    st.bar_chart(data=country_summary, x='국가명', y='수출금액', use_container_width=True)
                with chart_col2:
                    st.write("**날짜별 수출 실적 추이 (선 그래프)**")
                    # 시계열 추이를 보기 위해 날짜순으로 데이터를 먼저 정렬합니다.
                    date_sorted_top = interactive_top.sort_values('날짜')
                    st.line_chart(data=date_sorted_top, x='날짜', y='수출금액', color='국가명', use_container_width=True)

        except Exception as e:
            # 오류가 발생했을 때 사용자에게 에러 메시지를 보여줍니다.
            st.error(f"데이터를 처리하는 도중 에러가 발생했습니다: {e}")
            st.info("올바른 CSV 파일 경로가 지정되었는지 기입 상자와 사이드바를 확인해 주세요.")

    else:
        # --- [터미널 모드 (일반 실행)] ---
        # Streamlit 명령어(streamlit run)가 아닌 일반 파이썬 명령어(python 0908_1.py)로 실행했을 때 동작하는 부분입니다.
        print("=" * 60)
        print(" [반도체 수출 실적 데이터 분석 - 일반 터미널 모드] ")
        print("=" * 60)
        try:
            print(f"1. 데이터 로드 및 필터링 진행 중... (대상: {DEFAULT_CSV_PATH})")
            top_10 = load_and_filter_data(DEFAULT_CSV_PATH)
            
            print("\n2. 수출금액 상위 10건 필터링 결과:")
            print(top_10.to_string(index=False)) # 터미널 창에 표 형태로 데이터를 출력합니다.
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            standard_report_path = os.path.join(script_dir, REPORT_OUTPUT_PATH)
            print(f"\n3. 결과를 로컬 파일 `{standard_report_path}`에 저장하는 중...")
            top_10.to_csv(standard_report_path, index=False, encoding='utf-8-sig')
            print("▶ 저장 완료!")
            
            # 대시보드로 보는 방법을 안내합니다.
            print("\n[안내] 시각화 대시보드를 실행하려면 터미널에 아래 명령어를 입력하세요:")
            print(f"  streamlit run {os.path.basename(__file__)}")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n[에러] 처리 도중 오류가 발생했습니다: {e}")
            print("=" * 60)

# 이 파이썬 파일이 직접 실행될 때만 main() 함수를 호출하라는 의미입니다.
if __name__ == "__main__":
    main()