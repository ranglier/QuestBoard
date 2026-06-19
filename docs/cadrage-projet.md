# Cadrage projet — QuestBoard

> Version dépôt — cadrage consolidé  
> Objectif : conserver dans le dépôt les décisions produit, fonctionnelles, techniques et RPG nécessaires à la conception de QuestBoard.

---

## 0. Synthèse stabilisée

**QuestBoard** est un outil personnel, local-first, orienté travail professionnel.

Il poursuit deux objectifs complémentaires :

1. **Dashboard** : piloter le quotidien professionnel, visualiser les tâches, les réunions, les projets, les relances, les sujets en attente et les interruptions.
2. **Camp** : proposer une pause courte sous forme d’un mini idle RPG d’expéditions, alimenté par les tâches réellement accomplies.

Principe central :

> Le travail réel alimente le jeu.  
> Le jeu offre une pause courte, sans demander une attention continue.

QuestBoard ne doit pas devenir un outil officiel, collaboratif ou institutionnel. Il reste personnel, mais doit pouvoir produire des exports sobres et exploitables si nécessaire.

---

## 1. Décisions produit

### 1.1 Nom

Décisions :

- Le projet s’appelle **QuestBoard**.
- Le nom **QuestLog** n’est plus le nom produit principal.
- **QuestLog** pourra éventuellement être réutilisé plus tard pour une fonction d’historique ou de journal interne, mais ce n’est pas une décision V1.

### 1.2 Deux espaces séparés

Décisions :

- L’application comporte deux espaces principaux :
  - **Dashboard** : espace sérieux, affiché par défaut ;
  - **Camp** : espace RPG, consultable pendant les pauses.
- Les deux espaces sont séparés sous forme d’onglets ou de sections distinctes.
- Le Dashboard est toujours l’affichage par défaut au lancement.
- Le Camp peut être masqué via un **mode discret**.
- Le mode discret masque l’accès au Camp et les marqueurs explicitement RPG dans l’interface sérieuse.
- Comme le Dashboard et le Camp n’affichent pas les mêmes données, il n’est pas nécessaire de traduire toute l’interface RPG en libellés sobres.
- Un raccourci clavier pour activer rapidement le mode discret est souhaité.

### 1.3 Finalité

Décisions :

- QuestBoard doit devenir l’outil principal de pilotage quotidien.
- L’objectif prioritaire est de :
  - voir ce qui est prévu aujourd’hui ;
  - voir ce qui est en cours ;
  - retrouver le contexte d’un sujet interrompu ;
  - suivre les attentes et relances ;
  - rendre la progression plus motivante.
- La synthèse de fin de journée n’est pas nécessaire en V1.
- Le journal de travail est utile comme historique simple, mais pas comme rituel obligatoire.

---

## 2. MVP stabilisé

### 2.1 Choix du MVP

Décision :

> Le MVP vise directement l’option **Dashboard + première expédition**.

Cela signifie que la première version utile doit permettre :

- de créer et suivre des tâches dans le Dashboard ;
- de terminer une tâche ;
- de générer automatiquement XP, or et éventuellement provisions ;
- d’utiliser ces ressources dans le Camp ;
- de lancer une première expédition simple ;
- de récupérer un rapport narratif court et des récompenses.

Justification :

- Un simple Dashboard avec XP/or mais sans expédition ne testerait pas vraiment la promesse centrale du projet.
- Le MVP doit valider la boucle complète : **travail réel → récompense → pause RPG → progression**.

### 2.2 V0 technique

Décision :

- Créer une **V0 technique très courte** avant le MVP complet.

Cette V0 ne remplace pas le MVP. Elle sert uniquement à vérifier que les fondations fonctionnent :

- structure Docker Compose ;
- API FastAPI ;
- frontend SvelteKit ;
- base SQLite ;
- création rapide d’une tâche ;
- clôture d’une tâche ;
- calcul XP/or minimal.

Ensuite, le MVP ajoute l’inbox, la vue Aujourd’hui, les projets, le calendrier local, le Camp, le fondateur et la première expédition.

---

## 3. Dashboard

### 3.1 Vue Aujourd’hui

Objectif :

- Donner une vue d’ensemble de la journée et des sujets actifs.
- Ne pas imposer une planification rigide.
- Ne pas afficher une liste interminable.

Décisions :

- La vue Aujourd’hui affiche en priorité :
  - agenda ;
  - réunions du jour ;
  - tâches planifiées ;
  - tâches récurrentes prévues aujourd’hui ;
  - MEO / changements prévus ;
  - tâches en cours ;
  - tâches en attente ou à relancer ;
  - tâches proposées à faire ;
  - zone “reprendre” basée sur les tâches récemment modifiées.
- L’agenda domine la vue, car il donne la structure temporelle de la journée.
- Le nombre de tâches visibles par défaut est **8**, mais il doit être réglable par l’utilisateur.
- Des filtres doivent permettre d’affiner l’affichage.
- La vue Aujourd’hui ne doit pas afficher l’XP/or potentiel de la journée.
- Une vue semaine est souhaitée dès que cela reste raisonnable à implémenter.
- Pas de mini-frise horaire locale spécifique avant le calendrier local.

### 3.2 Calendrier local

Décisions :

- En V1, en l’absence d’intégration Microsoft, QuestBoard doit proposer un **mini-calendrier local** si cela ne complique pas excessivement le MVP.
- Le niveau minimal attendu est une **vue semaine**.
- Le calendrier local permet de visualiser ou créer manuellement des éléments planifiés.
- Le calendrier local doit pouvoir afficher :
  - événements manuels ;
  - tâches planifiées ;
  - routines ;
  - MEO / changements ;
  - éventuellement créneaux réservés.

Clarification :

- Créer un bloc de temps depuis une tâche signifie : sélectionner une tâche, choisir un créneau dans le calendrier, et créer un événement local lié à cette tâche.
- Cette fonctionnalité est utile, mais ne doit pas ralentir la V0 technique.

### 3.3 Inbox

Décisions :

- L’inbox fait partie du MVP.
- Elle est une vue dédiée, pas seulement un bloc du Dashboard.
- Elle accepte des notes libres.
- Une entrée inbox peut devenir :
  - tâche ;
  - projet ;
  - note ;
  - relance.
- Il doit être possible de coller un mail, un log ou un lien dans l’inbox si techniquement simple.
- Un raccourci clavier de capture rapide est souhaité.
- Une action “traiter / vider l’inbox” peut exister comme rituel hebdomadaire.

### 3.4 Capture rapide

Décisions :

- La capture minimale est :
  - titre ;
  - type ;
  - priorité.
- Une capture encore plus rapide avec uniquement un titre est souhaitée.
- Dans ce cas, QuestBoard peut proposer automatiquement un type et une priorité, corrigeables ensuite.
- La qualification complète peut venir plus tard.
- Le champ `source` est utile mais optionnel.
- La source doit être choisie dans une liste simple :
  - réunion ;
  - ticket ;
  - demande ;
  - mail ;
  - Teams ;
  - note ;
  - autre.

### 3.5 Projets

Décisions :

- La vue Projets doit exister.
- Elle propose :
  - une liste compacte ;
  - une vue Kanban.
- Le Kanban est d’abord pensé **par projet**, avec possibilité d’affiner plus tard par statut de tâche à l’intérieur d’un projet.
- Les projets affichent en priorité :
  - dernière note ;
  - prochaine action.
- Chaque projet possède une fiche détaillée avec notes et historique.
- Les projets peuvent être archivés.
- La liste des domaines est personnalisable.
- Des filtres par domaine sont nécessaires.
- Afficher par défaut environ **5 à 7 projets actifs** est acceptable.
- Les routines permanentes peuvent être affichées dans une zone séparée des projets temporaires.
- La notion de sous-quête / sous-projet n’est pas prioritaire pour la V1.

---

## 4. Tâches

### 4.1 Statuts

Statuts V1 :

- **Inbox** ;
- **À faire** ;
- **En cours** ;
- **En attente** ;
- **Planifié** ;
- **Terminé** ;
- **Abandonné**.

Décisions :

- `À relancer` n’est pas un statut.
- Une tâche `En attente` avec une `followup_date` dépassée apparaît automatiquement comme **à relancer**.
- Une vue dédiée aux sujets en attente / à relancer est utile.
- Pas de champ obligatoire `raison de l’attente`.
- Une raison d’abandon peut être conservée.
- Des actions rapides de relance sont souhaitées :
  - relancer dans 2 jours ;
  - relancer dans 1 semaine ;
  - relancer lundi prochain.

### 4.2 Types

Types V1 :

- Incident ;
- Interruption / imprévu ;
- Exploitation ;
- Projet ;
- Audit ;
- Documentation ;
- Script / automatisation ;
- Communication ;
- Réunion ;
- Analyse ;
- Suivi / relance ;
- Veille ;
- Amélioration continue ;
- MEO / changement ;
- Ticket utilisateur.

Décisions :

- `Incident` reste séparé.
- `Urgence` et `imprévu` sont regroupés dans `Interruption / imprévu`.
- Le type `Projet` peut exister pour une tâche, même si `Projet` existe aussi comme regroupement.
- Les domaines techniques comme Exchange, MECM, AD, RH, Veeam ou VTOM sont gérés dans les domaines/projets, pas dans les types.
- Des icônes ou couleurs par type sont souhaitées pour l’ergonomie.

### 4.3 Données d’une tâche

Modèle V1 recommandé :

```yaml
Task:
  id: string
  title: string
  description: string
  notes: string
  status: inbox | todo | in_progress | waiting | planned | done | abandoned
  type: incident | interruption | exploitation | project | audit | documentation | script | communication | meeting | analysis | followup | watch | improvement | change | user_ticket
  priority: low | normal | high | critical
  domain_id: string
  project_id: string
  difficulty: trivial | easy | normal | hard | complex | major
  due_date: date
  planned_date: datetime
  followup_date: date
  source: meeting | ticket | request | mail | teams | note | other
  source_detail: string
  external_links: list
  xp_reward: number
  created_at: datetime
  updated_at: datetime
  completed_at: datetime
  abandoned_reason: string
```

Décisions :

- `projet / domaine` est optionnel à la création.
- `description` et `notes` sont conservés :
  - `description` : résumé court ;
  - `notes` : suivi détaillé.
- Les liens externes simples doivent être prévus en V1 :
  - ticket ;
  - mail ;
  - fichier ;
  - dossier ;
  - URL.
- La difficulté est calculée automatiquement, avec correction manuelle possible.
- L’énergie estimée est retirée du MVP.
- Les tags libres ne sont pas retenus au départ.
- `gold_reward` n’est pas retenu comme champ direct sur `Task` en V1 ; l’or est calculé à la clôture selon la priorité et crédité côté compagnie.

---

## 5. Scoring XP / or

### 5.1 Principe général

Décision :

- **L’XP récompense la complexité, l’effort et l’apprentissage.**
- **L’or récompense la priorité, la valeur opérationnelle et l’importance immédiate.**

Conséquences :

- Une tâche complexe mais peu prioritaire donne beaucoup d’XP et peu d’or.
- Une tâche simple mais critique donne peu d’XP et beaucoup d’or.
- Un incident critique difficile donne beaucoup d’XP et beaucoup d’or.
- Les bonus automatiques complètent ce calcul selon le type ou le contexte.

Formule de base :

```text
Récompense = XP(complexité) + Or(priorité) + bonus automatiques éventuels
```

### 5.2 Barème XP par complexité

Décisions :

- Le barème XP est basé sur la difficulté / complexité.
- En mode sérieux, les libellés doivent rester sobres.
- Le dernier niveau est nommé **Majeure** côté Dashboard et **Boss** côté RPG.

| Mode sérieux | Mode RPG | Enum technique | XP |
|---|---|---|---:|
| Très simple | Triviale | `trivial` | 5 |
| Simple | Simple | `easy` | 10 |
| Standard | Normale | `normal` | 25 |
| Difficile | Difficile | `hard` | 50 |
| Complexe | Complexe | `complex` | 80 |
| Majeure | Boss | `major` | 150 |

### 5.3 Barème or par priorité

Décision :

- L’or est basé sur la priorité, et non plus sur la complexité.

| Priorité | Enum technique | Or |
|---|---|---:|
| Basse | `low` | 2 |
| Normale | `normal` | 5 |
| Haute | `high` | 15 |
| Critique | `critical` | 35 |

### 5.4 Bonus automatiques

Décisions :

- Les bonus doivent être automatiques quand le type/statut permet de les déduire.
- Pas de bonus manuel de pénibilité en V1 pour ne pas ajouter de charge de saisie.
- Une réunion donne de l’XP et un peu d’or.
- Une réunion organisée par l’utilisateur donne davantage.
- Un imprévu / interruption traité doit être valorisé.

| Cas | Bonus XP | Bonus or |
|---|---:|---:|
| Interruption traitée | +0 | +5 |
| Incident critique résolu | +0 | +25 |
| Sujet en attente débloqué | +0 | +10 |
| Documentation produite | +10 | +0 |
| Réunion organisée par l’utilisateur | +10 | +5 |
| Projet / quête terminé | Récompense spéciale | Récompense spéciale |

---

## 6. Camp / RPG

### 6.1 Concept

Décisions :

- La partie RPG est un **idle RPG d’expéditions**.
- Le joueur constitue une **compagnie itinérante d’aventuriers**.
- Le **camp / bivouac** sert de base mobile.
- La progression principale est celle de la compagnie.
- Le joueur incarne un **capitaine**.
- Le capitaine est jouable et peut partir en expédition.
- Le capitaine a une classe au choix.
- Le nom du capitaine et le nom de la compagnie sont personnalisables.
- Style visuel cible : **pixel art**.
- Ton narratif : **chaleureux**.
- Pas de marketplace, argent réel, compétition, spéculation ou échange externe.

Inspirations validées :

- **Habitica** : lien tâches réelles → récompenses.
- **Melvor Idle** : progression passive, compétences, ressources.
- **TBH / Task Bar Hero** : roster, héros autonomes, format discret de pause courte.

### 6.2 Boucle d’expédition

Décisions :

- Une expédition peut mobiliser un seul aventurier ou plusieurs.
- Pour le MVP, une seule expédition active à la fois.
- Les expéditions ont un taux de réussite.
- Le taux de réussite ajuste les récompenses.
- Le risque est affiché avant le lancement.
- Une expédition ne doit pas échouer de façon punitive.
- En cas de mauvais résultat :
  - récompense réduite ;
  - aventurier fatigué ou blessé ;
  - besoin de repos ;
  - court rapport narratif.
- Des événements aléatoires sont souhaités.
- Les expéditions longues matin → fin de journée sont repoussées.

Durées V1 validées :

- 30 minutes ;
- 1 heure ;
- 2 heures.

Affichage du taux de réussite :

- Recommandation : afficher à la fois un libellé et un pourcentage.
- Exemple : `Bon — 75 %`.
- Le libellé rend la lecture agréable, le pourcentage donne de la clarté.

Rapport d’expédition :

- Format : court paragraphe narratif.

### 6.3 Ressources RPG

Ressources V1 :

- XP ;
- or ;
- provisions.

Décisions :

- L’XP gagnée par les tâches va à la fois :
  - à la compagnie ;
  - au capitaine.
- L’or sert à :
  - équipement ;
  - recrutement ;
  - améliorations du camp.
- Les provisions servent à lancer des expéditions.
- Les provisions peuvent être gagnées via certaines tâches, notamment routines.
- Une production minimale quotidienne de provisions peut exister pour éviter le blocage.
- Les objets rares, narratifs ou cosmétiques, sont souhaités mais repoussés après la première boucle jouable.

### 6.4 Camp / bivouac

Décisions :

- Le Camp est d’abord fonctionnel, sous forme de menus/cartes.
- Les visuels viennent ensuite.
- Le Camp doit pouvoir évoluer visuellement plus tard.
- Les améliorations ont à la fois un impact de gameplay et un intérêt narratif/cosmétique.
- Pas de registre de compagnie en V1.
- Pas de journal de compagnie dédié finalement.

Éléments V1 :

- **Feu de camp** : accueil du Camp.
- **Tente de repos** : récupération des aventuriers fatigués ou blessés.
- **Chariot d’intendance** : ressources, provisions, or.
- **Table de cartes** : choix et lancement des expéditions.
- **Coffre de compagnie** : objets, butin, équipement plus tard.

Première amélioration de camp :

- La **tente de repos**.
- Elle commence très simplement, comme une couverture ou un abri rudimentaire.
- Elle peut être améliorée progressivement.

### 6.5 Aventuriers et classes

Décisions :

- Le MVP démarre avec un seul fondateur.
- Le fondateur est créé par le joueur.
- Les aventuriers peuvent être renommés.
- Les aventuriers peuvent être fatigués, au repos, en expédition ou blessés.
- Les traits de personnalité sont repoussés à une V2.

Classes V1 retenues :

- **Guerrier** ;
- **Rôdeur** ;
- **Mage** ;
- **Soigneur** ;
- **Artisan**.

### 6.6 Stratégie pixel art

Décisions :

- Il ne sert à rien de produire du pixel art définitif pour la V0 ou le MVP.
- Le prototype doit utiliser des placeholders, cartes UI, icônes simples ou silhouettes temporaires.
- La priorité V0/MVP est de valider la boucle fonctionnelle, pas la direction artistique.
- Après validation du gameplay, une mini direction artistique sera définie : taille des sprites, palette, ambiance, règles visuelles.
- PixelLab est identifié comme piste possible pour générer des concepts ou bases d’assets, mais ne doit pas devenir une dépendance du projet.
- Aseprite ou Pixelorama peuvent servir à nettoyer, homogénéiser ou produire les sprites définitifs.
- Les assets générés ou récupérés doivent être copiés dans le frontend comme fichiers statiques, afin que QuestBoard reste local-first et autonome.
- Les prompts, images ou exemples utilisés dans des outils externes ne doivent contenir aucune donnée professionnelle sensible.

Assets minimum envisagés plus tard :

- icônes XP, or, provisions ;
- icônes de classes ;
- cartes de camp ;
- états d’aventurier ;
- ressources ;
- éléments UI pixel art ;
- évolution visuelle de la tente de repos.

---

## 7. Vues RPG et historiques

### 7.1 Vue Camp

Contenu V1 :

- état du camp ;
- compagnie niveau X ;
- ressources : XP, or, provisions ;
- capitaine / fondateur ;
- expédition en cours ou disponible ;
- rapport d’expédition ;
- amélioration de camp disponible.

Décisions :

- La vue affiche d’abord le Camp.
- Elle reste fonctionnelle et textuelle dans la V1.
- Une progression globale de compagnie est affichée.
- Les achievements peuvent exister si cela reste simple.
- Les achievements peuvent être liés :
  - au Dashboard ;
  - au RPG.

### 7.2 Journal / historique

Décisions :

- Pas de journal de compagnie dédié en V1.
- Le journal de travail devient un onglet dans l’historique.
- Les rapports d’expédition peuvent rester accessibles dans le Camp ou un historique RPG léger, mais pas comme journal séparé.
- Le journal de travail est généré automatiquement à partir des tâches terminées.
- Il peut être corrigé ou complété manuellement.
- Pas de commentaire de fin de journée obligatoire.
- Une synthèse hebdomadaire n’est produite que sur demande.
- Un export Markdown hebdomadaire pourra être utile plus tard.

---

## 8. Modèles de données RPG

Modèles V1 recommandés :

```yaml
Company:
  id: string
  name: string
  level: number
  xp: number
  gold: number
  provisions: number

Adventurer:
  id: string
  name: string
  role: warrior | ranger | mage | healer | artisan
  is_captain: boolean
  level: number
  xp: number
  status: available | expedition | resting | tired | injured

Expedition:
  id: string
  name: string
  description: string
  duration_minutes: number
  risk: low | medium | high
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

CampUpgrade:
  id: string
  name: string
  description: string
  level: number
  cost_gold: number
  effect: string
```

Repoussé après V1 :

- équipement détaillé ;
- objets rares ;
- traits de personnalité ;
- carte du monde ;
- registre de compagnie ;
- plusieurs expéditions simultanées.

---

## 9. Intégration Microsoft

Décisions :

- L’intégration Microsoft n’est pas obligatoire pour la V0/MVP.
- Elle est importante pour l’adoption réelle.
- Priorités souhaitées :
  - Calendar ;
  - To Do ;
  - Planner.
- Lecture seule acceptable au départ.
- Écriture souhaitée ensuite.
- QuestBoard doit rester utilisable hors réseau professionnel.
- L’utilisateur ne peut pas enregistrer d’application Entra ID / Azure AD pour cet usage.

Approche retenue :

1. **V0 / MVP** : calendrier local interne à QuestBoard.
2. **Étape intermédiaire** : import manuel ou semi-manuel depuis Outlook / Microsoft 365 si utile.
3. **Intégration Microsoft réelle** : chantier séparé après MVP, selon voie d’authentification acceptable.

Une section `Limites connues` doit documenter explicitement les contraintes Microsoft.

---

## 10. Architecture technique

Décisions :

- Stack validée :
  - **Frontend** : SvelteKit ;
  - **Backend** : FastAPI ;
  - **Base de données** : SQLite ;
  - **ORM / modèles** : SQLModel ou SQLAlchemy ;
  - **Déploiement** : local ;
  - **Docker Compose** : dès le début ;
  - **API** : propre dès le départ.
- Séparation stricte :
  - code ;
  - données ;
  - exports ;
  - sauvegardes.
- Pas de notifications Windows.
- Seulement des marqueurs discrets dans l’application.
- Sauvegarde/restauration non obligatoire en V1, mais les chemins doivent être structurés proprement.
- Le mode mobile n’est pas prioritaire tant que l’application reste strictement locale.

---

## 11. Roadmap stabilisée

### Phase 1 — Cadrage final V1

- Stabiliser les vues.
- Stabiliser le modèle de données.
- Valider la stack.
- Valider le scoring XP/or.
- Valider la première boucle RPG.
- Écrire le backlog initial.

### Phase 2 — V0 technique dockerisée

- Créer structure projet.
- Créer Docker Compose.
- Créer API FastAPI.
- Créer frontend SvelteKit.
- Créer base SQLite.
- Créer modèle Task minimal.
- Créer capture rapide.
- Créer clôture de tâche.
- Calculer XP/or.

### Phase 3 — MVP Dashboard

- Ajouter Inbox.
- Ajouter projets / domaines.
- Ajouter vue Aujourd’hui.
- Ajouter tâches en attente et date de relance.
- Ajouter vue relances.
- Ajouter notes.
- Ajouter liens externes simples.
- Ajouter calendrier local si raisonnable.

### Phase 4 — MVP Camp / première expédition

- Créer Company.
- Créer capitaine fondateur.
- Créer Camp.
- Créer ressources XP/or/provisions.
- Créer expédition V1.
- Lancer une expédition.
- Résoudre automatiquement l’expédition.
- Afficher rapport et récompenses.
- Acheter première amélioration : tente de repos.

### Phase 5 — Confort d’usage

- Historique.
- Journal de travail.
- Exports Markdown.
- Recherche simple.
- Filtres avancés.
- Icônes / couleurs par type.
- Achievements simples.

### Phase 6 — Intégration Microsoft

- Étudier contraintes d’authentification.
- Tester import manuel ou semi-manuel.
- Étudier Calendar.
- Étudier To Do.
- Étudier Planner.
- Évaluer écriture agenda si possible.

### Phase 7 — Évolutions RPG

- Recrutement d’autres aventuriers.
- Équipement.
- Objets rares.
- Traits de personnalité.
- Carte / lieux.
- Plusieurs expéditions.
- Visuels pixel art évolutifs du camp.

---

## 12. Risques principaux

Risques jugés les plus importants :

1. **Friction de saisie**.
2. **Intégration Microsoft**.

Risques complémentaires :

- surcomplexité ;
- données sensibles ;
- jeu trop distrayant ;
- abandon si la partie RPG arrive trop tard.

Mesures de réduction :

- capture rapide en un titre ;
- champs avancés optionnels ;
- Dashboard affiché par défaut ;
- mode discret ;
- local-first ;
- pas de notification Windows ;
- pas de clic répétitif ;
- une seule expédition active au départ ;
- aucune punition si le joueur ne revient pas ;
- intégration Microsoft traitée comme chantier séparé.

### Informations à éviter dans QuestBoard

Ne pas saisir dans QuestBoard :

- mots de passe ;
- secrets ;
- tokens ;
- clés API ;
- données personnelles détaillées d’agents ou d’usagers ;
- informations RH sensibles ;
- détails de sécurité trop précis exploitables par un tiers ;
- contenu complet de mails sensibles ;
- éléments confidentiels non nécessaires au suivi personnel.

Préférer :

- libellés sobres ;
- références de ticket ;
- résumés courts ;
- liens externes plutôt que copie complète du contenu.

Mode `libellés sobres` :

- recommandé plus tard, mais non prioritaire V1 ;
- il pourrait masquer les descriptions et n’afficher que titres courts, statuts, types et priorités.

Pas de séparation `pro / perso / test` dans l’application principale.

---

## 13. Documents associés

Les livrables de conception associés à ce cadrage sont :

- `docs/fiche-mvp.md` ;
- `docs/maquettes-textuelles.md`.

Ces documents détaillent respectivement :

- le périmètre MVP ;
- la V0 technique ;
- les critères d’acceptation ;
- les écrans principaux ;
- les comportements attendus de la capture rapide, du Dashboard, de l’Inbox, des Projets, du Calendrier local et du Camp.

---

## 14. Journal des décisions de conception

Décisions ajoutées ou confirmées dans les dernières itérations :

- Le nom produit devient **QuestBoard**.
- Le MVP vise `Dashboard + première expédition`.
- Une V0 technique courte est recommandée avant le MVP complet.
- Mode discret : masque le Camp et les éléments explicitement RPG.
- Vue Aujourd’hui : 8 tâches visibles par défaut, réglable.
- Vue Aujourd’hui : agenda dominant.
- Vue semaine souhaitée.
- Capture possible avec titre seul.
- Source issue d’une liste simple.
- Inbox dédiée.
- Bouton “transformer en…” souhaité.
- `gold_reward` n’est pas retenu comme champ direct sur `Task` en V1 ; l’or est calculé à la clôture selon la priorité et crédité à la compagnie.
- Liens externes simples prévus dès la V1.
- `Incident` reste séparé de `Interruption / imprévu`.
- Projet : affichage par défaut 5 à 7 actifs.
- Sous-quêtes repoussées.
- Capitaine jouable.
- Nom de compagnie personnalisable.
- Durées d’expédition V1 validées : 30 min, 1 h, 2 h.
- Taux de réussite affiché en libellé + pourcentage.
- Rapport d’expédition en court paragraphe.
- XP vers compagnie + capitaine.
- Or calculé principalement à partir de la priorité.
- Complexité `Majeure` côté Dashboard, `Boss` côté RPG.
- Provisions via routines + production minimale quotidienne.
- Objets rares repoussés après première boucle jouable.
- Première amélioration du camp : tente de repos.
- Classes V1 : Guerrier, Rôdeur, Mage, Soigneur, Artisan.
- Fondateur créé par le joueur.
- Traits de personnalité repoussés V2.
- Pas de journal de compagnie dédié.
- Journal de travail dans l’historique.
- Calendrier local V1 accepté si raisonnable.
- Intégration Microsoft = chantier séparé.
- Stack validée : SvelteKit + FastAPI + SQLite.
- Docker Compose dès le début.
- Bonus automatiques.
- Réunion = XP + or.
- Réunion organisée = bonus.
- Pas de bonus manuel de pénibilité en V1.
- Risques principaux : friction de saisie et intégration Microsoft.
- Le pixel art ne bloque pas la V0/MVP : placeholders d’abord, direction artistique ensuite.
- PixelLab est identifié comme piste possible pour l’aide à la génération d’assets, mais pas comme dépendance obligatoire.

---

## 15. Prochaine étape

La prochaine étape est de transformer ce cadrage en conception technique et tickets de réalisation.

Livrables suivants recommandés :

1. modèle de données V1 finalisé ;
2. backlog technique initial ;
3. structure de dépôt Dockerisée ;
4. premiers endpoints API ;
5. premier squelette SvelteKit / FastAPI / SQLite.
