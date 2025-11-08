import { useCallback, useEffect, useState } from "react";
import { api } from "../api/client";
import SummaryCard from "../components/SummaryCard";
import Checklist from "../components/Checklist";

export default function ResultPage({ id }: { id: number }) {
  const [data, setData] = useState<any>(null);
  const refetch = useCallback(() => api.get(`/analysis/${id}`).then((r) => setData(r.data)), [id]);

  useEffect(() => {
    refetch();
  }, [refetch]);

  const download = useCallback(async () => {
    const r = await api.get(`/analysis/${id}/export`);
    const blob = new Blob([JSON.stringify(r.data, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `pliego-analysis-${id}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  }, [id]);

  if (!data) return <p>Cargando análisis…</p>;
  return (
    <>
      <button onClick={download}>Exportar JSON</button>
      <SummaryCard resumen={data.resumen} plazos={data.plazos} />
      <Checklist sobres={data.sobres} onChange={refetch} />
    </>
  );
}
