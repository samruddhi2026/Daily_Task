export interface TimePoint {
  timestamp: string;
  hour: number;
  heartRate: number;
  stressScore: number;
  isStressed: boolean;
}

export function generateDescriptiveInsights(data: TimePoint[]): string {
  if (!data || data.length === 0) {
    return "Insufficient data to generate pattern insights.";
  }

  // Find continuous blocks of stress
  const stressedPeriods: { start: string; end: string; avgHr: number; maxScore: number }[] = [];

  let currentPeriod: TimePoint[] = [];

  for (let i = 0; i < data.length; i++) {
    const point = data[i];
    if (point.isStressed) {
      currentPeriod.push(point);
    } else {
      if (currentPeriod.length > 0) {
        // End of a stressed period
        recordPeriod(currentPeriod, stressedPeriods);
        currentPeriod = [];
      }
    }
  }

  // If ended on a stressed period
  if (currentPeriod.length > 0) {
    recordPeriod(currentPeriod, stressedPeriods);
  }

  if (stressedPeriods.length === 0) {
    return "Subject maintained a healthy baseline throughout the recorded period. No significant acute stress events were detected.";
  }

  // Generate description based on the most severe period
  // Find the period with the highest maxScore
  const worstPeriod = stressedPeriods.reduce((prev, current) =>
    (prev.maxScore > current.maxScore) ? prev : current
  );

  let insight = `Pattern recognized: Acute stress levels detected primarily between ${worstPeriod.start} and ${worstPeriod.end}, `;
  insight += `accompanied by an average elevated heart rate of ${Math.round(worstPeriod.avgHr)} BPM. `;

  if (stressedPeriods.length > 1) {
    insight += `Additional minor stress spikes were observed at other times of the day. `;
  }

  if (worstPeriod.maxScore > 85) {
    insight += `The severity of the peak stress suggests a highly demanding cognitive or physiological load. `;
  }

  insight += `The subject successfully recovered baseline physiological states outside of these highlighted windows.`;

  return insight;
}

function recordPeriod(period: TimePoint[], list: any[]) {
  const start = period[0].timestamp;
  const end = period[period.length - 1].timestamp;
  const avgHr = period.reduce((sum, p) => sum + p.heartRate, 0) / period.length;
  const maxScore = Math.max(...period.map(p => p.stressScore));
  list.push({ start, end, avgHr, maxScore });
}

// Generate a random daily profile that ensures realistic variations
export function generateMockDayData(): TimePoint[] {
  const data: TimePoint[] = [];
  // Decide randomly when the stress peak happens
  const peakHourStart = Math.floor(Math.random() * 16) + 6; // Somewhere between 6 AM and 10 PM
  const peakDuration = Math.floor(Math.random() * 3) + 2; // 2 to 4 hours long

  for (let i = 0; i < 24; i++) {
    const isPeak = i >= peakHourStart && i <= peakHourStart + peakDuration;

    // Baseline HR is ~60-75, Stressed HR is ~85-115
    const baseHr = 65 + Math.random() * 10;
    const peakHr = 90 + Math.random() * 25;
    const hr = isPeak ? peakHr : baseHr;

    // Baseline stress is ~10-40, Stressed is 70-95
    const baseStress = 10 + Math.random() * 30;
    const peakStress = 75 + Math.random() * 20;
    const stressScore = isPeak ? peakStress : baseStress;

    const ampm = i >= 12 ? 'PM' : 'AM';
    const displayHour = i % 12 === 0 ? 12 : i % 12;
    const timestamp = `${displayHour}:00 ${ampm}`;

    data.push({
      timestamp,
      hour: i,
      heartRate: Math.round(hr),
      stressScore: Math.round(stressScore),
      isStressed: stressScore > 65
    });
  }
  return data;
}
