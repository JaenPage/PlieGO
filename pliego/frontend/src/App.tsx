import { useState } from "react";
import UploadPage from "./pages/UploadPage";
import ResultPage from "./pages/ResultPage";
import "./styles/globals.css";

export default function App() {
  const [analysisId, setAnalysisId] = useState<number | undefined>();
  return (
    <main style={{ maxWidth: 960, margin: "0 auto", padding: "1rem" }}>
      <h1>PlieGO (MVP)</h1>
      {!analysisId ? (
        <UploadPage onReady={setAnalysisId} />
      ) : (
        <ResultPage id={analysisId} />
      )}
      <p style={{ marginTop: "2rem", fontSize: "0.9rem", opacity: 0.8 }}>
        Aviso: Esta herramienta no sustituye la revisión jurídica/técnica; el usuario es responsable final.
      </p>
    </main>
  );
}
