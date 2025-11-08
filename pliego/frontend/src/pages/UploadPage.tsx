import { useState } from "react";
import { api } from "../api/client";
import FileUpload from "../components/FileUpload";

export default function UploadPage({ onReady }: { onReady: (id: number) => void }) {
  const [id, setId] = useState<number | undefined>();
  return (
    <div>
      <h2>Sube tu pliego (PDF/DOCX)</h2>
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
