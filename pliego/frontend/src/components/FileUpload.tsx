import React, { useState } from "react";
import { api } from "../api/client";

export default function FileUpload({ onUploaded }: { onUploaded: (id: number) => void }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();

  const onChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    setLoading(true);
    setError(undefined);
    const form = new FormData();
    form.append("file", e.target.files[0]);
    try {
      const { data } = await api.post("/upload", form, { headers: { "Content-Type": "multipart/form-data" } });
      onUploaded(data.id);
    } catch (err: any) {
      setError("Error subiendo archivo");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" accept=".pdf,.docx" onChange={onChange} />
      {loading && <p>Procesando…</p>}
      {error && <p>{error}</p>}
    </div>
  );
}
