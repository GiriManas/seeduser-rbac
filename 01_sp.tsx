import { Chart as ChartJS, Tooltip, Legend, PointElement, LinearScale, Title } from 'chart.js';
import { Scatter } from 'react-chartjs-2';
import { ChartOptions } from 'chart.js';
import { useRef } from 'react';

ChartJS.register(PointElement, LinearScale, Title, Tooltip, Legend);

interface DataPoint {
  x: number;
  y: number;
  topic: string;
}

interface ScatterPlotProps {
  data: DataPoint[];
  setHoveredPoint: (point: DataPoint | null) => void;
}

export default function ScatterPlot({ data, setHoveredPoint }: ScatterPlotProps) {
  const chartRef = useRef<any>(null);

  const groupedData = data.reduce((acc: Record<string, DataPoint[]>, point) => {
    if (!acc[point.topic]) acc[point.topic] = [];
    acc[point.topic].push(point);
    return acc;
  }, {});

  const colors: Record<string, string> = {
    'Neuro A': 'blue',
    'Neuro B': 'green',
    'Neuro C': 'orange',
  };

  const datasets = Object.entries(groupedData).map(([topic, points]) => ({
    label: topic,
    data: points,
    backgroundColor: colors[topic],
  }));

  const options: ChartOptions<'scatter'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' },
      tooltip: {
        enabled: true, // Let Chart.js handle tooltip display
      },
    },
    onHover: (event, elements) => {
      if (!chartRef.current) return;
      if (elements.length > 0) {
        const chart = chartRef.current;
        const datasetIndex = elements[0].datasetIndex;
        const index = elements[0].index;
        const point = chart.data.datasets[datasetIndex].data[index] as DataPoint;
        setHoveredPoint(point);
      } else {
        setHoveredPoint(null);
      }
    },
    scales: {
      x: {
        title: { display: true, text: 'X Axis' },
        min: 0,
        max: 10,
      },
      y: {
        title: { display: true, text: 'Y Axis' },
        min: 0,
        max: 10,
      },
    },
  };

  return (
    <div style={{ width: 600, height: 600 }}>
      <Scatter ref={chartRef} options={options} data={{ datasets }} />
    </div>
  );
}