'use client'

import { useMemo, useState } from 'react'
import ScatterPlot, { DataPoint } from './ScatterPlot'

export default function NeuroClusterView() {
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null)

  const data: DataPoint[] = useMemo(() => {
    const generatePoints = (topic: string) =>
      Array.from({ length: 10 }, (_, i) => ({
        x: i + 1,
        y: parseFloat((Math.random() * 10).toFixed(2)),
        topic,
      }))

    return [
      ...generatePoints('Neuro A'),
      ...generatePoints('Neuro B'),
      ...generatePoints('Neuro C'),
    ]
  }, [])

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