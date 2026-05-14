export type Prediction = {
  prediction: string;
  confidence: number;
  features: Record<string, number>;
  "class": number;
  warnings?: string[];
  physiological_confidence?: "acceptable" | "limited" | string;
};
