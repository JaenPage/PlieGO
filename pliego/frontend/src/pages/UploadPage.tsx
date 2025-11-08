import { useState } from "react";
import FileUpload from "../components/FileUpload";

export default function UploadPage({ onReady }: { onReady: (id: number) => void }) {
  const [id, setId] = useState<number | undefined>();
  return (
    <div>
      <h2>Sube tu pliego (PDF/DOCX)</h2>
      <FileUpload
        onUploaded={(nid) => {
          setId(nid);
          onReady(nid);
        }}
      />
      {id && <p>Archivo recibido. Analizando…</p>}
    </div>
  );
}
