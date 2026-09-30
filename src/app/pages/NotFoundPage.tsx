import { Link } from "react-router";

export function NotFoundPage() {
  return (
    <section className="section page-section narrow-page" aria-labelledby="not-found-heading">
      <p className="eyebrow">404</p>
      <h1 id="not-found-heading">That district does not exist.</h1>
      <p>The portfolio has enough systems already. This route is not one of them.</p>
      <Link className="button button-primary" to="/">
        Return home
      </Link>
    </section>
  );
}
