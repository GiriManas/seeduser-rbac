return (
  <div className="flex items-center justify-center">
    <div
      className="relative"
      style={{
        width: '600px',
        height: '600px',
        border: '1px solid #ccc', // Optional: helps you visualize bounds
      }}
    >
      <Scatter
        ref={chartRef}
        data={{ datasets }}
        options={{
          ...options,
          responsive: false, // force fixed size
          maintainAspectRatio: false,
        }}
      />
    </div>
  </div>
)