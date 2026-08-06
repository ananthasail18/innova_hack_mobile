export interface User {
  id: string;
  name: string;
  email: string | null;
  created_at: string;
  updated_at: string;
}

export interface TasteProfile {
  id: string;
  user_id: string;
  spice_preference: number;
  sweetness_preference: number;
  creaminess_preference: number;
  tanginess_preference: number;
  masala_intensity_preference: number;
  crunchiness_preference: number;
  oiliness_preference: number;
  saltiness_preference: number;
  confidence_score: number;
  onboarding_completed: boolean;
  dna_matrix?: any;
  created_at: string;
  updated_at: string;
}

export interface QuizAnswer {
  question_id: string;
  selected_option_id: string;
}

export interface QuizSubmission {
  user_id: string;
  answers: QuizAnswer[];
}

export interface Restaurant {
  id: string;
  name: string;
  slug: string;
  description?: string;
  logo_url?: string;
  logo?: string;
  theme_color?: string;
  primary_color?: string;
  secondary_color?: string;
  hero_image?: string;
  cover_image?: string;
  city?: string;
  cuisine?: string;
  opening_hours?: string;
  price_range?: string;
  created_at: string;
}

export interface Category {
  id: string;
  restaurant_id: string;
  name: string;
  sort_order: number;
}

export interface Dish {
  id: string;
  restaurant_id: string;
  category_id: string;
  name: string;
  description: string | null;
  price: number;
  image_url: string | null;
  is_vegetarian: boolean;
  is_available: boolean;
  display_order: number;
  
  // Vectors
  spice_level: number;
  sweetness_level: number;
  creaminess_level: number;
  tanginess_level: number;
  masala_intensity_level: number;
  crunchiness_level: number;
  oiliness_level: number;
  saltiness_level: number;
  
  // JSON arrays
  ingredients: string[];
  allergens: string[];
  dietary_tags: string[];
  recommended_pairings: string[];
  
  // Text & Optional
  preparation_style: string | null;
  chef_notes: string | null;
  serving_style: string | null;
  recommended_temperature: string | null;
  popularity_score: number;
}

export interface RecommendationReason {
  type: string;
  text: string;
}

export interface DishRecommendation {
  dish: Dish;
  score: number;
  confidence: number;
  reasons: RecommendationReason[];
}

export interface RecommendationResponse {
  user_id: string;
  recommendations: DishRecommendation[];
}

export interface CartItem {
  dish: Dish;
  quantity: number;
}

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data: T;
  message: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatResponse {
  message: string | null;
  tool_calls: {
    id: string;
    name: string;
    arguments: any;
  }[];
  updated_ui_actions: {
    action: string;
    payload: any;
  }[];
}

export interface RestaurantDetail {
  restaurant: Restaurant;
  menu: Dish[];
  categories: Category[];
  theme: {
    primary_color: string | null;
    secondary_color: string | null;
  };
  metadata: {
    city: string | null;
    cuisine: string | null;
    description: string | null;
    opening_hours: string | null;
    price_range: string | null;
  };
  recommendations?: DishRecommendation[];
}

export interface TasteEvent {
  id: string;
  user_id: string;
  type: 'order' | 'feedback' | 'scan';
  dish_id?: string;
  restaurant_id?: string;
  rating?: number;
  taste_shift_vector?: any;
  created_at: string;
}

export interface RecommendationDecision {
  id: string;
  user_id: string;
  intent: string;
  context: any;
  recommended_dish_ids: string[];
  taste_profile_snapshot: any;
  created_at: string;
}

export interface RecommendationIntent {
  query: string;
  context?: any;
  filters?: {
    category?: string;
    is_vegetarian?: boolean;
    spice_level_max?: number;
  };
}

export interface AssistantResult {
  message: string;
  recommendations: DishRecommendation[];
  source?: 'LIVE_AI' | 'SERVER_DETERMINISTIC' | 'DEVICE_OFFLINE';
}

