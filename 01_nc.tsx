'use client'

import { useMemo, useState } from 'react'
import ScatterPlot, { DataPoint } from './ScatterPlot'

export default function NeuroClusterView() {
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null)

  const data: DataPoint[] = useMemo(() => {
    const generatePoints = (topic: string) => {
      return Array.from({ length: 10 }, () => ({
        x: parseFloat((Math.random() * 10).toFixed(2)),
        y: parseFloat((Math.random() * 10).toFixed(2)),
        topic,
      }))
    }

    return [
      ...generatePoints('Neuro A'),
      ...generatePoints('Neuro B'),
      ...generatePoints('Neuro C'),
    ]
  }, [])

  return (
    <section className="flex items-center justify-center min-h-screen bg-white p-4">
      <div className="flex flex-col md:flex-row items-start gap-8">
        <ScatterPlot data={data} setHoveredPoint={setHoveredPoint} />
        {hoveredPoint && (
          <div className="text-gray-800 text-sm mt-4 md:mt-0">
            <p>
              Hovered Topic: <strong>{hoveredPoint.topic}</strong>
            </p>
            <p>X: {hoveredPoint.x.toFixed(2)}, Y: {hoveredPoint.y.toFixed(2)}</p>
          </div>
        )}
      </div>
    </section>
  )
}