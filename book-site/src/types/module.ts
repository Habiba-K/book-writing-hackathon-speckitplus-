/**
 * Type definitions for the Physical AI & Humanoid Robotics textbook
 * Based on data-model.md specifications
 */

/**
 * Represents a subtopic or section within a chapter.
 */
export interface Topic {
  title: string;
  description?: string;
  conceptType?: 'theory' | 'hands-on' | 'reference';
}

/**
 * Represents a chapter within a module.
 */
export interface Chapter {
  chapterNumber: number;
  title: string;
  slug: string;
  estimatedTime?: string;
  objectives?: string[];
  topics: string[];
  hasCodeExamples?: boolean;
  hasLabExercise?: boolean;
}

/**
 * Represents one of the 4 course modules in the textbook.
 */
export interface Module {
  moduleNumber: 1 | 2 | 3 | 4;
  title: string;
  subtitle: string;
  timeframe: string;
  description: string;
  icon: string;
  accentColor: string;
  status: 'available' | 'coming-soon' | 'in-progress';
  chapters: Chapter[];
  prerequisites: string[];
  learningOutcomes: string[];
  navigationPath: string;
}

/**
 * Root data structure for modules.json
 */
export interface ModulesData {
  modules: Module[];
}

/**
 * Props for the ModuleCard component
 */
export interface ModuleCardProps {
  module: Module;
}

/**
 * Props for the HomepageModules component
 */
export interface HomepageModulesProps {
  modules?: Module[];
}
