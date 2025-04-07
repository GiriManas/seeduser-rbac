'use client'

import {
  Chart as ChartJS,
  PointElement,
  LinearScale,
  Tooltip,
  Legend,
  Colors,
  Title,
} from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import { Scatter } from 'react-chartjs-2'
import { useEffect, useRef, useState } from 'react'

ChartJS.register(PointElement, LinearScale, Tooltip, Legend, Colors, Title, zoomPlugin)

interface DataPoint {
  topic: string
  x: number
  y: number
}

const colorPalette = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1',
  '#ec4899', '#14b8a6', '#a855f7', '#f97316',
]

export default function ScatterPlot() {
  const [rawData, setRawData] = useState<DataPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null)
  const [xRange, setXRange] = useState<[number, number] | null>(null)
  const [yRange, setYRange] = useState<[number, number] | null>(null)
  const [hoveredPoint, setHoveredPoint] = useState<DataPoint | null>(null)
  const [hoveredLegendIndex, setHoveredLegendIndex] = useState<number | null>(null)
  const chartRef = useRef<any>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('/api/scatter-data')
        const data = await res.json()
        setRawData(data)
      } catch (error) {
        console.error('Fetch error:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const filteredData = rawData.filter((item) => {
    const matchTopic = !selectedTopic || item.topic === selectedTopic
    const matchX = !xRange || (item.x >= xRange[0] && item.x <= xRange[1])
    const matchY = !yRange || (item.y >= yRange[0] && item.y <= yRange[1])
    return matchTopic && matchX && matchY
  })

  const grouped = filteredData.reduce((acc: Record<string, DataPoint[]>, item) => {
    acc[item.topic] = acc[item.topic] || []
    acc[item.topic].push(item)
    return acc
  }, {})

  const datasets = Object.entries(grouped).map(([topic, points], idx) => {
    const isHovered = hoveredLegendIndex === null || hoveredLegendIndex === idx
    return {
      label: topic,
      data: points,
      backgroundColor: colorPalette[idx % colorPalette.length],
      pointRadius: isHovered ? 6 : 3,
      borderWidth: isHovered ? 1 : 0,
      borderColor: isHovered ? '#000' : 'transparent',
      hidden: selectedTopic !== null && selectedTopic !== topic,
    }
  })

  const data = { datasets }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        type: 'linear',
        title: { display: true, text: 'X Value' },
      },
      y: {
        title: { display: true, text: 'Y Value' },
      },
    },
    plugins: {
      legend: {
        position: 'top',
        onLeave: () => setHoveredLegendIndex(null),
        onHover: (_, legendItem) => {
          setHoveredLegendIndex(legendItem.datasetIndex)
        },
      },
      tooltip: {
        enabled: false,
        external: function (context) {
          const tooltip = context.tooltip
          if (!tooltip || !tooltip.dataPoints?.length) {
            setHoveredPoint(null)
            return
          }

          const dataPoint = tooltip.dataPoints[0].raw
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
        limits: {
          x: { min: 'original', max: 'original' },
          y: { min: 'original', max: 'original' },
        },
      },
    },
    onHover: (event: any, _: any, chart: any) => {
      const legendItems = chart.legend.legendItems
      const mouseX = event.x
      const mouseY = event.y

      let found = null
      legendItems.forEach((_: any, index: number) => {
        const box = chart.legend.legendHitBoxes[index]
        if (
          mouseX >= box.left &&
          mouseX <= box.left + box.width &&
          mouseY >= box.top &&
          mouseY <= box.top + box.height
        ) {
          found = index
        }
      })

      setHoveredLegendIndex(found)
    },
  }

  const handleResetZoom = () => {
    chartRef.current?.resetZoom()
  }

  const handleDownload = () => {
    const chart = chartRef.current
    const url = chart?.toBase64Image()
    const link = document.createElement('a')
    link.href = url
    link.download = 'scatter-plot.png'
    link.click()
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h2 className="text-lg font-semibold">Scatter Plot: Complaint Topics</h2>
        <div className="flex flex-wrap gap-2">
          <button
            className={`px-3 py-1 rounded border ${
              selectedTopic === null ? 'bg-blue-500 text-white' : 'bg-white text-gray-700'
            }`}
            onClick={() => setSelectedTopic(null)}
          >
            All Topics
          </button>
          {Array.from(new Set(rawData.map((d) => d.topic))).map((topic) => (
            <button
              key={topic}
              className={`px-3 py-1 rounded border ${
                selectedTopic === topic ? 'bg-blue-500 text-white' : 'bg-white text-gray-700'
              }`}
              onClick={() => setSelectedTopic(topic)}
            >
              {topic}
            </button>
          ))}
        </div>
      </div>

      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">X Range</label>
          <div className="flex items-center gap-2 mt-1">
            <input
              type="number"
              placeholder="Min X"
              className="input input-bordered input-sm w-24"
              onChange={(e) => setXRange((prev) => [Number(e.target.value), prev?.[1] ?? 100])}
            />
            <input
              type="number"
              placeholder="Max X"
              className="input input-bordered input-sm w-24"
              onChange={(e) => setXRange((prev) => [prev?.[0] ?? 0, Number(e.target.value)])}
            />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Y Range</label>
          <div className="flex items-center gap-2 mt-1">
            <input
              type="number"
              placeholder="Min Y"
              className="input input-bordered input-sm w-24"
              onChange={(e) => setYRange((prev) => [Number(e.target.value), prev?.[1] ?? 100])}
            />
            <input
              type="number"
              placeholder="Max Y"
              className="input input-bordered input-sm w-24"
              onChange={(e) => setYRange((prev) => [prev?.[0] ?? 0, Number(e.target.value)])}
            />
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-4 mt-2">
        <button
          onClick={handleResetZoom}
          className="px-4 py-2 bg-indigo-500 text-white rounded hover:bg-indigo-600"
        >
          Reset Zoom
        </button>
        <button
          onClick={handleDownload}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Download PNG
        </button>
      </div>

      {/* Chart */}
      {loading ? (
        <p className="text-gray-500">Loading data...</p>
      ) : (
        <div className="h-[400px]">
          <Scatter ref={chartRef} data={data} options={options} />
        </div>
      )}

      {/* External Tooltip */}
      {hoveredPoint && (
        <div className="mt-4 p-3 border rounded-md bg-gray-50 text-sm w-fit shadow-sm">
          <p><strong>Topic:</strong> {hoveredPoint.topic}</p>
          <p><strong>X:</strong> {hoveredPoint.x}</p>
          <p><strong>Y:</strong> {hoveredPoint.y}</p>
        </div>
      )}
    </div>
  )
}