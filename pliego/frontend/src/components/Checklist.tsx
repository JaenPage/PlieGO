import styles from "../styles/card.module.css";
import { api } from "../api/client";

type Item = { id: number; descripcion: string; obligatorio: boolean; estado: "pending" | "ok" };
type Props = { sobres: Record<"A" | "B" | "C", Item[]>; onChange: () => void };

export default function Checklist({ sobres, onChange }: Props) {
  const sections: ("A" | "B" | "C")[] = ["A", "B", "C"];
  const toggle = async (id: number, estado: "pending" | "ok") => {
    try {
      await api.patch(`/requirement/${id}`, { estado });
      onChange();
    } catch (error) {
      console.error("No se pudo actualizar el requisito", error);
    }
  };

  return (
    <div className={styles.card}>
      <h3>Checklist por sobres</h3>
      {sections.map((s) => (
        <div key={s}>
          <h4>Sobre {s}</h4>
          <ul>
            {(sobres?.[s] || []).map((item) => (
              <li key={item.id} style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <span style={{ flex: 1 }}>
                  {item.descripcion}
                  {!item.obligatorio && " (Opcional)"}
                </span>
                <button onClick={() => toggle(item.id, item.estado === "ok" ? "pending" : "ok")}>
                  {item.estado === "ok" ? "✓ OK" : "Pendiente"}
                </button>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
