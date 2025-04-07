'use client';

import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  ChartOptions,
  ChartTypeRegistry,
  Chart,
} from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
import { Scatter } from 'react-chartjs-2';
import { useState } from 'react';

// Register Chart.js components and plugins
ChartJS.register(LinearScale, PointElement, Tooltip, Legend, zoomPlugin);

// Optional: type for your data point
interface DataPoint {
  x: number;
  y: number;
  topic?: string;
}

export default function ScatterPlot() {
  const [hoveredLegendIndex, setHoveredLegendIndex] = useState<number | null>(null);
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null);

  const options: ChartOptions<'scatter'> = {
    scales: {
      x: {
        type: 'linear',
        title: { display: true, text: 'X Value' },
      },
      y: {
        title: { display: true, text: 'Y Value' },
      },
    },
    plugins: {
      legend: {
        position: 'top',
        onLeave: () => setHoveredLegendIndex(null),
        onHover: (_, legendItem) => {
          setHoveredLegendIndex(legendItem.datasetIndex ?? null);
        },
      },
      tooltip: {
        enabled: false,
        external: function ({
          chart,
          tooltip,
        }: {
          chart: Chart<'scatter'>;
          tooltip: ChartTypeRegistry['scatter']['options']['plugins']['tooltip'];
        }) {
          const tooltipModel = tooltip as any;

          if (!tooltipModel || !tooltipModel.dataPoints?.length) {
            setHoveredPoint(null);
            return;
          }

          const dataPoint: DataPoint = tooltipModel.dataPoints[0].raw;
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

  const data = {
    datasets: [
      {
        label: 'Scatter Dataset',
        data: [
          { x: 10, y: 20, topic: 'A' },
          { x: 15, y: 10, topic: 'B' },
          { x: 25, y: 30, topic: 'C' },
        ],
        backgroundColor: 'rgba(75,192,192,1)',
      },
    ],
  };

  return (
    <div className="w-full h-full">
      <Scatter options={options} data={data} />
    </div>
  );
}