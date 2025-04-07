// src/app/NeuroCluster/NeuroClusterView.tsx

import { useEffect, useState } from 'react'
import ScatterPlot, { DataPoint } from './ScatterPlot'

export default function NeuroClusterView() {
  const [loading, setLoading] = useState(true)
  const [session, setSession] = useState<{ accessToken: string } | null>(null)

  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null)
  const [hoveredLegendIndex, setHoveredLegendIndex] = useState<number | null>(null)

  // Dummy data for demonstration
  const data: DataPoint[] = [
    { topic: 'Neuron A', x: 1, y: 5 },
    { topic: 'Neuron B', x: 2, y: 3 },
    { topic: 'Neuron C', x: 4, y: 7 },
  ]

  useEffect(() => {
    // Simulate fetching session
    setSession({ accessToken: 'demo-token' })
    setLoading(false)
  }, [])

  if (loading) return <>Loading...</>
  if (!session || !session.accessToken) return <></>

  return (
    <section>
      <div className="container mx-auto px-4 py-6">
        <ScatterPlot
          data={data}
          setHoveredPoint={setHoveredPoint}
          setHoveredLegendIndex={setHoveredLegendIndex}
        />
        {hoveredPoint && (
          <div className="mt-4 text-sm text-gray-700">
            Hovered Point: {hoveredPoint.topic} (x: {hoveredPoint.x}, y: {hoveredPoint.y})
          </div>
        )}
      </div>
    </section>
  )
}