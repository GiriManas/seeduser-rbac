"use client";

import { useMemo, useState } from "react";
import { ScatterPlot, DataPoint } from "@/components/ScatterPlot";

function generatePoints(topic: string, count: number): DataPoint[] {
  return Array.from({ length: count }, () => ({
    x: parseFloat((Math.random() * 9 + 1).toFixed(2)),
    y: parseFloat((Math.random() * 9 + 1).toFixed(2)),
    topic,
  }));
}

export default function NeuroClusterView() {
  const data: DataPoint[] = useMemo(() => [
    ...generatePoints("Neuro A", 10),
    ...generatePoints("Neuro B", 10),
    ...generatePoints("Neuro C", 10),
  ], []);

  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null);

  return (
    <section className="flex justify-center items-center h-screen bg-white">
      <div className="flex gap-8">
        <ScatterPlot data={data} setHoveredPoint={setHoveredPoint} />
        {hoveredPoint && (
          <div className="text-gray-700 p-4 border rounded shadow-md w-60 h-fit">
            <div>
              <span className="font-bold">Hovered Topic:</span> {hoveredPoint.topic}
            </div>
            <div>X: {hoveredPoint.x.toFixed(2)}</div>
            <div>Y: {hoveredPoint.y.toFixed(2)}</div>
          </div>
        )}
      </div>
    </section>
  );
}