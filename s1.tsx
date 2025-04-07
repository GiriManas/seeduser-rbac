// src/app/NeuroCluster/ScatterPlot.tsx

import { Chart as ChartJS, Tooltip, Legend, LinearScale, PointElement, Title, ChartOptions } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import { Scatter } from 'react-chartjs-2'
import { useRef } from 'react'

ChartJS.register(Tooltip, Legend, LinearScale, PointElement, Title, zoomPlugin)

export type DataPoint = {
  topic: string
  x: number
  y: number
}

type ScatterPlotProps = {
  data: DataPoint[]
  setHoveredPoint: (point: DataPoint | null) => void
  setHoveredLegendIndex: (index: number | null) => void
}

export default function ScatterPlot({
  data,
  setHoveredPoint,
  setHoveredLegendIndex,
}: ScatterPlotProps) {
  const chartRef = useRef<any>(null)

  const chartData = {
    datasets: [
      {
        label: 'Neuro Points',
        data,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  }

  const options: ChartOptions<'scatter'> = {
    responsive: true,
    plugins: {
      legend: {
        onLeave: () => setHoveredLegendIndex(null),
        onHover: (_, legendItem) => setHoveredLegendIndex(legendItem.datasetIndex ?? null),
      },
      tooltip: {
        enabled: false,
        external: (tooltip) => {
          const tooltipModel = tooltip as any
          if (!tooltipModel || !tooltipModel.dataPoints?.length) {
            setHoveredPoint(null)
            return
          }
          const dataPoint: DataPoint = tooltipModel.dataPoints[0].raw
          setHoveredPoint({
            topic: dataPoint.topic,
            x: dataPoint.x,
            y: dataPoint.y,
          })
        },
      },
      zoom: {
        pan: {
          enabled: true,
          mode: 'xy',
        },
        zoom: {
          wheel: { enabled: true },
          pinch: { enabled: true },
          mode: 'xy',
        },
      },
    },
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
      },
      y: {
        type: 'linear',
        position: 'left',
      },
    },
  }

  return <Scatter ref={chartRef} data={chartData} options={options} />
}