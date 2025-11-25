"""
VIX 로보 어드바이저 Flask 애플리케이션
"""

from flask import Flask, render_template, jsonify, request
from robo_advisor import VIXRoboAdvisor
import os

app = Flask(__name__)
advisor = VIXRoboAdvisor()


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/api/recommendation', methods=['GET'])
def get_recommendation():
    """주간 포트폴리오 추천 API"""
    try:
        recommendation = advisor.get_weekly_recommendation()
        return jsonify(recommendation)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    """현재 시장 데이터 API"""
    try:
        market_data = advisor.get_current_data()
        return jsonify({
            'success': True,
            'data': market_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/allocation/<float:vix_value>', methods=['GET'])
def get_allocation(vix_value):
    """특정 VIX 값에 대한 포트폴리오 배분 API"""
    try:
        allocation, strategy, description, risk_level = advisor.calculate_allocation(vix_value)
        return jsonify({
            'success': True,
            'vix_value': vix_value,
            'allocation': allocation,
            'strategy': strategy,
            'description': description,
            'risk_level': risk_level
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/portfolio-calculator', methods=['POST'])
def calculate_portfolio():
    """포트폴리오 가치 계산 API"""
    try:
        data = request.json
        initial_investment = float(data.get('investment', 10000))

        # 현재 시장 데이터 가져오기
        market_data = advisor.get_current_data()
        vix_value = market_data['vix']['value']
        spy_price = market_data['spy']['value']
        qqq_price = market_data['qqq']['value']

        # 포트폴리오 배분 계산
        allocation, strategy, description, risk_level = advisor.calculate_allocation(vix_value)

        # 포트폴리오 가치 계산
        portfolio = advisor.calculate_portfolio_value(
            initial_investment, allocation, spy_price, qqq_price
        )

        return jsonify({
            'success': True,
            'market_data': market_data,
            'strategy': strategy,
            'description': description,
            'risk_level': risk_level,
            'portfolio': portfolio
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/vix-history/<int:days>', methods=['GET'])
def get_vix_history(days):
    """VIX 히스토리 데이터 API"""
    try:
        history = advisor.get_vix_history(days)
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """헬스 체크 엔드포인트"""
    return jsonify({
        'status': 'healthy',
        'service': 'VIX Robo Advisor'
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
