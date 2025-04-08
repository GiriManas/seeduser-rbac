import { useState, useMemo } from 'react';
import ScatterPlot from './ScatterPlot';

interface DataPoint {
  x: number;
  y: number;
  topic: string;
}

export default function NeuroClusterView() {
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null);

  const generatePoints = (topic: string): DataPoint[] => {
    return Array.from({ length: 10 }, () => ({
      x: parseFloat((Math.random() * 10).toFixed(2)),
      y: parseFloat((Math.random() * 10).toFixed(2)),
      topic,
    }));
  };

  const data: DataPoint[] = useMemo(() => [
    ...generatePoints('Neuro A'),
    ...generatePoints('Neuro B'),
    ...generatePoints('Neuro C'),
  ], []);

  return (
    <section className="p-4">
      <h2 className="text-xl font-semibold mb-4">Neuro Topics Scatter Plot</h2>
      <div className="flex gap-8">
        <ScatterPlot data={data} setHoveredPoint={setHoveredPoint} />
        {hoveredPoint && (
          <div className="p-4 border rounded shadow-md bg-white">
            <p><strong>Hovered Topic:</strong> {hoveredPoint.topic}</p>
            <p>X: {hoveredPoint.x.toFixed(2)}</p>
            <p>Y: {hoveredPoint.y.toFixed(2)}</p>
          </div>
        )}
      </div>
    </section>
  );
}