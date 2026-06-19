# Économie & RPG — décisions V1 consolidées

> Document issu d'une session de conception.
> Il consolide les décisions sur le scoring, l'économie, les expéditions et le modèle de données.
> Il complète `cadrage-projet.md` et `fiche-mvp.md` sans en changer le périmètre MVP.

---

## 1. Scoring XP / or

Principe inchangé : l'XP récompense la complexité, l'or récompense la priorité.

Répartition décidée :

| Source | Vers la compagnie | Vers le capitaine |
|---|---|---|
| XP d'une tâche terminée | 100 % | 50 % |
| XP d'une expédition | oui (plein) | oui, au capitaine participant (plein) |
| Or d'une tâche | crédité à la compagnie | — |
| Or d'une expédition (net) | ~½ du gain or des tâches du jour, **plafonné sous lui** | — |

Les autres membres (post-MVP) gagnent leur XP via leur part du `reward_xp` des expéditions auxquelles ils participent.

---

## 2. Difficulté auto-calculée

La difficulté par défaut découle du **type seul**, corrigeable à la main.
Le niveau **Majeure / Boss** (150 XP) n'est **jamais** attribué automatiquement : réservé à une mise à la main.

| Type | Difficulté par défaut | XP |
|---|---|---:|
| Suivi / relance, Veille | Très simple / Simple | 5–10 |
| Exploitation, Communication, Interruption | Simple | 10 |
| Réunion, Ticket utilisateur | Standard | 25 |
| Documentation, Analyse, Amélioration continue | Standard | 25 |
| Script / automatisation | Difficile | 50 |
| Audit, MEO / changement | Difficile | 50 |
| Incident | Difficile | 50 |
| Projet | Complexe | 80 |

---

## 3. Économie RPG

### 3.1 Courbe de niveau

Passer au niveau *n* (compagnie **et** capitaine) coûte `100 × n` XP cumulés.
(100 pour L1→L2, 200 pour L2→L3, etc.)

### 3.2 Améliorations du camp

Tente de repos, trois paliers : **200 / 550 / 1200 or**.
(Remplace la valeur 25 or des maquettes, trop basse au regard du gain quotidien.)

### 3.3 Provisions

- **+2** crédités à la première tâche terminée du jour (plancher anti-blocage).
- **+1** par tâche de type routine / exploitation.

Les provisions n'ont d'autre usage que les expéditions et auront donc tendance à s'accumuler : acceptable en V1, à surveiller comme futur poste de dépense.

### 3.4 Rythme estimé

Sur une journée type sobre (~3–4 tâches de fond + ~5 routines) : première amélioration de tente vers ~2,5 jours, niveau 5 vers ~5 jours, niveau 10 vers ~3 semaines. La courbe de niveau est le réglage le plus simple à ajuster une fois de vraies données disponibles.

---

## 4. Expéditions — réussite et résultats

### 4.1 Formule de réussite

```
taux = base(risque) + bonus_affinité + (Compétence × 0,5)
       borné entre 30 % et 95 %
```

| Risque | Taux de base | Récompense de base |
|---|---:|---|
| Faible | 75 % | modeste |
| Moyen | 60 % | correcte |
| Élevé | 45 % | généreuse |

- `bonus_affinité` = **+10 %** si la classe de l'aventurier correspond à la classe favorite de l'expédition, sinon 0.
- La formule somme la contribution de chaque membre envoyé ; en MVP, un seul membre (le fondateur).

### 4.2 Classes favorites par type d'expédition

| Type d'expédition | Classe favorite |
|---|---|
| Reconnaissance / exploration | Rôdeur |
| Escorte / combat | Guerrier |
| Ruines / arcanes / énigmes | Mage |
| Sauvetage / soin | Soigneur |
| Récupération / réparation | Artisan |

### 4.3 Bandes de résultat

Le taux affiché détermine la distribution des résultats :

| Résultat | Multiplicateur de récompense |
|---|---:|
| Grande réussite | ×1,3 |
| Réussite | ×1,0 |
| Réussite mitigée | ×0,6 |
| Revers | ×0,3 |

**Jamais de perte au-delà des provisions misées.** Même un revers rend un peu de butin et un court récit narratif.

### 4.4 Revers : fatigue et blessure

- Un revers réduit la récompense et peut laisser l'aventurier **Fatigué** (quasi systématique) ou **Blessé** (~25 %).
- **Fatigué** : indisponible ~1 h. **Blessé** : indisponible ~4 h.
- La **tente de repos** réduit ces durées (~40 % au niveau 1) — c'est sa raison d'être concrète.
- Valeurs réglables.

---

## 5. Compétence & affinité

- **Compétence** : stat de réussite, **une par aventurier**. Échelle ~1 à 20, **démarre à 6**, **+1 à chaque montée de niveau**.
- L'affinité de classe module la réussite via le `bonus_affinité` ci-dessus.
- Un système de compétences plus riche (stats détaillées, arbres) est reporté — voir §7.

---

## 6. Modèle de données — ajouts

Seuls deux champs sont ajoutés au modèle RPG. `Task`, `Company` et `CampUpgrade` restent inchangés.

```yaml
Adventurer:
  id: string
  name: string
  role: warrior | ranger | mage | healer | artisan
  is_captain: boolean
  level: number
  xp: number
  competence: number          # NOUVEAU — démarre à 6, +1 par niveau
  status: available | expedition | resting | tired | injured

Expedition:
  id: string
  name: string
  description: string
  duration_minutes: number     # 30 | 60 | 120
  risk: low | medium | high
  favored_class: warrior | ranger | mage | healer | artisan   # NOUVEAU
  success_rate: number
  status: available | active | completed
  started_at: datetime
  completed_at: datetime
  assigned_adventurers: list
  cost_provisions: number
  reward_xp: number
  reward_gold: number
  reward_provisions: number
  result_summary: string
```

Note d'implémentation (local-first, sans process always-on) : la résolution d'une expédition se calcule **en lazy** au prochain chargement, à partir de `started_at + duration_minutes`.

---

## 7. Aujourd'hui ↔ Calendrier (option A)

- **Aujourd'hui** = vue **jour** uniquement : agenda du jour (en lecture) + sections de tâches.
- Toute la dimension **semaine et placement de créneaux** vit dans le **Calendrier local**.
- Le bascule « Vue semaine » est **retiré** de la vue Aujourd'hui.
- Bénéfice : pas de doublon de grille hebdomadaire, et si le calendrier est coupé du MVP (« si raisonnable »), Aujourd'hui reste intact.

---

## 8. Bloc gelé — Profondeur RPG (post-MVP, Phase 7)

Décisions de direction, **hors périmètre MVP** (la compagnie reste à un seul fondateur en MVP) :

- **Recrutement** : vivier de 2–3 candidats au camp (classe + Compétence aléatoires), recrutés contre de l'or, coût croissant avec la Compétence ; roster plafonné, plafond relevé par le niveau de compagnie ou une amélioration de camp.
- **Montée en niveau des membres** : via leur part d'XP des expéditions auxquelles ils participent.
- **Identité de classe** : cible à terme un **arbre de compétences complet** par classe (gros chantier lointain) ; des perks par paliers de niveau peuvent servir d'étape intermédiaire.
- **Repère d'architecture** : garder la classe comme entité de premier plan, afin d'y accrocher l'arbre plus tard via de nouvelles tables, sans réécrire l'existant.
