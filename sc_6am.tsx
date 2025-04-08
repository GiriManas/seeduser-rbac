import React, { useState } from 'react';
import {
  Chart as ChartJS,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Scatter } from 'react-chartjs-2';
import type { ChartOptions } from 'chart.js';

ChartJS.register(PointElement, LinearScale, Title, Tooltip, Legend);

export type DataPoint = {
  x: number;
  y: number;
  topic: string;
};

type ScatterPlotProps = {
  data: DataPoint[];
};

const ScatterPlot: React.FC<ScatterPlotProps> = ({ data }) => {
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null);

  const topicColors: { [key: string]: string } = {
    'Neuro A': 'blue',
    'Neuro B': 'green',
    'Neuro C': 'orange',
  };

  const grouped = data.reduce<Record<string, DataPoint[]>>((acc, point) => {
    if (!acc[point.topic]) acc[point.topic] = [];
    acc[point.topic].push(point);
    return acc;
  }, {});

  const datasets = Object.entries(grouped).map(([topic, points]) => ({
    label: topic,
    data: points,
    backgroundColor: topicColors[topic] || 'gray',
    pointRadius: 6,
    pointHoverRadius: 8,
  }));

  const options: ChartOptions<'scatter'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Neuro Topics Scatter Plot',
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const { x, y } = context.parsed;
            const topic = context.dataset.label!;
            setHoveredPoint({ x, y, topic }); // set on hover
            return `${topic}: (x: ${x}, y: ${y})`;
          },
        },
      },
    },
    onHover: () => {},
    scales: {
      x: {
        title: {
          display: true,
          text: 'X Axis',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Y Axis',
        },
      },
    },
  };

  return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="flex items-start gap-8">
        <div className="w-[600px] h-[600px] p-4 bg-white border shadow rounded-lg">
          <Scatter options={options} data={{ datasets }} />
        </div>

        <div className="min-w-[200px] text-sm mt-4">
          {hoveredPoint ? (
            <div className="p-4 border rounded bg-gray-50 shadow">
              <p>
                <strong>Hovered Topic:</strong> {hoveredPoint.topic}
              </p>
              <p>
                <strong>X:</strong> {hoveredPoint.x.toFixed(2)}
              </p>
              <p>
                <strong>Y:</strong> {hoveredPoint.y.toFixed(2)}
              </p>
            </div>
          ) : (
            <div className="p-4 border rounded bg-gray-50 text-gray-500 shadow">
              Hover a point to see details
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ScatterPlot;