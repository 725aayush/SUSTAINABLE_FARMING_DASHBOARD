document.addEventListener('DOMContentLoaded', function () {
    // Handle form submission
    document.getElementById('farmerForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const farmerName = document.getElementById('farmerName').value;
        const city = document.getElementById('city').value || "";

        fetch('/submit_farmer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: farmerName,
                city: city
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('statusMessage').innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            } else {
                document.getElementById('statusMessage').innerHTML = `<div class="alert alert-success">${data.message}</div>`;
                pollForUpdates();
            }
        })
        .catch(err => {
            console.error("Submit error:", err);
        });
    });

    // Export recommendations
    document.getElementById('exportBtn')?.addEventListener('click', function () {
        fetch('/export_recommendations')
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'farm_recommendations.xlsx';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            });
    });

    // Polling for updates
    function pollForUpdates() {
        fetch('/get_updates')
            .then(response => response.json())
            .then(data => {
                console.log("Update data:", data);
                updateWeatherUI(data.weather);
                updateRecommendationsUI(data.recommendations);
                updateMarketUI(data.market_data);
                setTimeout(pollForUpdates, 5000);
            })
            .catch(err => {
                console.error("Polling error:", err);
                setTimeout(pollForUpdates, 10000); // Retry slower on failure
            });
    }

    function updateWeatherUI(weather) {
        if (!weather) return;

        document.getElementById('weatherTemp').textContent = `${weather.temp}°C`;
        document.getElementById('weatherCondition').textContent = weather.condition;
        document.getElementById('weatherHumidity').textContent = weather.humidity;
        document.getElementById('weatherWind').textContent = weather.wind;

        const condition = weather.condition.toLowerCase();
        let iconClass = 'fa-cloud';
        if (condition.includes('sun') || condition.includes('clear')) {
            iconClass = 'fa-sun';
        } else if (condition.includes('rain')) {
            iconClass = 'fa-cloud-rain';
        }

        document.getElementById('weatherIcon').innerHTML =
            `<i class="fas ${iconClass} fa-3x text-secondary"></i>`;
    }

    function updateRecommendationsUI(recommendations) {
        const container = document.querySelector('#recommendationsContainer');
        if (!container) return;

        if (!recommendations || recommendations.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-seedling fa-4x text-muted mb-3"></i>
                    <p class="text-muted">No recommendations yet. Submit farmer information to get started.</p>
                </div>`;
            return;
        }

        let html = '';
        recommendations.forEach(rec => {
            const timestamp = rec.timestamp ? new Date(rec.timestamp).toLocaleString() : 'Just now';
            html += `
                <div class="card mb-3 new-data">
                    <div class="card-header">
                        <h6>Recommendation for ${rec.farmer}</h6>
                    </div>
                    <div class="card-body">
                        <p class="card-text">${rec.suggestion}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge bg-primary">Score: ${rec.score}</span>
                            <small class="text-muted">${timestamp}</small>
                        </div>
                    </div>
                </div>`;
        });

        container.innerHTML = html;
    }

    function updateMarketUI(marketData) {
        const tableBody = document.getElementById('marketTable');
        if (!tableBody) return;

        if (!marketData || marketData.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="3" class="text-center py-4 text-muted">No market data available</td>
                </tr>`;
            return;
        }

        let html = '';
        marketData.forEach(item => {
            let demandBadge = '<span class="badge bg-secondary">Low</span>';
            if (item.demand === 'High') {
                demandBadge = '<span class="badge bg-danger">High</span>';
            } else if (item.demand === 'Medium') {
                demandBadge = '<span class="badge bg-warning text-dark">Medium</span>';
            }

            html += `
                <tr class="new-data">
                    <td>${item.product}</td>
                    <td>₹${item.price.toLocaleString()}</td>
                    <td>${demandBadge}</td>
                </tr>`;
        });

        tableBody.innerHTML = html;

        fetch('/get_market_chart')
            .then(response => response.json())
            .then(data => {
                if (data.chart) {
                    document.getElementById('marketChart').innerHTML =
                        `<img src="data:image/png;base64,${data.chart}" class="img-fluid" alt="Profitability Chart">`;
                }
            });
    }
});

