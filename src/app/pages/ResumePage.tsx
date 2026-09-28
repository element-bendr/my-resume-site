import { experience, skills } from "../../content";
import type { SkillContent } from "../../content/types";

const groupedSkills = skills.reduce<Record<string, SkillContent[]>>((groups, skill) => {
  (groups[skill.category] ??= []).push(skill);
  return groups;
}, {});

export function ResumePage() {
  return (
    <section className="section page-section" aria-labelledby="resume-heading">
      <div className="section-heading">
        <p className="eyebrow">Professional history</p>
        <h1 id="resume-heading">Resume</h1>
        <p>
          This route uses the structured, source-referenced profile history. Unverified education
          and legacy percentage skill scores are deliberately omitted.
        </p>
      </div>

      <div className="timeline" aria-label="Work experience">
        {experience.map((entry) => (
          <article className="timeline-entry" key={entry.id}>
            <p className="timeline-period">{entry.period}</p>
            <div>
              <h2>{entry.role}</h2>
              <p className="timeline-org">{entry.organization}</p>
              <p>{entry.summary}</p>
              <ul>
                {entry.highlights.map((highlight) => (
                  <li key={highlight}>{highlight}</li>
                ))}
              </ul>
            </div>
          </article>
        ))}
      </div>

      <div className="skills-section">
        <div className="section-heading">
          <p className="eyebrow">Capabilities</p>
          <h2>Evidence-backed skills</h2>
        </div>
        <div className="skill-grid">
          {Object.entries(groupedSkills).map(([category, categorySkills]) => (
            <section className="panel" key={category}>
              <h3>{category}</h3>
              <ul className="plain-list">
                {categorySkills.map((skill) => (
                  <li key={skill.id}>{skill.label}</li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      </div>
    </section>
  );
}
