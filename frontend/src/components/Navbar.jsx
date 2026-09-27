import { NavLink } from "react-router";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <NavLink to="/" className="brand">
          AI Clinical Document Reviewer
        </NavLink>

        <nav className="nav-links">
          <NavLink to="/" end>
            Home
          </NavLink>

          <NavLink to="/analyze">
            Analyze
          </NavLink>

          <NavLink to="/reports">
            Reports
          </NavLink>
        </nav>
      </div>
    </header>
  );
}

export default Navbar;