import React from 'react';
import ModuleCard from '../ModuleCard';
import styles from './styles.module.css';
import modulesData from '../../data/modules.json';
import type { Module } from '../../types/module';

interface HomepageModulesProps {
  modules?: Module[];
}

export default function HomepageModules({ modules }: HomepageModulesProps): React.ReactElement {
  const modulesList = modules || (modulesData.modules as Module[]);

  return (
    <section className={styles.modulesSection}>
      <div className={styles.container}>
        <header className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Course Modules</h2>
          <p className={styles.sectionSubtitle}>
            Master Physical AI and Humanoid Robotics through four comprehensive modules
          </p>
        </header>
        <div className={styles.modulesGrid}>
          {modulesList.map((module) => (
            <ModuleCard key={module.moduleNumber} module={module} />
          ))}
        </div>
      </div>
    </section>
  );
}
