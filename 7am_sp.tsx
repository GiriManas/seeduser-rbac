'use client'

import { Chart as ChartJS, Tooltip, Legend, PointElement, LinearScale, Title } from 'chart.js'
import { Scatter } from 'react-chartjs-2'
import type { ChartData, ChartOptions } from 'chart.js'

ChartJS.register(PointElement, LinearScale, Title, Tooltip, Legend)

export type DataPoint = {
  x: number
  y: number
  topic: string
}

export type ScatterPlotProps = {
  data: DataPoint[]
  setHoveredPoint?: (point: DataPoint | null) => void
}

export default function ScatterPlot({ data, setHoveredPoint }: ScatterPlotProps) {
  const topics = [...new Set(data.map(point => point.topic))]
  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']

  const datasets = topics.map((topic, index) => ({
    label: topic,
    data: data.filter(p => p.topic === topic),
    backgroundColor: colors[index % colors.length],
  }))

  const chartData: ChartData<'scatter'> = {
    datasets,
  }

  const options: ChartOptions<'scatter'> = {
    responsive: true,
    maintainAspectRatio: true,
    onHover: (event, chartElements) => {
      if (!setHoveredPoint) return

      if (chartElements.length > 0) {
        const datasetIndex = chartElements[0].datasetIndex
        const index = chartElements[0].index
        const point = datasets[datasetIndex].data[index] as DataPoint
        setHoveredPoint(point)
      } else {
        setHoveredPoint(null)
      }
    },
    plugins: {
      legend: {
        position: 'top',
      },
      tooltip: {
        callbacks: {
          label: context => {
            const point = context.raw as DataPoint
            return `${point.topic}: (${point.x.toFixed(2)}, ${point.y.toFixed(2)})`
          },
        },
      },
      title: {
        display: true,
        text: 'Neuro Topics Scatter Plot',
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'X Axis',
        },
        min: 0,
        max: 11,
      },
      y: {
        title: {
          display: true,
          text: 'Y Axis',
        },
        min: 0,
        max: 11,
      },
    },
  }

  return (
    <div className="w-[600px] h-[600px] mx-auto">
      <Scatter data={chartData} options={options} />
    </div>
  )
}