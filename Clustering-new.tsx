import { Chart, ChartOptions, TooltipModel } from 'chart.js';
import { useState } from 'react';

type RawDataPoint = {
  topic: string;
  x: number;
  y: number;
};

type LegendItem = {
  datasetIndex?: number;
};

export default function ScatterPlot() {
  const [hoveredLegendIndex, setHoveredLegendIndex] = useState<number | null>(null);
  const [hoveredPoint, setHoveredPoint] = useState<RawDataPoint | null>(null);

  const options: ChartOptions<'scatter'> = {
    scales: {
      x: {
        type: 'linear',
        title: {
          display: true,
          text: 'X Value',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Y Value',
        },
      },
    },
    plugins: {
      legend: {
        position: 'top',
        onLeave: () => setHoveredLegendIndex(null),
        onHover: (_event, legendItem: LegendItem) => {
          setHoveredLegendIndex(legendItem.datasetIndex ?? null);
        },
      },
      tooltip: {
        enabled: false,
        external: function (context: {
          chart: Chart;
          tooltip: TooltipModel<'scatter'>;
        }) {
          const tooltip = context.tooltip;
          if (!tooltip || !tooltip.dataPoints?.length) {
            setHoveredPoint(null);
            return;
          }

          const dataPoint = tooltip.dataPoints[0].raw as RawDataPoint;

          setHoveredPoint({
            topic: dataPoint.topic,
            x: dataPoint.x,
            y: dataPoint.y,
          });
        },
      },
      zoom: {
        pan: {
          enabled: true,
          mode: 'xy',
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true,
          },
          mode: 'xy',
        },
      },
    },
  };

  return (
    <div>
      {/* Render your scatter chart component here, passing `options` as prop */}
    </div>
  );
}