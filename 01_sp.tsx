// app/components/ScatterPlot.tsx

"use client";

import { Chart as ChartJS, Tooltip, Legend, PointElement, LinearScale, Title } from "chart.js";
import { Scatter } from "react-chartjs-2";
import { ChartOptions } from "chart.js";
import { useRef } from "react";

ChartJS.register(PointElement, LinearScale, Tooltip, Legend, Title);

export type DataPoint = {
  x: number;
  y: number;
  topic: string;
};

type ScatterPlotProps = {
  data: DataPoint[];
  setHoveredPoint: (point: DataPoint | null) => void;
};

export function ScatterPlot({ data, setHoveredPoint }: ScatterPlotProps) {
  const chartRef = useRef<any>(null);

  const topics = Array.from(new Set(data.map((point) => point.topic)));
  const colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"];

  const datasets = topics.map((topic, index) => ({
    label: topic,
    data: data.filter((point) => point.topic === topic),
    backgroundColor: colors[index % colors.length],
    pointRadius: 6,
  }));

  const options: ChartOptions<"scatter"> = {
    responsive: false,
    maintainAspectRatio: false,
    scales: {
      x: { title: { display: true, text: "X Axis" }, min: 0, max: 10 },
      y: { title: { display: true, text: "Y Axis" }, min: 0, max: 10 },
    },
    plugins: {
      tooltip: {
        enabled: true,
        callbacks: {
          label: (tooltipItem) => {
            const point = datasets[tooltipItem.datasetIndex].data[tooltipItem.dataIndex] as DataPoint;
            return `${point.topic}: (${point.x.toFixed(2)}, ${point.y.toFixed(2)})`;
          },
        },
      },
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Neuro Topics Scatter Plot",
        font: {
          size: 18,
        },
      },
    },
    onHover: (_, elements) => {
      if (elements.length > 0) {
        const chart = chartRef.current;
        const element = elements[0];
        const datasetIndex = element.datasetIndex;
        const index = element.index;
        const point = datasets[datasetIndex].data[index] as DataPoint;
        setHoveredPoint(point);
      } else {
        setHoveredPoint(null);
      }
    },
  };

  return (
    <div className="w-[600px] h-[600px]">
      <Scatter ref={chartRef} data={{ datasets }} options={options} />
    </div>
  );
}