/**
 * AlignED Report 4 — Dumbbell Chart
 * Single chart showing output vs trace scores for each model-condition pair.
 * The connecting line between dots encodes the knowledge-application gap.
 *
 * Data: 2 models x 3 conditions, scored on output (0-2) and trace (0-2).
 */
document.addEventListener('DOMContentLoaded', function() {
  /* Only render on the results page */
  if (document.body.dataset.page !== 'results') return;

  var canvas = document.getElementById('chart-dumbbell');
  if (!canvas) return;

  /* Colours: output = primary blue, trace = terracotta */
  var OUTPUT_COLOUR = '#3B6B9A';
  var TRACE_COLOUR = '#B67D5C';
  var LINE_COLOUR = '#C0BDB7';

  /* Row labels (bottom to top, since Chart.js y-axis goes upward) */
  var labels = [
    'Gemini — C: Specific fading',
    'Gemini — B: General CLT',
    'Gemini — A: Unprompted',
    'Claude — C: Specific fading',
    'Claude — B: General CLT',
    'Claude — A: Unprompted'
  ];

  /* Scores: [output, trace] for each row (same order as labels) */
  var data = [
    { output: 2, trace: 2 },  /* Gemini C */
    { output: 1, trace: 2 },  /* Gemini B */
    { output: 0, trace: 0 },  /* Gemini A */
    { output: 2, trace: 1 },  /* Claude C */
    { output: 0, trace: 2 },  /* Claude B */
    { output: 0, trace: 0 }   /* Claude A */
  ];

  /* Build scatter datasets for output dots and trace dots */
  var outputPoints = data.map(function(d, i) { return { x: d.output, y: i }; });
  var tracePoints = data.map(function(d, i) { return { x: d.trace, y: i }; });

  /**
   * Custom plugin to draw connecting lines between output and trace dots.
   * This runs before the scatter points are drawn so dots sit on top of lines.
   */
  var dumbbellLinePlugin = {
    id: 'dumbbellLines',
    beforeDatasetsDraw: function(chart) {
      var ctx = chart.ctx;
      var xScale = chart.scales.x;
      var yScale = chart.scales.y;

      ctx.save();
      ctx.strokeStyle = LINE_COLOUR;
      ctx.lineWidth = 3;
      ctx.lineCap = 'round';

      data.forEach(function(d, i) {
        var x1 = xScale.getPixelForValue(d.output);
        var x2 = xScale.getPixelForValue(d.trace);
        var y = yScale.getPixelForValue(i);

        ctx.beginPath();
        ctx.moveTo(x1, y);
        ctx.lineTo(x2, y);
        ctx.stroke();
      });

      ctx.restore();
    }
  };

  /**
   * Custom plugin to highlight the Condition B rows with a subtle
   * background band, drawing the eye to the knowledge-application gap.
   */
  var highlightPlugin = {
    id: 'conditionBHighlight',
    beforeDraw: function(chart) {
      var ctx = chart.ctx;
      var yScale = chart.scales.y;
      var chartArea = chart.chartArea;

      /* Condition B rows are at index 1 (Gemini B) and 4 (Claude B) */
      var highlightRows = [1, 4];
      var bandHeight = 28;

      ctx.save();
      ctx.fillStyle = 'rgba(254, 243, 199, 0.45)';

      highlightRows.forEach(function(rowIndex) {
        var yPixel = yScale.getPixelForValue(rowIndex);
        ctx.fillRect(
          chartArea.left,
          yPixel - bandHeight / 2,
          chartArea.right - chartArea.left,
          bandHeight
        );
      });

      ctx.restore();
    }
  };

  new Chart(canvas.getContext('2d'), {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Output score',
          data: outputPoints,
          backgroundColor: OUTPUT_COLOUR,
          borderColor: OUTPUT_COLOUR,
          pointRadius: 8,
          pointHoverRadius: 10,
          pointStyle: 'circle'
        },
        {
          label: 'Trace score',
          data: tracePoints,
          backgroundColor: TRACE_COLOUR,
          borderColor: TRACE_COLOUR,
          pointRadius: 8,
          pointHoverRadius: 10,
          pointStyle: 'circle'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      scales: {
        x: {
          min: -0.2,
          max: 2.2,
          ticks: {
            stepSize: 1,
            callback: function(value) {
              if (value === 0) return '0';
              if (value === 1) return '1';
              if (value === 2) return '2';
              return '';
            },
            font: { family: "'Inter', sans-serif", size: 13 }
          },
          title: {
            display: true,
            text: 'Score (0\u20132)',
            font: { family: "'Inter', sans-serif", size: 13, weight: '600' }
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.06)'
          }
        },
        y: {
          type: 'linear',
          min: -0.5,
          max: 5.5,
          reverse: false,
          ticks: {
            stepSize: 1,
            callback: function(value) {
              return labels[value] || '';
            },
            font: { family: "'Inter', sans-serif", size: 12 },
            color: '#2D3748'
          },
          grid: {
            display: false
          }
        }
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            font: { family: "'Inter', sans-serif", size: 13 },
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 20
          }
        },
        tooltip: {
          titleFont: { family: "'Inter', sans-serif" },
          bodyFont: { family: "Georgia, serif" },
          callbacks: {
            title: function(items) {
              if (items.length > 0) {
                var rowIndex = items[0].parsed.y;
                return labels[rowIndex] || '';
              }
              return '';
            },
            label: function(item) {
              return item.dataset.label + ': ' + item.parsed.x;
            }
          }
        }
      }
    },
    plugins: [dumbbellLinePlugin, highlightPlugin]
  });
});
