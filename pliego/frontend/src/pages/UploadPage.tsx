import { useEffect, useState } from "react";
import { api } from "../api/client";
import FileUpload from "../components/FileUpload";

export default function UploadPage({ onReady }: { onReady: (id: number) => void }) {
  const [id, setId] = useState<number | undefined>();
  const [apiOk, setApiOk] = useState<boolean | null>(null);

  useEffect(() => {
    api
      .get("/health")
      .then(() => setApiOk(true))
      .catch((e) => {
        console.error(e);
        setApiOk(false);
      });
  }, []);

  return (
    <div>
      <h2>Sube tu pliego (PDF/DOCX)</h2>
      {apiOk === false && <p style={{ color: "#b91c1c" }}>No hay conexión con la API (revisa puerto 8000)</p>}
      <FileUpload
        onUploaded={async (nid) => {
          setId(nid);
          await api.post(`/analysis/${nid}/persist`);
          onReady(nid);
        }}
      />
      {id && <p>Archivo recibido. Analizando…</p>}
    </div>
  );
}
