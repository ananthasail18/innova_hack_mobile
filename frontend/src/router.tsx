import { createHashRouter } from 'react-router-dom';
import { Layout } from '@/layouts/Layout';
import { LandingPage } from '@/pages/LandingPage';
import { QuizPage } from '@/pages/QuizPage';
import { RestaurantPage } from '@/pages/RestaurantPage';
import { DishDetailPage } from '@/pages/DishDetailPage';
import { TasteDNADashboard } from '@/pages/TasteDNADashboard';
import { CartPage } from '@/pages/CartPage';
import { MarketplaceSandboxPage } from '@/pages/MarketplaceSandboxPage';
import { AssistantPage } from '@/pages/AssistantPage';
import { ActivityPage } from '@/pages/ActivityPage';

export const router = createHashRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <LandingPage /> },
      { path: 'welcome', element: <LandingPage /> },
      { path: 'quiz', element: <QuizPage /> },
      { path: 'restaurant', element: <RestaurantPage /> },
      { path: 'restaurant/:slug', element: <RestaurantPage /> },
      { path: 'dish/:id', element: <DishDetailPage /> },
      { path: 'profile', element: <TasteDNADashboard /> },
      { path: 'taste-dna', element: <TasteDNADashboard /> },
      { path: 'cart', element: <CartPage /> },
      { path: 'sandbox', element: <MarketplaceSandboxPage /> },
      { path: 'assistant', element: <AssistantPage /> },
      { path: 'activity', element: <ActivityPage /> },
    ],
  },
]);
