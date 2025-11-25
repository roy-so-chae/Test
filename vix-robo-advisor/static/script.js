// 전역 변수
let allocationChart = null;
let vixHistoryChart = null;
let currentRecommendation = null;

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', function() {
    loadRecommendation();

    // 새로고침 버튼
    document.getElementById('refresh-btn').addEventListener('click', function() {
        loadRecommendation();
    });

    // 계산 버튼
    document.getElementById('calculate-btn').addEventListener('click', function() {
        calculatePortfolio();
    });
});

// 추천 데이터 로드
async function loadRecommendation() {
    showLoading(true);

    try {
        const response = await fetch('/api/recommendation');
        const data = await response.json();

        if (data.success) {
            currentRecommendation = data;
            updateUI(data);
            showLoading(false);
        } else {
            showError(data.error || '데이터를 불러올 수 없습니다.');
        }
    } catch (error) {
        showError('서버 연결에 실패했습니다: ' + error.message);
    }
}

// UI 업데이트
function updateUI(data) {
    // 시장 데이터 업데이트
    updateMarketData(data.market_data);

    // 전략 정보 업데이트
    updateStrategy(data);

    // 포트폴리오 배분 업데이트
    updateAllocation(data.allocation);

    // VIX 히스토리 차트 업데이트
    updateVixHistory(data.vix_history);

    // 추천 날짜
    document.getElementById('recommendation-date').textContent =
        `추천일: ${data.recommendation_date}`;
}

// 시장 데이터 업데이트
function updateMarketData(marketData) {
    // VIX
    document.getElementById('vix-value').textContent = marketData.vix.value.toFixed(2);
    const vixChange = document.getElementById('vix-change');
    vixChange.textContent = `${marketData.vix.change >= 0 ? '+' : ''}${marketData.vix.change}%`;
    vixChange.className = `card-change ${marketData.vix.change >= 0 ? 'positive' : 'negative'}`;

    // SPY
    document.getElementById('spy-value').textContent = `$${marketData.spy.value.toFixed(2)}`;
    const spyChange = document.getElementById('spy-change');
    spyChange.textContent = `${marketData.spy.change >= 0 ? '+' : ''}${marketData.spy.change}%`;
    spyChange.className = `card-change ${marketData.spy.change >= 0 ? 'positive' : 'negative'}`;

    // QQQ
    document.getElementById('qqq-value').textContent = `$${marketData.qqq.value.toFixed(2)}`;
    const qqqChange = document.getElementById('qqq-change');
    qqqChange.textContent = `${marketData.qqq.change >= 0 ? '+' : ''}${marketData.qqq.change}%`;
    qqqChange.className = `card-change ${marketData.qqq.change >= 0 ? 'positive' : 'negative'}`;

    // 업데이트 시간
    document.getElementById('update-time').textContent = `업데이트: ${marketData.timestamp}`;
}

// 전략 정보 업데이트
function updateStrategy(data) {
    document.getElementById('strategy-name').textContent = data.strategy;
    document.getElementById('risk-level').textContent = `위험도: ${data.risk_level}`;
    document.getElementById('strategy-description').textContent = data.description;
}

// 포트폴리오 배분 업데이트
function updateAllocation(allocation) {
    // 배분 비율 텍스트
    document.getElementById('cash-allocation').textContent = `${allocation.cash}%`;
    document.getElementById('spy-allocation').textContent = `${allocation.spy}%`;
    document.getElementById('qqq-allocation').textContent = `${allocation.qqq}%`;

    // 차트 업데이트
    updateAllocationChart(allocation);
}

// 포트폴리오 배분 차트
function updateAllocationChart(allocation) {
    const ctx = document.getElementById('allocationChart').getContext('2d');

    // 기존 차트 제거
    if (allocationChart) {
        allocationChart.destroy();
    }

    allocationChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['현금', 'SPY', 'QQQ'],
            datasets: [{
                data: [allocation.cash, allocation.spy, allocation.qqq],
                backgroundColor: [
                    'rgb(16, 185, 129)',  // cash
                    'rgb(59, 130, 246)',   // spy
                    'rgb(139, 92, 246)'    // qqq
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed + '%';
                        }
                    }
                }
            }
        }
    });
}

// VIX 히스토리 차트
function updateVixHistory(history) {
    const ctx = document.getElementById('vixHistoryChart').getContext('2d');

    // 기존 차트 제거
    if (vixHistoryChart) {
        vixHistoryChart.destroy();
    }

    const labels = history.map(item => item.date);
    const values = history.map(item => item.value);

    vixHistoryChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'VIX 지수',
                data: values,
                borderColor: 'rgb(139, 92, 246)',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        display: false
                    }
                },
                y: {
                    display: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            }
        }
    });
}

// 포트폴리오 계산
async function calculatePortfolio() {
    const investment = parseFloat(document.getElementById('investment-amount').value);

    if (isNaN(investment) || investment < 100) {
        alert('최소 투자 금액은 $100입니다.');
        return;
    }

    try {
        const response = await fetch('/api/portfolio-calculator', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ investment: investment })
        });

        const data = await response.json();

        if (data.success) {
            displayPortfolioResult(data.portfolio);
        } else {
            alert('계산 중 오류가 발생했습니다: ' + data.error);
        }
    } catch (error) {
        alert('서버 연결에 실패했습니다: ' + error.message);
    }
}

// 포트폴리오 계산 결과 표시
function displayPortfolioResult(portfolio) {
    document.getElementById('calc-cash').textContent =
        `$${portfolio.cash.amount.toLocaleString()}`;

    document.getElementById('calc-spy').textContent =
        `$${portfolio.spy.amount.toLocaleString()} (${portfolio.spy.shares.toFixed(2)} 주)`;

    document.getElementById('calc-qqq').textContent =
        `$${portfolio.qqq.amount.toLocaleString()} (${portfolio.qqq.shares.toFixed(2)} 주)`;

    document.getElementById('calc-total').textContent =
        `$${portfolio.total.toLocaleString()}`;

    document.getElementById('portfolio-result').style.display = 'block';
}

// 로딩 표시
function showLoading(show) {
    const loading = document.getElementById('loading');
    const content = document.getElementById('content');

    if (show) {
        loading.style.display = 'block';
        content.style.display = 'none';
    } else {
        loading.style.display = 'none';
        content.style.display = 'block';
    }
}

// 에러 표시
function showError(message) {
    showLoading(false);
    alert('오류: ' + message);
}
