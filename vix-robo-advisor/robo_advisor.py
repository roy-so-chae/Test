"""
VIX 기반 로보 어드바이저
VIX 지수를 기반으로 현금, SPY, QQQ의 포트폴리오 비율을 계산합니다.
"""

import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Tuple


class VIXRoboAdvisor:
    """VIX 지수 기반 포트폴리오 배분 로보 어드바이저"""

    def __init__(self):
        self.vix_symbol = "^VIX"
        self.spy_symbol = "SPY"
        self.qqq_symbol = "QQQ"

    def get_current_data(self) -> Dict:
        """현재 VIX, SPY, QQQ 데이터를 가져옵니다."""
        try:
            # VIX 데이터
            vix = yf.Ticker(self.vix_symbol)
            vix_data = vix.history(period="5d")

            # SPY 데이터
            spy = yf.Ticker(self.spy_symbol)
            spy_data = spy.history(period="5d")

            # QQQ 데이터
            qqq = yf.Ticker(self.qqq_symbol)
            qqq_data = qqq.history(period="5d")

            if vix_data.empty or spy_data.empty or qqq_data.empty:
                raise ValueError("데이터를 가져올 수 없습니다.")

            current_vix = round(vix_data['Close'].iloc[-1], 2)
            current_spy = round(spy_data['Close'].iloc[-1], 2)
            current_qqq = round(qqq_data['Close'].iloc[-1], 2)

            # 주간 변화율 계산 (5일 기준)
            vix_change = round(((current_vix - vix_data['Close'].iloc[0]) / vix_data['Close'].iloc[0]) * 100, 2)
            spy_change = round(((current_spy - spy_data['Close'].iloc[0]) / spy_data['Close'].iloc[0]) * 100, 2)
            qqq_change = round(((current_qqq - qqq_data['Close'].iloc[0]) / qqq_data['Close'].iloc[0]) * 100, 2)

            return {
                'vix': {
                    'value': current_vix,
                    'change': vix_change
                },
                'spy': {
                    'value': current_spy,
                    'change': spy_change
                },
                'qqq': {
                    'value': current_qqq,
                    'change': qqq_change
                },
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            raise Exception(f"데이터 가져오기 실패: {str(e)}")

    def calculate_allocation(self, vix_value: float) -> Tuple[Dict, str, str]:
        """
        VIX 값을 기반으로 포트폴리오 배분을 계산합니다.

        Returns:
            allocation (Dict): 자산별 배분 비율
            strategy (str): 전략 이름
            description (str): 전략 설명
        """
        if vix_value < 15:
            # 낮은 변동성 - 공격적 포트폴리오
            allocation = {
                'cash': 10,
                'spy': 50,
                'qqq': 40
            }
            strategy = "공격적 (Aggressive)"
            description = "시장 변동성이 낮아 위험자산 비중을 높입니다. 기술주(QQQ) 비중이 높습니다."
            risk_level = "높음"

        elif 15 <= vix_value < 20:
            # 정상 변동성 - 균형 포트폴리오
            allocation = {
                'cash': 20,
                'spy': 45,
                'qqq': 35
            }
            strategy = "균형 (Balanced)"
            description = "정상적인 시장 변동성으로 균형잡힌 포트폴리오를 유지합니다."
            risk_level = "중간"

        elif 20 <= vix_value < 30:
            # 높은 변동성 - 보수적 포트폴리오
            allocation = {
                'cash': 40,
                'spy': 40,
                'qqq': 20
            }
            strategy = "보수적 (Conservative)"
            description = "변동성이 높아져 현금 비중을 늘리고 안전자산 위주로 운용합니다."
            risk_level = "낮음"

        else:  # vix_value >= 30
            # 극도의 변동성 - 매우 보수적
            allocation = {
                'cash': 60,
                'spy': 30,
                'qqq': 10
            }
            strategy = "매우 보수적 (Very Conservative)"
            description = "극도의 시장 변동성으로 현금 비중을 대폭 늘리고 방어적으로 운용합니다."
            risk_level = "매우 낮음"

        return allocation, strategy, description, risk_level

    def get_weekly_recommendation(self) -> Dict:
        """주간 포트폴리오 추천을 생성합니다."""
        try:
            # 현재 데이터 가져오기
            market_data = self.get_current_data()
            vix_value = market_data['vix']['value']

            # 포트폴리오 배분 계산
            allocation, strategy, description, risk_level = self.calculate_allocation(vix_value)

            # VIX 히스토리 (30일)
            vix_history = self.get_vix_history(30)

            return {
                'success': True,
                'market_data': market_data,
                'allocation': allocation,
                'strategy': strategy,
                'description': description,
                'risk_level': risk_level,
                'vix_history': vix_history,
                'recommendation_date': datetime.now().strftime('%Y년 %m월 %d일')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_vix_history(self, days: int = 30) -> list:
        """VIX 히스토리 데이터를 가져옵니다."""
        try:
            vix = yf.Ticker(self.vix_symbol)
            vix_data = vix.history(period=f"{days}d")

            history = []
            for date, row in vix_data.iterrows():
                history.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'value': round(row['Close'], 2)
                })

            return history
        except Exception as e:
            return []

    def calculate_portfolio_value(self, initial_investment: float, allocation: Dict,
                                 spy_price: float, qqq_price: float) -> Dict:
        """
        포트폴리오 가치 계산

        Args:
            initial_investment: 초기 투자금
            allocation: 자산 배분 비율
            spy_price: SPY 현재 가격
            qqq_price: QQQ 현재 가격

        Returns:
            각 자산별 투자 금액과 수량
        """
        cash_amount = initial_investment * (allocation['cash'] / 100)
        spy_amount = initial_investment * (allocation['spy'] / 100)
        qqq_amount = initial_investment * (allocation['qqq'] / 100)

        spy_shares = spy_amount / spy_price
        qqq_shares = qqq_amount / qqq_price

        return {
            'cash': {
                'amount': round(cash_amount, 2),
                'percentage': allocation['cash']
            },
            'spy': {
                'amount': round(spy_amount, 2),
                'shares': round(spy_shares, 4),
                'price': spy_price,
                'percentage': allocation['spy']
            },
            'qqq': {
                'amount': round(qqq_amount, 2),
                'shares': round(qqq_shares, 4),
                'price': qqq_price,
                'percentage': allocation['qqq']
            },
            'total': round(initial_investment, 2)
        }
