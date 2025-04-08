'use client'

import {
  Chart as ChartJS,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Scatter } from 'react-chartjs-2'
import { ChartOptions } from 'chart.js'
import { useRef } from 'react'

ChartJS.register(PointElement, LinearScale, Title, Tooltip, Legend)

export type DataPoint = {
  x: number
  y: number
  topic: string
}

type ScatterPlotProps = {
  data: DataPoint[]
  setHoveredPoint?: (point: DataPoint | null) => void
}

export default function ScatterPlot({ data, setHoveredPoint }: ScatterPlotProps) {
  const chartRef = useRef<any>(null)

  const topics = Array.from(new Set(data.map((d) => d.topic)))
  const colors = ['#3b82f6', '#10b981', '#f59e0b']

  const datasets = topics.map((topic, index) => ({
    label: topic,
    data: data.filter((d) => d.topic === topic),
    backgroundColor: colors[index % colors.length],
  }))

  const options: ChartOptions<'scatter'> = {
    responsive: false,
    maintainAspectRatio: false,
    interaction: {
      mode: 'nearest',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top' as const,
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const point = context.raw as DataPoint
            return `(${point.x}, ${point.y})`
          },
        },
      },
    },
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        title: {
          display: true,
          text: 'X Axis',
        },
        min: 0,
        max: 10,
      },
      y: {
        title: {
          display: true,
          text: 'Y Axis',
        },
        min: 0,
        max: 10,
      },
    },
    onHover: (event, elements) => {
      if (setHoveredPoint) {
        if (elements.length > 0) {
          const datasetIndex = elements[0].datasetIndex
          const index = elements[0].index
          const point = datasets[datasetIndex].data[index] as DataPoint
          setHoveredPoint(point)
        } else {
          setHoveredPoint(null)
        }
      }
    },
  }

  return (
    <div className="relative w-[600px] h-[600px]">
      <Scatter ref={chartRef} data={{ datasets }} options={options} />
    </div>
  )
}