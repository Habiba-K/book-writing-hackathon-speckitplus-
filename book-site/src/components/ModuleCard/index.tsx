import React from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';
import type { Module } from '../../types/module';

interface ModuleCardProps {
  module: Module;
}

export default function ModuleCard({ module }: ModuleCardProps): React.ReactElement {
  const {
    moduleNumber,
    title,
    subtitle,
    timeframe,
    description,
    chapters,
    accentColor,
    navigationPath,
  } = module;

  return (
    <Link
      to={navigationPath}
      className={styles.cardLink}
      style={{ textDecoration: 'none' }}
    >
      <article
        className={styles.card}
        style={{ '--module-accent': accentColor } as React.CSSProperties}
        tabIndex={0}
        role="article"
        aria-label={`Module ${moduleNumber}: ${title}`}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            window.location.href = navigationPath;
          }
        }}
      >
        <header className={styles.cardHeader}>
          <span className={styles.moduleNumber}>Module {moduleNumber}</span>
          <span className={styles.timeframe}>{timeframe}</span>
        </header>

        <div className={styles.cardContent}>
          <h3 className={styles.title}>{title}</h3>
          <p className={styles.subtitle}>{subtitle}</p>
          <p className={styles.description}>{description}</p>
        </div>

        <div className={styles.chaptersSection}>
          <h4 className={styles.chaptersTitle}>Chapters</h4>
          <ul className={styles.chaptersList}>
            {chapters.map((chapter) => (
              <li key={chapter.chapterNumber} className={styles.chapterItem}>
                <span className={styles.chapterNumber}>{chapter.chapterNumber}.</span>
                <span className={styles.chapterTitle}>{chapter.title}</span>
              </li>
            ))}
          </ul>
        </div>

        <footer className={styles.cardFooter}>
          <span className={styles.exploreText}>Explore Module &rarr;</span>
        </footer>
      </article>
    </Link>
  );
}
