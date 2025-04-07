import { useState, useEffect } from 'react';
import ScatterPlot from './ScatterPlot'; // adjust path if needed

export default function NeuroClusterView() {
  const [loading, setLoading] = useState(true);
  const [hoveredPoint, setHoveredPoint] = useState(null);
  const [hoveredLegendIndex, setHoveredLegendIndex] = useState<number | null>(null);

  // Dummy session (replace with actual logic)
  const session = { accessToken: 'fake-token' };

  useEffect(() => {
    if (session?.accessToken) {
      setLoading(false);
    }
  }, [session?.accessToken]);

  if (loading) {
    return <>Loading...</>;
  }

  if (!session || !session.accessToken) {
    return <></>;
  }

  // Dummy data (replace with real data from props or API)
  const data = {
    datasets: [
      {
        label: 'Example Dataset',
        data: [
          { topic: 'A', x: 10, y: 20 },
          { topic: 'B', x: 15, y: 30 },
          { topic: 'C', x: 5, y: 8 },
        ],
        backgroundColor: 'rgba(75,192,192,1)',
      },
    ],
  };

  return (
    <section>
      <div>
        <ScatterPlot
          data={data}
          setHoveredPoint={setHoveredPoint}
          setHoveredLegendIndex={setHoveredLegendIndex}
        />
      </div>
    </section>
  );
}