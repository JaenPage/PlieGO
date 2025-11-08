import styles from "../styles/card.module.css";
type Props = { sobres: Record<"A" | "B" | "C", string[]> };
export default function Checklist({ sobres }: Props) {
  const sections: ("A" | "B" | "C")[] = ["A", "B", "C"];
  return (
    <div className={styles.card}>
      <h3>Checklist por sobres</h3>
      {sections.map((s) => (
        <div key={s}>
          <h4>Sobre {s}</h4>
          <ul>
            {(sobres?.[s] || []).map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
