'use client'

import { useMemo, useState } from 'react'
import ScatterPlot, { DataPoint } from './ScatterPlot'

export default function NeuroClusterView() {
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null)

  const generatePoints = (topic: string): DataPoint[] =>
    Array.from({ length: 10 }, () => ({
      x: parseFloat((Math.random() * 10).toFixed(2)),
      y: parseFloat((Math.random() * 10).toFixed(2)),
      topic,
    }))

  const data: DataPoint[] = useMemo(() => [
    ...generatePoints('Neuro A'),
    ...generatePoints('Neuro B'),
    ...generatePoints('Neuro C'),
  ], [])

  return (
    <section className="min-h-screen flex flex-col items-center justify-center px-4">
      <ScatterPlot data={data} setHoveredPoint={setHoveredPoint} />

      {hoveredPoint && (
        <div className="absolute right-10 top-1/2 transform -translate-y-1/2 bg-white p-4 rounded-md shadow-md border">
          <div className="text-gray-700">
            <p>Hovered Topic: <strong>{hoveredPoint.topic}</strong></p>
            <p>X: {hoveredPoint.x.toFixed(2)}, Y: {hoveredPoint.y.toFixed(2)}</p>
          </div>
        </div>
      )}
    </section>
  )
}