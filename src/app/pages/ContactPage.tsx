import { identity, links } from "../../content";

export function ContactPage() {
  return (
    <section className="section page-section narrow-page" aria-labelledby="contact-heading">
      <p className="eyebrow">Contact</p>
      <h1 id="contact-heading">Build something that has to keep working.</h1>
      <p>
        For consulting, engineering, or systems work, use the public portfolio email. Legacy phone
        and unverified profile links are intentionally not carried into this rebuild.
      </p>
      <a className="button button-primary" href={`mailto:${identity.publicEmail}`}>
        {identity.publicEmail}
      </a>
      <div className="contact-links" aria-label="Public links">
        {links
          .filter((link) => link.kind !== "email")
          .map((link) => (
            <a key={link.id} href={link.href} rel="noreferrer" target="_blank">
              {link.label}
            </a>
          ))}
      </div>
    </section>
  );
}
