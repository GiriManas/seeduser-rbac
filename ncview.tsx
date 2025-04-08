'use client'

import { useState } from 'react'
import ScatterPlot, { DataPoint } from './ScatterPlot'

export default function NeuroClusterView() {
  const data: DataPoint[] = [
    ...Array.from({ length: 10 }, (_, i) => ({ x: i + 1, y: Math.random() * 10, topic: 'Neuro A' })),
    ...Array.from({ length: 10 }, (_, i) => ({ x: i + 1, y: Math.random() * 10, topic: 'Neuro B' })),
    ...Array.from({ length: 10 }, (_, i) => ({ x: i + 1, y: Math.random() * 10, topic: 'Neuro C' })),
  ]

  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null)

  return (
    <section className="p-6">
      <div className="max-w-5xl mx-auto">
        <ScatterPlot
          data={data}
          setHoveredPoint={(point: DataPoint | null) => setHoveredPoint(point)}
        />
        {hoveredPoint && (
          <div className="mt-4 text-center text-gray-700">
            Hovered Topic: <strong>{hoveredPoint.topic}</strong><br />
            X: {hoveredPoint.x.toFixed(2)}, Y: {hoveredPoint.y.toFixed(2)}
          </div>
        )}
      </div>
    </section>
  )
}