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
  category:
    | "heating"
    | "appliance"
    | "kitchen"
    | "bathroom"
    | "flooring"
    | "other";
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
  name: string;
  scheduled_date: Date;
  completed_date?: Date;
  status: "pending" | "completed" | "skipped" | "issue_reported";
  notes?: string;
  was_successful?: boolean;
  issues_encountered?: string;
  object_id: number;
  user_id: number;
  advice_id: number;
  object?: ObjectItem;
}

export interface Contribution {
  id: number;
  title: string;
  content: string;
  category: string;
  status: "pending" | "approved" | "rejected";
  upvotes: number;
  author_id: number;
  created_at: Date;
}

export interface ObjectRequest {
  id: number;
  name: string;
  category:
    | "heating"
    | "appliance"
    | "kitchen"
    | "bathroom"
    | "flooring"
    | "other";
  brand?: string;
  model?: string;
  purchase_date?: Date;
  manual_url?: string;
  notes?: string;
  parent_id?: number;
  status: "pending" | "approved" | "rejected";
  admin_notes?: string;
  requester_id: number;
  reviewed_by?: number;
  created_at: Date;
  reviewed_at?: Date;
}

export interface ObjectRequestDecision {
  status: "approved" | "rejected";
  admin_notes?: string;
}

export interface Problem {
  id: number;
  title: string;
  description: string;
  category:
    | "electrical"
    | "leak"
    | "mechanical"
    | "noise"
    | "heating_cooling"
    | "wear"
    | "safety"
    | "other";
  severity: "low" | "medium" | "high" | "critical";
  status: "open" | "in_progress" | "resolved" | "closed";
  symptoms?: string;
  possible_causes?: string;
  object_id: number;
  reported_by: number;
  created_at: Date;
  updated_at: Date;
  deleted_at?: Date;
}

export interface ProblemResolution {
  id: number;
  solution: string;
  steps?: string;
  cost_estimate?: string;
  time_estimate?: string;
  was_successful?: boolean;
  feedback?: string;
  helpfulness_score: number;
  images?: string;
  problem_id: number;
  resolved_by: number;
  created_at: Date;
  updated_at: Date;
  deleted_at?: Date;
}

export interface ProblemChat {
  id: number;
  problem_id: number;
  user_id: number;
  username: string;
  message: string;
  created_at: string | Date;
  deleted_at?: string | Date;
}

export interface ProblemChatCreate {
  message: string;
}
