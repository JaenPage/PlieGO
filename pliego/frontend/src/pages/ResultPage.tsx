import { useEffect, useState } from "react";
import { api } from "../api/client";
import SummaryCard from "../components/SummaryCard";
import Checklist from "../components/Checklist";

export default function ResultPage({ id }: { id: number }) {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    api.get(`/analysis/${id}`).then((r) => setData(r.data));
  }, [id]);
  if (!data) return <p>Cargando análisis…</p>;
  return (
    <>
      <SummaryCard resumen={data.resumen} plazos={data.plazos} />
      <Checklist sobres={data.sobres} />
    </>
  );
}
