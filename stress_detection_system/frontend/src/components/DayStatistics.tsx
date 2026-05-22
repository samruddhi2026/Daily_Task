import { useMemo, useState, useEffect } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceArea
} from "recharts";
import ReactMarkdown from 'react-markdown';
import { TimePoint, generateDescriptiveInsights, generateMockDayData } from "../utils/insights";

export function DayStatistics() {
  const [data, setData] = useState<TimePoint[]>([]);
  const [insights, setInsights] = useState<string>("");
  const [aiReport, setAiReport] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);

  useEffect(() => {
    // Generate the dynamic mock data on mount to simulate a unique daily pattern
    const mockData = generateMockDayData();
    setData(mockData);
    setInsights(generateDescriptiveInsights(mockData));
  }, []);

  // Find stressed periods for highlighing
  const stressedAreas = useMemo(() => {
    if (!data.length) return [];
    const areas: { start: string; end: string }[] = [];
    let start: string | null = null;
    
    for (let i = 0; i < data.length; i++) {
      if (data[i].isStressed && !start) {
        start = data[i].timestamp;
      } else if (!data[i].isStressed && start) {
        // End the area slightly after the last stressed point
        areas.push({ start, end: data[i].timestamp });
        start = null;
      }
    }
    if (start) {
      areas.push({ start, end: data[data.length - 1].timestamp });
    }
    return areas;
  }, [data]);

  const generateAIReport = async () => {
    setIsGenerating(true);
    setAiReport(null);
    try {
      const response = await fetch("http://localhost:8000/api/v1/reports/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      if (!response.ok) {
        throw new Error("Failed to generate report");
      }
      const result = await response.json();
      setAiReport(result.report);
    } catch (error: any) {
      setAiReport("Error: " + error.message);
    } finally {
      setIsGenerating(false);
    }
  };

  if (!data.length) return null;

  return (
    <div className="mt-8 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Pattern Analysis & Trends</h2>
          <p className="text-sm text-slate-500">Day-wise physiological stress tracking</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={generateAIReport}
            disabled={isGenerating}
            className="rounded bg-blue-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {isGenerating ? "Generating..." : "Generate Deep AI Report"}
          </button>
          <button 
            onClick={() => {
              const mockData = generateMockDayData();
              setData(mockData);
              setInsights(generateDescriptiveInsights(mockData));
              setAiReport(null);
            }}
            className="rounded bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-200 transition-colors"
          >
            Simulate New Pattern
          </button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-4">
        {/* Descriptive Insights Box */}
        <div className={`lg:col-span-1 flex flex-col justify-start rounded-lg bg-blue-50/50 p-5 border border-blue-100 ${aiReport ? 'overflow-y-auto max-h-72' : 'justify-center'}`}>
          <div className="flex items-center gap-2 mb-3">
            <div className="h-2 w-2 rounded-full bg-blue-500 animate-pulse"></div>
            <h3 className="text-sm font-semibold text-blue-900 uppercase tracking-wider">AI Insight</h3>
          </div>
          {aiReport ? (
            <div className="prose prose-sm prose-blue text-slate-700">
              <ReactMarkdown>{aiReport}</ReactMarkdown>
            </div>
          ) : (
            <p className="text-sm leading-relaxed text-slate-700">
              {insights}
            </p>
          )}
        </div>

        {/* Recharts Timeline */}
        <div className="lg:col-span-3 h-72">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorHr" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis 
                dataKey="timestamp" 
                axisLine={false} 
                tickLine={false} 
                tick={{ fontSize: 11, fill: '#64748b' }} 
                minTickGap={30}
              />
              <YAxis 
                axisLine={false} 
                tickLine={false} 
                tick={{ fontSize: 11, fill: '#64748b' }}
              />
              <Tooltip 
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                labelStyle={{ fontWeight: 'bold', color: '#0f172a' }}
              />
              
              {/* Highlight the dynamically detected stress periods */}
              {stressedAreas.map((area, idx) => (
                <ReferenceArea 
                  key={idx} 
                  x1={area.start} 
                  x2={area.end} 
                  strokeOpacity={0.3} 
                  fill="#fecaca" 
                  fillOpacity={0.3} 
                />
              ))}

              <Area 
                type="monotone" 
                dataKey="heartRate" 
                stroke="#3b82f6" 
                strokeWidth={2}
                fillOpacity={1} 
                fill="url(#colorHr)" 
                name="Heart Rate (BPM)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
