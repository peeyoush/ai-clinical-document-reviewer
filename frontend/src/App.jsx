import { Outlet } from "react-router";

import Navbar from "./components/Navbar";

function App() {
  return (
    <>
      <Navbar />

      <main className="page-container">
        <Outlet />
      </main>
    </>
  );
}

export default App;