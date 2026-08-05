import type { Dish, TasteProfile } from './types';

export const offlineStore = {
  saveCatalog: (dishes: Dish[]) => {
    try {
      localStorage.setItem('tasteai_catalog', JSON.stringify(dishes));
    } catch (e) {
      console.error('Failed to save catalog to localStorage', e);
    }
  },
  getCatalog: (): Dish[] => {
    try {
      const data = localStorage.getItem('tasteai_catalog');
      return data ? JSON.parse(data) : [];
    } catch (e) {
      return [];
    }
  },
  saveProfile: (profile: TasteProfile) => {
    try {
      localStorage.setItem('tasteai_profile', JSON.stringify(profile));
    } catch (e) {
      console.error('Failed to save profile to localStorage', e);
    }
  },
  getProfile: (): TasteProfile | null => {
    try {
      const data = localStorage.getItem('tasteai_profile');
      return data ? JSON.parse(data) : null;
    } catch (e) {
      return null;
    }
  }
};
