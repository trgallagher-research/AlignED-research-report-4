/**
 * AlignED Report 4 — Charts
 * Renders Chart.js charts on the results page.
 * Data: 2 models x 3 conditions, output scores and trace scores.
 */
document.addEventListener('DOMContentLoaded', function() {
  /* Only render charts on the results page */
  if (document.body.dataset.page !== 'results') return;

  /* Colour scheme: one colour per model */
  var COLOURS = {
    claude: {
      fill: 'rgba(59, 107, 154, 0.75)',
      border: '#3B6B9A'
    },
    gemini: {
      fill: 'rgba(182, 125, 92, 0.75)',
      border: '#B67D5C'
    }
  };

  /* Condition labels for x-axis */
  var conditionLabels = ['A: Unprompted', 'B: General CLT', 'C: Specific fading'];

  /* Score data */
  var claudeOutput = [0, 0, 2];
  var geminiOutput = [0, 1, 2];
  var claudeTrace  = [0, 2, 1];
  var geminiTrace  = [0, 2, 2];

  /* Shared chart options */
  var sharedOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        max: 2,
        ticks: {
          stepSize: 1,
          font: { family: "'Inter', sans-serif", size: 12 }
        },
        title: {
          display: true,
          text: 'Score (0\u20132)',
          font: { family: "'Inter', sans-serif", size: 13, weight: '600' }
        }
      },
      x: {
        ticks: {
          font: { family: "'Inter', sans-serif", size: 12 }
        }
      }
    },
    plugins: {
      legend: {
        labels: {
          font: { family: "'Inter', sans-serif", size: 13 },
          usePointStyle: true,
          pointStyle: 'rectRounded'
        }
      },
      tooltip: {
        titleFont: { family: "'Inter', sans-serif" },
        bodyFont: { family: "Georgia, serif" }
      }
    }
  };

  /* Chart 1: Output scores by condition */
  var outputCtx = document.getElementById('chart-output-scores');
  if (outputCtx) {
    new Chart(outputCtx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: conditionLabels,
        datasets: [
          {
            label: 'Claude Opus 4.6',
            data: claudeOutput,
            backgroundColor: COLOURS.claude.fill,
            borderColor: COLOURS.claude.border,
            borderWidth: 2,
            borderRadius: 4
          },
          {
            label: 'Gemini 3.1 Pro',
            data: geminiOutput,
            backgroundColor: COLOURS.gemini.fill,
            borderColor: COLOURS.gemini.border,
            borderWidth: 2,
            borderRadius: 4
          }
        ]
      },
      options: sharedOptions
    });
  }

  /* Chart 2: Trace scores by condition */
  var traceCtx = document.getElementById('chart-trace-scores');
  if (traceCtx) {
    new Chart(traceCtx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: conditionLabels,
        datasets: [
          {
            label: 'Claude Opus 4.6',
            data: claudeTrace,
            backgroundColor: COLOURS.claude.fill,
            borderColor: COLOURS.claude.border,
            borderWidth: 2,
            borderRadius: 4
          },
          {
            label: 'Gemini 3.1 Pro',
            data: geminiTrace,
            backgroundColor: COLOURS.gemini.fill,
            borderColor: COLOURS.gemini.border,
            borderWidth: 2,
            borderRadius: 4
          }
        ]
      },
      options: sharedOptions
    });
  }
});
