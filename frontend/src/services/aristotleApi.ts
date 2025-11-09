// frontend/src/services/aristotleApi.ts
/**
 * API client for AI-stotle backend
 * Provides typed methods for all API endpoints
 */

import axios, { AxiosInstance } from 'axios';
import {
  AskQuestionRequest,
  QuestionResponse,
  ExperimentSearchParams,
  ExperimentSearchResponse,
  HealthResponse,
  StatsResponse,
  MetaResponse,
  RootResponse
} from '../types/api';

export class AristotleApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string = 'http://localhost:8000') {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<RootResponse> {
    const response = await this.client.get<RootResponse>('/');
    return response.data;
  }

  /**
   * Detailed health check with stats
   */
  async getHealth(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/health');
    return response.data;
  }

  /**
   * Ask AI-stotle a question
   */
  async askQuestion(request: AskQuestionRequest): Promise<QuestionResponse> {
    const response = await this.client.post<QuestionResponse>('/ask', request);
    return response.data;
  }

  /**
   * Search experiments by query
   */
  async searchExperiments(
    params: ExperimentSearchParams
  ): Promise<ExperimentSearchResponse> {
    const response = await this.client.get<ExperimentSearchResponse>(
      '/experiments/search',
      { params }
    );
    return response.data;
  }

  /**
   * Get usage statistics
   */
  async getStats(): Promise<StatsResponse> {
    const response = await this.client.get<StatsResponse>('/stats');
    return response.data;
  }

  /**
   * Get API metadata and capabilities
   */
  async getMeta(): Promise<MetaResponse> {
    const response = await this.client.get<MetaResponse>('/meta.json');
    return response.data;
  }
}

// Export singleton instance
export const aristotleApi = new AristotleApiClient();

// Export factory function for custom base URL
export const createAristotleApi = (baseURL: string) => {
  return new AristotleApiClient(baseURL);
};
