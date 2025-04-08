'use client'

import { useRef } from 'react'
import {
  Chart as ChartJS,
  Tooltip,
  Legend,
  LinearScale,
  PointElement,
  Title,
} from 'chart.js'
import { Scatter } from 'react-chartjs-2'

ChartJS.register(LinearScale, PointElement, Tooltip, Legend, Title)

export type DataPoint = {
  x: number
  y: number
  topic: string
}

export type ScatterPlotProps = {
  data: DataPoint[]
  setHoveredPoint: (point: DataPoint | null) => void
}

const COLORS = [
  '#3b82f6', // blue
  '#10b981', // green
  '#f59e0b', // amber
  '#ef4444', // red
  '#8b5cf6', // violet
  '#ec4899', // pink
]

export default function ScatterPlot({ data, setHoveredPoint }: ScatterPlotProps) {
  const chartRef = useRef<any>(null)

  // Group data by topic
  const grouped = data.reduce<Record<string, DataPoint[]>>((acc, point) => {
    acc[point.topic] = acc[point.topic] || []
    acc[point.topic].push(point)
    return acc
  }, {})

  const datasets = Object.entries(grouped).map(([topic, points], index) => ({
    label: topic,
    data: points,
    pointBackgroundColor: COLORS[index % COLORS.length],
    pointRadius: 6,
  }))

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    onHover: (_: any, elements: any[]) => {
      if (elements.length > 0) {
        const datasetIndex = elements[0].datasetIndex
        const index = elements[0].index
        const point = datasets[datasetIndex].data[index]
        setHoveredPoint(point)
      } else {
        setHoveredPoint(null)
      }
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: (ctx: any) => {
            const { x, y } = ctx.raw
            return `(${x.toFixed(2)}, ${y.toFixed(2)})`
          },
          title: (ctx: any) => {
            const datasetIndex = ctx[0].datasetIndex
            return datasets[datasetIndex].label
          },
        },
      },
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Neuro Topics Scatter Plot',
      },
    },
    scales: {
      x: {
        title: { display: true, text: 'X Axis' },
      },
      y: {
        title: { display: true, text: 'Y Axis' },
      },
    },
  }

  return (
    <div className="w-full h-[400px]">
      <Scatter ref={chartRef} data={{ datasets }} options={options} />
    </div>
  )
}