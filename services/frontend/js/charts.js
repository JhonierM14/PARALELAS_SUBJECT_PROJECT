async function loadData() {
    const response = await fetch('http://127.0.0.1:5000/correlation');
    const data = await response.json();
    const labels = data.data_points.map(dp => dp.date);
    const events = data.data_points.map(dp => dp.event_count);
    const icolcap = data.data_points.map(dp => dp.icolcap);

    const ctx = document.getElementById('correlationChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                { label: 'Eventos', data: events, borderColor: 'red', fill: false },
                { label: 'ICOLCAP', data: icolcap, borderColor: 'blue', fill: false }
            ]
        }
    });
}

loadData();
