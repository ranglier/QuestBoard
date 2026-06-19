# Maquettes textuelles — QuestBoard

## Navigation principale

```text
QuestBoard                                      [+ Capture] [Mode discret]
────────────────────────────────────────────────────────────────────────
Dashboard | Inbox | Projets | Calendrier | Historique | Camp
```

Comportement :

- Dashboard affiché par défaut.
- Camp masquable via mode discret.
- Capture rapide accessible globalement.

## Vue Dashboard / Aujourd’hui

Objectif : voir ce qui structure la journée, ce qui est en cours et ce qui demande attention.

```text
┌─ Aujourd’hui ─────────────────────────────────────────────────────────┐
│ Agenda / calendrier local                                             │
│ 09:00  Réunion équipe                                                 │
│ 11:00  Point projet                                                   │
│ 14:00  MEO / changement                                               │
├───────────────────────────────────────────────────────────────────────┤
│ Planifié aujourd’hui                                                  │
│ - Revue MEO du lundi                                                  │
│ - Préparer retour ticket                                              │
├───────────────────────────────────────────────────────────────────────┤
│ En cours                                                             │
│ - Diagnostic MECM Remote Control                                      │
│ - Audit infra mail                                                    │
├───────────────────────────────────────────────────────────────────────┤
│ En attente / à relancer                                               │
│ - Attente retour NOC                                                  │
│ - Relance fournisseur                                                 │
├───────────────────────────────────────────────────────────────────────┤
│ Reprendre                                                             │
│ - Dernière note sur projet actif                                      │
└───────────────────────────────────────────────────────────────────────┘
```

Règles :

- 8 tâches visibles par défaut, réglable par l’utilisateur.
- Filtres par statut, type, priorité et domaine.
- Pas d’affichage XP/or potentiel sur le Dashboard.

## Capture rapide

```text
┌─ Capture rapide ─────────────────────────┐
│ Titre : [                             ]  │
│ Type : [auto / liste]                    │
│ Priorité : [auto / liste]                │
│ Source : [optionnel]                     │
│                                          │
│ [Capturer] [Qualifier maintenant]        │
└──────────────────────────────────────────┘
```

Règles :

- titre seul accepté ;
- type et priorité proposés automatiquement si possible ;
- qualification complète possible plus tard ;
- raccourci clavier souhaité.

## Vue Inbox

```text
┌─ Inbox ───────────────────────────────────────────────────────────────┐
│ Entrées non qualifiées                                                │
│                                                                       │
│ [ ] Mail copié / note libre                                           │
│     Source : mail                                                     │
│     [Transformer en tâche] [Projet] [Note] [Relance]                  │
│                                                                       │
│ [ ] Demande orale à traiter                                           │
│     Source : demande                                                  │
│     [Transformer en tâche] [Projet] [Note] [Relance]                  │
└───────────────────────────────────────────────────────────────────────┘
```

## Vue Projets

Deux modes : liste compacte et Kanban par projet.

Chaque projet affiche :

- nom ;
- domaine ;
- statut ;
- progression automatique ;
- dernière note ;
- prochaine action ;
- tâches associées ;
- historique.

## Vue Calendrier local

Objectif V1 : calendrier local sans synchronisation Microsoft.

Niveau minimal souhaité : vue semaine.

```text
Lundi       Mardi       Mercredi       Jeudi       Vendredi
09:00       ...         ...            ...         ...
10:00
11:00
```

Fonctions :

- créer un événement local ;
- planifier une tâche ;
- afficher tâches récurrentes, MEO et changements ;
- créer un bloc de temps depuis une tâche plus tard.

## Vue Camp

```text
┌─ Camp ────────────────────────────────────────────────────────────────┐
│ Compagnie : Niveau 1        XP : 40 / 100   Or : 25   Provisions : 3 │
├───────────────────────────────────────────────────────────────────────┤
│ Camp                                                                  │
│ [Feu de camp] [Tente de repos] [Chariot] [Table de cartes] [Coffre]  │
├───────────────────────────────────────────────────────────────────────┤
│ Capitaine                                                             │
│ Nom : à définir       Classe : Guerrier / Rôdeur / Mage / Soigneur   │
│ Statut : disponible                                                  │
├───────────────────────────────────────────────────────────────────────┤
│ Expédition                                                            │
│ Explorer les abords du camp                                           │
│ Durée : 30 min   Risque : faible   Réussite : Bon — 75 %             │
│ Coût : 1 provision                                                    │
│ [Lancer]                                                              │
├───────────────────────────────────────────────────────────────────────┤
│ Rapport                                                               │
│ Court paragraphe narratif après résolution de l’expédition.           │
└───────────────────────────────────────────────────────────────────────┘
```

## Vue Historique

Contient le journal de travail généré automatiquement à partir des tâches terminées.

Pas de journal de compagnie dédié en V1.

Les rapports d’expédition restent accessibles depuis le Camp ou un historique RPG léger plus tard.
