import {
  BarChart as RechartsBarChart,
  Bar as RechartsBar,
  XAxis as RechartsXAxis,
  YAxis as RechartsYAxis,
  CartesianGrid as RechartsCartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer as RechartsResponsiveContainer,
  Cell as RechartsCell,
  ScatterChart as RechartsScatterChart,
  Scatter as RechartsScatter,
  ZAxis as RechartsZAxis,
} from 'recharts';

// Re-export as JSX components (keeping names short and clean)
export const BarChart = RechartsBarChart;
export const Bar = RechartsBar;
export const XAxis = RechartsXAxis;
export const YAxis = RechartsYAxis;
export const CartesianGrid = RechartsCartesianGrid;
export const Tooltip = RechartsTooltip;
export const ResponsiveContainer = RechartsResponsiveContainer;
export const Cell = RechartsCell;
export const ScatterChart = RechartsScatterChart;
export const Scatter = RechartsScatter;
export const ZAxis = RechartsZAxis;





import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from '@/components/ui/chart';




<BarChart data={data}>
  <XAxis dataKey="name" />
  <YAxis />
  <Tooltip />
  <Bar dataKey="count">
    {data.map((_, index) => (
      <Cell key={index} fill={colors[index % colors.length]} />
    ))}
  </Bar>
</BarChart>