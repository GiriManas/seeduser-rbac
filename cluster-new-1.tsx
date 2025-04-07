'use client';

import React from 'react';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  ChartOptions,
  Chart,
} from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
import { Scatter } from 'react-chartjs-2';
import type { TooltipModel } from 'chart.js';

ChartJS.register(LinearScale, PointElement, Tooltip, Legend, zoomPlugin);

interface DataPoint {
  topic: string;
  x: number;
  y: number;
}

interface ScatterPlotProps {
  data: {
    datasets: {
      label: string;
      data: DataPoint[];
      backgroundColor?: string;
    }[];
  };
  setHoveredPoint: (point: DataPoint | null) => void;
  setHoveredLegendIndex: (index: number | null) => void;
}

export default function ScatterPlot({
  data,
  setHoveredPoint,
  setHoveredLegendIndex,
}: ScatterPlotProps) {
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
          tooltip: TooltipModel<'scatter'>;
        }) {
          if (!tooltip || !tooltip.dataPoints?.length) {
            setHoveredPoint(null);
            return;
          }

          const dataPoint = tooltip.dataPoints[0].raw as DataPoint;

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

  return <Scatter data={data} options={options} />;
}