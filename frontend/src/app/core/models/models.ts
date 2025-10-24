export interface User {
  id: number;
  email: string;
  username: string;
  location?: string;
  created_at: Date;
}

export interface ObjectItem {
  id: number;
  name: string;
  category: 'heating' | 'appliance' | 'kitchen' | 'bathroom' | 'flooring' | 'other';
  brand?: string;
  model?: string;
  purchase_date?: Date;
  manual_url?: string;
  notes?: string;
  owner_id: number;
  created_at: Date;
}

export interface MaintenanceAdvice {
  id: number;
  title: string;
  description: string;
  frequency_days?: number;
  category: string;
  is_validated: boolean;
  created_at: Date;
}

export interface MaintenanceTask {
  id: number;
  scheduled_date: Date;
  completed_date?: Date;
  status: 'pending' | 'completed' | 'skipped' | 'issue_reported';
  notes?: string;
  was_successful?: boolean;
  issues_encountered?: string;
  object_id: number;
  user_id: number;
  advice_id: number;
}

export interface Contribution {
  id: number;
  title: string;
  content: string;
  category: string;
  status: 'pending' | 'approved' | 'rejected';
  upvotes: number;
  author_id: number;
  created_at: Date;
}
