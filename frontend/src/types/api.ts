// frontend/src/types/api.ts
/**
 * TypeScript types for AI-stotle API
 * Generated from backend/api/main.py
 */

// Request Types
export interface AskQuestionRequest {
  question: string;
  student_age?: number;
  context?: Record<string, any>;
  use_knowledge_base?: boolean;
}

export interface ExperimentSearchParams {
  query: string;
  limit?: number;
}

// Response Types
export interface QuestionResponse {
  answer: string;
  success: boolean;
  cost?: number;
  tokens_used?: number;
  sources?: Source[];
}

export interface Source {
  // From experiments collection
  name?: string;
  category?: string;
  age_min?: number;
  age_max?: number;
  wow_factor?: number;

  // From qa_pairs collection
  question?: string;
  experiment?: string;
  experiment_id?: string;
}

export interface ExperimentResult {
  name: string;
  category: string;
  age_range: string;
  wow_factor: number;
}

export interface ExperimentSearchResponse {
  results: ExperimentResult[];
}

export interface HealthResponse {
  status: string;
  aristotle: string;
  knowledge_base: KnowledgeBaseStats;
  model: string;
  embeddings: string;
}

export interface KnowledgeBaseStats {
  total_experiments: number;
  total_qa_pairs: number;
  total_concepts: number;
  total_passages: number;
  collections: string[];
  embedding_model: string;
  embedding_dimension: number;
  vector_db: string;
  total_cost: string;
}

export interface StatsResponse {
  knowledge_base: KnowledgeBaseStats;
  model: string;
  cost_per_1k_questions: string;
  vs_gpt4: string;
}

export interface MetaResponse {
  api: {
    title: string;
    version: string;
    description: string;
    philosophy: string;
  };
  endpoints: EndpointInfo[];
  capabilities: Capabilities;
  status: string;
  documentation: string;
}

export interface EndpointInfo {
  path: string;
  method: string;
  description: string;
  parameters?: Record<string, string>;
}

export interface Capabilities {
  ai_provider: string;
  model: string;
  temperature: number;
  knowledge_base: {
    enabled: boolean;
    vector_db: string;
    total_experiments: number;
    total_qa_pairs: number;
    total_concepts: number;
    total_passages: number;
    collections: string[];
    embedding_model: string;
    embedding_dimension: number;
    total_cost: string;
  };
  rag_enabled: boolean;
  cors_enabled: boolean;
}

export interface RootResponse {
  status: string;
  service: string;
  version: string;
  philosophy: string;
}

// Error Response
export interface ErrorResponse {
  detail: string;
}
