import styles from "../styles/card.module.css";

export default function SummaryCard({ resumen, plazos }: { resumen: any; plazos: any }) {
  return (
    <div className={styles.card}>
      <h3>Resumen del pliego</h3>
      <ul>
        <li>Plazo de presentación: {plazos?.presentacion || "—"}</li>
        <li>Procedimiento: {resumen?.procedimiento || "—"}</li>
        <li>Lotes: {resumen?.lotes ?? "—"}</li>
      </ul>
    </div>
  );
}
