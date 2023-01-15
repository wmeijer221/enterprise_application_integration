export interface Review {
  uuid: string;
  reviewer: string;
  sentiment: Sentiment;
  source_id: string;
  source_name: string;
  text: string;
  timestamp: string;
  title_id: string;
}

export interface Sentiment {
  negativity: number;
  polarity: number;
  positivity: number;
}

export interface AverageSentiment {
  avg_negativity: number;
  avg_polarity: number;
  avg_positivity: number;
  count: number;
}

