import { Link } from "react-router";

function Home() {
  return (
    <section className="page">
      <h1>AI Clinical Document Reviewer</h1>

      <p>
        Analyze clinical text, images, and PDF documents and generate a
        structured clinical review.
      </p>

      <Link to="/analyze" className="button">
        Analyze a Document
      </Link>
    </section>
  );
}

export default Home;