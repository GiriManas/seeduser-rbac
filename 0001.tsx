return (
  <section className="p-4">
    <h2 className="text-xl font-semibold mb-4">Neuro Topics Scatter Plot</h2>
    
    {/* Use flex and prevent wrap */}
    <div className="flex flex-row gap-8 items-start">
      
      {/* Fixed-size chart container */}
      <div className="w-[600px] h-[600px]">
        <ScatterPlot data={data} setHoveredPoint={setHoveredPoint} />
      </div>

      {/* Hover box to the right of chart */}
      {hoveredPoint && (
        <div className="p-4 border rounded shadow-md bg-white w-[200px] text-sm">
          <p><strong>Hovered Topic:</strong> {hoveredPoint.topic}</p>
          <p>X: {hoveredPoint.x.toFixed(2)}</p>
          <p>Y: {hoveredPoint.y.toFixed(2)}</p>
        </div>
      )}
    </div>
  </section>
);