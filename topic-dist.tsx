import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

const data = [
  { name: 'A', count: 10 },
  { name: 'B', count: 20 },
];

export default function TestChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="count">
          {data.map((_, i) => (
            <Cell key={i} fill={['#8884d8', '#82ca9d'][i % 2]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}