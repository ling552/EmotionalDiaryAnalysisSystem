function safeParseJson(scriptId) {
  const el = document.getElementById(scriptId);
  if (!el) return null;
  try {
    return JSON.parse(el.textContent || '{}');
  } catch (e) {
    return null;
  }
}

function pastelColor(alpha) {
  return `rgba(142, 203, 255, ${alpha})`;
}

function pastelPink(alpha) {
  return `rgba(255, 180, 217, ${alpha})`;
}

export function renderEmotionCharts() {
  const payload = safeParseJson('chart-data');
  if (!payload) return;

  const lineCanvas = document.getElementById('scoreLine');
  const pieCanvas = document.getElementById('emotionPie');

  if (lineCanvas && payload.labels && payload.scores) {
    // eslint-disable-next-line no-undef
    new Chart(lineCanvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: payload.labels,
        datasets: [
          {
            label: '情绪得分',
            data: payload.scores,
            borderColor: 'rgba(93, 182, 255, 1)',
            backgroundColor: 'rgba(142, 203, 255, .35)',
            tension: 0.35,
            fill: true,
            pointRadius: 3,
            pointBackgroundColor: 'rgba(255, 134, 196, 1)',
            pointBorderColor: 'rgba(255, 255, 255, 1)',
            pointBorderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: {
            grid: { color: 'rgba(16, 24, 40, .06)' },
            ticks: { color: 'rgba(31, 41, 55, .75)' },
          },
          y: {
            grid: { color: 'rgba(16, 24, 40, .06)' },
            ticks: { color: 'rgba(31, 41, 55, .75)' },
          },
        },
      },
    });
  }

  if (pieCanvas && payload.emotion_counts) {
    const labels = Object.keys(payload.emotion_counts);
    const values = labels.map((k) => payload.emotion_counts[k]);

    const colors = labels.map((_, i) => (i % 2 === 0 ? pastelColor(0.65) : pastelPink(0.65)));
    const borderColors = labels.map((_, i) => (i % 2 === 0 ? 'rgba(93, 182, 255, 1)' : 'rgba(255, 134, 196, 1)'));

    // eslint-disable-next-line no-undef
    new Chart(pieCanvas.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels,
        datasets: [
          {
            data: values,
            backgroundColor: colors,
            borderColor: borderColors,
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              color: 'rgba(31, 41, 55, .78)',
              font: { weight: '700' },
            },
          },
        },
      },
    });
  }
}
