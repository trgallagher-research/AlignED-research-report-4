/**
 * AlignED Report 4 — Dumbbell Chart
 * Single chart showing output vs trace scores for each model-condition pair.
 * The connecting line between dots encodes the knowledge-application gap.
 *
 * Data: 2 models x 3 conditions, scored on output (0-2) and trace (0-2).
 * Legend is rendered as HTML above the chart. The chart's built-in legend
 * is disabled to avoid duplication.
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

  /*
   * Row layout (bottom to top on chart):
   * 0: Claude — A: Unprompted
   * 1: Claude — B: General CLT        (highlighted)
   * 2: Claude — C: Specific fading
   * 3: (gap between model groups)
   * 4: Gemini — A: Unprompted
   * 5: Gemini — B: General CLT         (highlighted)
   * 6: Gemini — C: Specific fading
   */
  var ROW_COUNT = 7;
  var GAP_ROW = 3;

  /* Full labels for each row, displayed on the y-axis */
  var rowLabels = {
    0: 'Claude — A: Unprompted',
    1: 'Claude — B: General CLT',
    2: 'Claude — C: Specific fading',
    4: 'Gemini — A: Unprompted',
    5: 'Gemini — B: General CLT',
    6: 'Gemini — C: Specific fading'
  };

  /* Data keyed by row index: { output, trace } */
  var rowData = {
    0: { output: 0, trace: 0 },  /* Claude A */
    1: { output: 0, trace: 2 },  /* Claude B */
    2: { output: 2, trace: 1 },  /* Claude C */
    4: { output: 0, trace: 0 },  /* Gemini A */
    5: { output: 1, trace: 2 },  /* Gemini B */
    6: { output: 2, trace: 2 }   /* Gemini C */
  };

  /* Condition B rows for highlighting */
  var HIGHLIGHT_ROWS = [1, 5];

  /* Build scatter points */
  var outputPoints = [];
  var tracePoints = [];
  Object.keys(rowData).forEach(function(key) {
    var i = parseInt(key);
    var d = rowData[i];
    outputPoints.push({ x: d.output, y: i });
    tracePoints.push({ x: d.trace, y: i });
  });

  /**
   * Plugin: draw connecting lines between output and trace dots.
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

      Object.keys(rowData).forEach(function(key) {
        var i = parseInt(key);
        var d = rowData[i];
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
   * Plugin: highlight Condition B rows and draw separator line.
   */
  var annotationPlugin = {
    id: 'annotations',
    beforeDraw: function(chart) {
      var ctx = chart.ctx;
      var yScale = chart.scales.y;
      var chartArea = chart.chartArea;
      var bandHeight = 28;

      ctx.save();

      /* Highlight Condition B rows */
      ctx.fillStyle = 'rgba(254, 243, 199, 0.5)';
      HIGHLIGHT_ROWS.forEach(function(rowIndex) {
        var yPixel = yScale.getPixelForValue(rowIndex);
        ctx.fillRect(
          chartArea.left,
          yPixel - bandHeight / 2,
          chartArea.right - chartArea.left,
          bandHeight
        );
      });

      /* Draw a thin separator line at the gap row */
      var gapY = yScale.getPixelForValue(GAP_ROW);
      ctx.strokeStyle = '#E8E4DF';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(chartArea.left, gapY);
      ctx.lineTo(chartArea.right, gapY);
      ctx.stroke();

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
      layout: {
        padding: {
          top: 10
        }
      },
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
          max: ROW_COUNT - 0.5,
          reverse: false,
          ticks: {
            stepSize: 1,
            callback: function(value) {
              return rowLabels[value] || '';
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
        /* Disable built-in legend — we use the HTML key above the chart */
        legend: {
          display: false
        },
        tooltip: {
          titleFont: { family: "'Inter', sans-serif" },
          bodyFont: { family: "Georgia, serif" },
          callbacks: {
            title: function(items) {
              if (items.length > 0) {
                var rowIndex = items[0].parsed.y;
                return rowLabels[rowIndex] || '';
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
    plugins: [dumbbellLinePlugin, annotationPlugin]
  });
});
