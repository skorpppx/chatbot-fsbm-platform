"""PDF 2 - Frontend Angular Complet"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 02/10", "Frontend Angular Complet",
           "Angular 17 + TypeScript + Composants + Routing + Services",
           accent_color=HexColor('#DD0031'))

# TOC
story.append(Paragraph("Sommaire", ST_CHAPTER))
for label, page in [
    ("Chapitre 1 - C'est quoi Angular ?", "3"),
    ("Chapitre 2 - TypeScript : les bases", "7"),
    ("Chapitre 3 - Anatomie d'un composant Angular", "11"),
    ("Chapitre 4 - Templates et data binding", "16"),
    ("Chapitre 5 - Services et injection de dependance", "20"),
    ("Chapitre 6 - HttpClient et appels API", "24"),
    ("Chapitre 7 - Routing et lazy loading", "27"),
    ("Chapitre 8 - Signals (Angular 17)", "31"),
    ("Chapitre 9 - Layout shell explique", "34"),
    ("Chapitre 10 - Les 9 pages decortiquees", "37"),
    ("Chapitre 11 - Mode sombre et theme service", "44"),
    ("Chapitre 12 - Animations et responsive", "47"),
    ("Chapitre 13 - Build et deploiement", "50"),
]:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# CHAPITRE 1
story.append(Paragraph("Chapitre 1 - C'est quoi Angular ?", ST_CHAPTER))

story.append(Paragraph("1.1 Definition courte", ST_H1))
story.append(Paragraph(
    "<b>Angular</b> est un framework JavaScript (plus precisement TypeScript) developpe par "
    "<b>Google</b> depuis 2010. Il sert a construire des SPA (Single Page Applications) de "
    "facon structuree.",
    ST_BODY))

story.append(Paragraph("1.2 Histoire en bref", ST_H1))
story.append(std_table([
    ['Annee', 'Version', 'Note'],
    ['2010', 'AngularJS (v1)', 'Premiere version, JavaScript pur'],
    ['2016', 'Angular 2', 'Reecriture complete en TypeScript'],
    ['2018', 'Angular 6+', 'Stabilisation, releases tous les 6 mois'],
    ['2023', 'Angular 17', 'Standalone components officialise'],
    ['2024', 'Angular 18', 'Zoneless preview, ameliorations'],
], col_widths=[2*cm, 4*cm, 10*cm]))

story.append(alert_box(
    "Notre projet utilise <b>Angular 17.3</b>, sorti en mars 2024. C'est une version stable, "
    "supportee, avec toutes les nouveautes modernes (standalone, signals, control flow).",
    kind="info"))

story.append(Paragraph("1.3 Pourquoi Angular ?", ST_H1))
story.append(Paragraph(
    "Angular est un framework <b>opinionated</b> : il impose une structure et une maniere de "
    "faire. C'est a la fois sa force et sa faiblesse.",
    ST_BODY))
story.append(std_table([
    ['Forces', 'Faiblesses'],
    ['Structure imposee = code uniforme', 'Courbe d\'apprentissage raide'],
    ['Routing, forms, HTTP integres', 'Plus verbeux que React'],
    ['TypeScript par defaut (typage fort)', 'Bundle initial plus gros'],
    ['CLI puissant (ng generate)', 'Moins flexible que Vue/React'],
    ['Soutenu par Google', 'Conventions parfois rigides'],
    ['Excellent pour grosses apps', 'Overkill pour petits sites'],
], col_widths=[8*cm, 8*cm]))

story.append(analogy(
    "Angular est comme un <b>uniforme scolaire</b> : tout le monde est habille pareil, c'est "
    "moins fun mais on s'y retrouve. React est comme des <b>vetements libres</b> : plus de "
    "liberte, mais chacun fait son style et c'est moins coherent en equipe."))

story.append(Paragraph("1.4 Que produit Angular ?", ST_H1))
story.append(Paragraph(
    "Quand on lance <code>npm run build</code>, Angular produit :",
    ST_BODY))
for x in [
    "Un fichier <b>index.html</b> minimal (le 'P' de SPA)",
    "Plusieurs fichiers <b>.js</b> compresses (le code de l'application)",
    "Un fichier <b>styles.css</b> minifie",
    "Des <b>chunks</b> pour les pages lazy-loaded",
    "Des assets (images, fonts, logos)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph(
    "Ces fichiers sont servis par un serveur web (en dev: Angular dev server sur port 4200, "
    "en prod: nginx/Apache). Le navigateur les telecharge, execute le JS, et tout s'anime.",
    ST_BODY))
story.append(PageBreak())

# CHAPITRE 2 - TypeScript
story.append(Paragraph("Chapitre 2 - TypeScript : les bases", ST_CHAPTER))

story.append(Paragraph("2.1 C'est quoi TypeScript ?", ST_H1))
story.append(Paragraph(
    "<b>TypeScript</b> est un <b>sur-ensemble</b> de JavaScript developpe par Microsoft. "
    "Il ajoute un systeme de types statiques a JavaScript.",
    ST_BODY))

story.append(Paragraph("2.2 JavaScript vs TypeScript", ST_H1))
story.append(code(
    "// JavaScript (typage dynamique)\n"
    "function ajouter(a, b) {\n"
    "  return a + b;\n"
    "}\n"
    "ajouter(2, 3);         // 5  - OK\n"
    "ajouter(\"2\", \"3\");     // \"23\" - bug silencieux !\n"
    "\n"
    "// TypeScript (typage statique)\n"
    "function ajouter(a: number, b: number): number {\n"
    "  return a + b;\n"
    "}\n"
    "ajouter(2, 3);         // 5  - OK\n"
    "ajouter(\"2\", \"3\");     // ERREUR DE COMPILATION !"
))

story.append(Paragraph("2.3 Les types de base", ST_H1))
story.append(std_table([
    ['Type', 'Exemple', 'Description'],
    ['string', '"Hello"', 'Chaine de caracteres'],
    ['number', '42, 3.14', 'Nombre (entier ou decimal)'],
    ['boolean', 'true, false', 'Vrai ou faux'],
    ['null', 'null', 'Valeur absente intentionnellement'],
    ['undefined', 'undefined', 'Non defini'],
    ['any', '(tout)', 'Echappe le typage (a eviter !)'],
    ['void', '(rien)', 'Pour les fonctions sans retour'],
    ['number[]', '[1, 2, 3]', 'Tableau de nombres'],
    ['string[]', '["a", "b"]', 'Tableau de strings'],
    ['{name: string}', '{name: "Akram"}', 'Objet typé'],
], col_widths=[3.5*cm, 4*cm, 8.5*cm]))

story.append(Paragraph("2.4 Interfaces", ST_H1))
story.append(Paragraph(
    "Les interfaces definissent la forme d'un objet :",
    ST_BODY))
story.append(code(
    "interface Message {\n"
    "  id: number;\n"
    "  sender: 'bot' | 'user';   // type union\n"
    "  text: string;\n"
    "  timestamp: Date;\n"
    "  intent?: string;          // ? = optionnel\n"
    "  confidence?: number;\n"
    "}\n"
    "\n"
    "// Utilisation\n"
    "const msg: Message = {\n"
    "  id: 1,\n"
    "  sender: 'user',\n"
    "  text: 'Bonjour',\n"
    "  timestamp: new Date()\n"
    "  // intent et confidence sont optionnels\n"
    "};"
))

story.append(Paragraph("2.5 Classes", ST_H1))
story.append(code(
    "class ChatService {\n"
    "  // Proprietes typees\n"
    "  private apiUrl: string = '/api';\n"
    "  \n"
    "  // Constructeur avec parametres typés\n"
    "  constructor(private http: HttpClient) {}\n"
    "  \n"
    "  // Methode typée\n"
    "  sendMessage(message: string): Observable<ChatResponse> {\n"
    "    return this.http.post<ChatResponse>(\n"
    "      `${this.apiUrl}/chat`,\n"
    "      { message }\n"
    "    );\n"
    "  }\n"
    "}"
))

story.append(Paragraph("2.6 Les avantages du typage", ST_H1))
for x in [
    "<b>Erreurs detectees a la compilation</b> au lieu d'au runtime",
    "<b>Autocompletion</b> dans l'IDE (VSCode propose les methodes/proprietes)",
    "<b>Refactoring</b> sur : on renomme une variable, le compilateur trouve tous les usages",
    "<b>Documentation vivante</b> : le type EST la documentation",
    "<b>Confiance</b> : si ca compile, ca a une bonne chance de marcher",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))
story.append(PageBreak())

# CHAPITRE 3 - Composants
story.append(Paragraph("Chapitre 3 - Anatomie d'un composant Angular", ST_CHAPTER))

story.append(Paragraph("3.1 Qu'est-ce qu'un composant ?", ST_H1))
story.append(Paragraph(
    "Un <b>composant</b> est l'unite de base d'une application Angular. Il combine 3 choses :",
    ST_BODY))
for x in [
    "<b>Template HTML</b> : ce qu'on voit a l'ecran",
    "<b>Logique TypeScript</b> : le comportement",
    "<b>Styles CSS</b> : l'apparence",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(analogy(
    "Un composant est comme une <b>brique LEGO</b>. Tu peux combiner plusieurs briques pour "
    "construire des structures complexes. Notre app a 28 briques (composants) au total."))

story.append(Paragraph("3.2 Exemple complet - typing-indicator", ST_H1))
story.append(code(
    "import { Component } from '@angular/core';\n"
    "\n"
    "@Component({\n"
    "  selector: 'app-typing-indicator',  // balise HTML personnalisee\n"
    "  standalone: true,                   // composant autonome\n"
    "  template: `\n"
    "    <div class=\"typing-indicator\">\n"
    "      <div class=\"typing-dot\"></div>\n"
    "      <div class=\"typing-dot\"></div>\n"
    "      <div class=\"typing-dot\"></div>\n"
    "    </div>\n"
    "  `\n"
    "})\n"
    "export class TypingIndicatorComponent {}"
))

story.append(Paragraph(
    "Maintenant, dans un autre composant, on peut l'utiliser comme une balise HTML :",
    ST_BODY))
story.append(code(
    "<app-typing-indicator></app-typing-indicator>\n"
    "// ou simplement\n"
    "<app-typing-indicator />"
))

story.append(Paragraph("3.3 Le decorateur @Component", ST_H1))
story.append(Paragraph(
    "<code>@Component</code> est un <b>decorateur</b>. C'est une syntaxe TypeScript qui "
    "permet d'attacher des metadonnees a une classe. Angular les utilise pour comprendre "
    "ce qu'est cette classe.",
    ST_BODY))
story.append(std_table([
    ['Propriete', 'Role'],
    ['selector', 'Nom de la balise HTML (ex: <app-chat>)'],
    ['standalone', 'true = pas besoin de NgModule (Angular 17+)'],
    ['imports', 'Liste des dependances (autres composants, modules)'],
    ['template', 'HTML inline'],
    ['templateUrl', 'Ou fichier HTML externe'],
    ['styles', 'CSS inline'],
    ['styleUrl', 'Ou fichier CSS externe'],
], col_widths=[3*cm, 13*cm]))

story.append(Paragraph("3.4 @Input et @Output", ST_H1))
story.append(Paragraph(
    "Pour communiquer entre composants :",
    ST_BODY))
story.append(Paragraph("@Input : recevoir des donnees du parent", ST_H2))
story.append(code(
    "// Enfant : message-bubble.component.ts\n"
    "export class MessageBubbleComponent {\n"
    "  @Input() message!: Message;  // ! = sera defini\n"
    "}\n"
    "\n"
    "// Parent : chat-window.component.html\n"
    "<app-message-bubble [message]=\"msg\" />"
))

story.append(Paragraph("@Output : envoyer des evenements au parent", ST_H2))
story.append(code(
    "// Enfant : input-bar.component.ts\n"
    "export class InputBarComponent {\n"
    "  @Output() sendMessage = new EventEmitter<string>();\n"
    "  \n"
    "  onClick() {\n"
    "    this.sendMessage.emit(this.message);\n"
    "  }\n"
    "}\n"
    "\n"
    "// Parent : chat-window.component.html\n"
    "<app-input-bar (sendMessage)=\"handleSend($event)\" />"
))

story.append(Paragraph("3.5 Les hooks de cycle de vie", ST_H1))
story.append(Paragraph(
    "Angular appelle des methodes a des moments precis du cycle de vie d'un composant :",
    ST_BODY))
story.append(std_table([
    ['Hook', 'Quand est-il appele'],
    ['ngOnInit', 'Apres l\'initialisation (1 fois)'],
    ['ngOnChanges', 'Quand un @Input change'],
    ['ngAfterViewInit', 'Apres le rendu du template'],
    ['ngAfterViewChecked', 'Apres chaque check du template'],
    ['ngOnDestroy', 'Juste avant la destruction du composant'],
], col_widths=[4*cm, 12*cm]))

story.append(code(
    "export class ChatWindowComponent implements OnInit, AfterViewChecked {\n"
    "  ngOnInit() {\n"
    "    // Initialise le 1er message d'accueil\n"
    "    this.messages.push({ id: 0, sender: 'bot', text: 'Bonjour !'});\n"
    "  }\n"
    "  \n"
    "  ngAfterViewChecked() {\n"
    "    // Scroll auto vers le bas a chaque nouveau message\n"
    "    if (this.messagesEnd) {\n"
    "      this.messagesEnd.nativeElement.scrollIntoView();\n"
    "    }\n"
    "  }\n"
    "}"
))
story.append(PageBreak())

# CHAPITRE 4 - Templates
story.append(Paragraph("Chapitre 4 - Templates et data binding", ST_CHAPTER))

story.append(Paragraph("4.1 Interpolation : {{ }}", ST_H1))
story.append(Paragraph(
    "Pour afficher une valeur de la classe dans le template :",
    ST_BODY))
story.append(code(
    "// TS\n"
    "export class Component {\n"
    "  name = 'Akram';\n"
    "  count = 42;\n"
    "}\n"
    "\n"
    "// HTML\n"
    "<p>Bonjour {{ name }}, j'ai {{ count }} messages.</p>\n"
    "// Affiche : Bonjour Akram, j'ai 42 messages."
))

story.append(Paragraph("4.2 Property binding : [propriete]", ST_H1))
story.append(Paragraph(
    "Pour lier une propriete HTML a une valeur dynamique :",
    ST_BODY))
story.append(code(
    "<img [src]=\"logoUrl\" [alt]=\"logoAlt\" />\n"
    "<button [disabled]=\"isLoading\">Envoyer</button>\n"
    "<div [class.active]=\"isSelected\">..</div>\n"
    "<div [style.color]=\"textColor\">..</div>"
))

story.append(Paragraph("4.3 Event binding : (evenement)", ST_H1))
story.append(Paragraph(
    "Pour reagir aux evenements utilisateur :",
    ST_BODY))
story.append(code(
    "<button (click)=\"handleClick()\">Cliquer</button>\n"
    "<input (input)=\"handleInput($event)\" />\n"
    "<input (keydown.enter)=\"handleEnter()\" />\n"
    "<form (submit)=\"handleSubmit()\">..</form>"
))

story.append(Paragraph("4.4 Two-way binding : [(ngModel)]", ST_H1))
story.append(Paragraph(
    "Pour synchroniser une variable avec un champ formulaire :",
    ST_BODY))
story.append(code(
    "// TS\n"
    "export class Component {\n"
    "  username = '';\n"
    "}\n"
    "\n"
    "// HTML\n"
    "<input [(ngModel)]=\"username\" placeholder=\"Nom...\" />\n"
    "<p>Bonjour {{ username }}</p>\n"
    "// Quand on tape dans l'input, username se met a jour\n"
    "// ET le paragraph s'update en temps reel"
))

story.append(Paragraph("4.5 Directives structurelles", ST_H1))
story.append(Paragraph("@if / @for / @switch (Angular 17+)", ST_H2))
story.append(code(
    "@if (user) {\n"
    "  <p>Connecte : {{ user.name }}</p>\n"
    "} @else {\n"
    "  <p>Non connecte</p>\n"
    "}\n"
    "\n"
    "@for (item of items; track item.id) {\n"
    "  <li>{{ item.name }}</li>\n"
    "}\n"
    "\n"
    "@switch (status) {\n"
    "  @case ('online') { <span>En ligne</span> }\n"
    "  @case ('away')   { <span>Absent</span> }\n"
    "  @default         { <span>Hors ligne</span> }\n"
    "}"
))

story.append(Paragraph("Anciennes directives *ngIf / *ngFor", ST_H2))
story.append(code(
    "<p *ngIf=\"user\">Connecte : {{ user.name }}</p>\n"
    "<p *ngIf=\"!user\">Non connecte</p>\n"
    "\n"
    "<li *ngFor=\"let item of items\">{{ item.name }}</li>"
))
story.append(alert_box(
    "Notre projet utilise principalement les <b>anciennes directives</b> (*ngIf, *ngFor). "
    "C'est OK et toujours supporté. Pour un nouveau projet, prefere @if / @for.",
    kind="info"))
story.append(PageBreak())

# CHAPITRE 5 - Services
story.append(Paragraph("Chapitre 5 - Services et injection de dependance", ST_CHAPTER))

story.append(Paragraph("5.1 C'est quoi un service ?", ST_H1))
story.append(Paragraph(
    "Un <b>service</b> est une classe qui contient de la logique reutilisable. "
    "Typiquement : appels HTTP, gestion d'etat global, calculs metier.",
    ST_BODY))

story.append(analogy(
    "Si les composants sont des <b>vendeurs</b> dans un magasin, les services sont les "
    "<b>fournisseurs</b>. Les vendeurs demandent aux fournisseurs ce dont ils ont besoin. "
    "Tous les vendeurs partagent les memes fournisseurs."))

story.append(Paragraph("5.2 Exemple : ChatService", ST_H1))
story.append(code(
    "import { Injectable } from '@angular/core';\n"
    "import { HttpClient } from '@angular/common/http';\n"
    "import { Observable } from 'rxjs';\n"
    "\n"
    "@Injectable({ providedIn: 'root' })  // singleton dans toute l'app\n"
    "export class ChatService {\n"
    "  private apiUrl = '/api';\n"
    "  \n"
    "  constructor(private http: HttpClient) {}\n"
    "  \n"
    "  sendMessage(message: string, sessionId: string): Observable<ChatResponse> {\n"
    "    return this.http.post<ChatResponse>(\n"
    "      `${this.apiUrl}/chat`,\n"
    "      { message, session_id: sessionId }\n"
    "    );\n"
    "  }\n"
    "  \n"
    "  sendFeedback(payload: FeedbackPayload) {\n"
    "    return this.http.post(`${this.apiUrl}/feedback`, payload);\n"
    "  }\n"
    "}"
))

story.append(Paragraph("5.3 Injection de dependance", ST_H1))
story.append(Paragraph(
    "L'injection de dependance (DI) est le pattern par lequel Angular fournit "
    "automatiquement les services aux composants qui en ont besoin.",
    ST_BODY))
story.append(Paragraph("Methode 1 : Constructor injection (ancien)", ST_H2))
story.append(code(
    "export class ChatPageComponent {\n"
    "  constructor(private chatService: ChatService) {}\n"
    "  \n"
    "  send(text: string) {\n"
    "    this.chatService.sendMessage(text, 'sess').subscribe(...);\n"
    "  }\n"
    "}"
))
story.append(Paragraph("Methode 2 : inject() function (Angular 14+)", ST_H2))
story.append(code(
    "import { inject } from '@angular/core';\n"
    "\n"
    "export class ChatPageComponent {\n"
    "  private chatService = inject(ChatService);\n"
    "  \n"
    "  send(text: string) {\n"
    "    this.chatService.sendMessage(text, 'sess').subscribe(...);\n"
    "  }\n"
    "}"
))

story.append(alert_box(
    "Avantage : pas besoin de constructeur, plus concis, fonctionne aussi dans les guards "
    "et resolvers (la ou il n'y a pas de constructeur).",
    kind="tip"))

story.append(Paragraph("5.4 providedIn", ST_H1))
story.append(Paragraph(
    "<code>providedIn: 'root'</code> indique que le service est un <b>singleton global</b> : "
    "une seule instance partagee dans toute l'application. C'est ce qu'on veut pour 99% des "
    "services.",
    ST_BODY))
story.append(PageBreak())

# CHAPITRE 6 - HttpClient
story.append(Paragraph("Chapitre 6 - HttpClient et appels API", ST_CHAPTER))

story.append(Paragraph("6.1 Configuration", ST_H1))
story.append(Paragraph(
    "HttpClient doit etre enregistre au bootstrap de l'app :",
    ST_BODY))
story.append(code(
    "// main.ts\n"
    "import { provideHttpClient } from '@angular/common/http';\n"
    "import { bootstrapApplication } from '@angular/platform-browser';\n"
    "\n"
    "bootstrapApplication(AppComponent, {\n"
    "  providers: [\n"
    "    provideHttpClient(),\n"
    "    provideAnimations(),\n"
    "    provideRouter(routes),\n"
    "  ]\n"
    "}).catch(err => console.error(err));"
))

story.append(Paragraph("6.2 Les 4 methodes principales", ST_H1))
story.append(code(
    "// GET\n"
    "this.http.get<Filiere[]>('/api/academic/filieres')\n"
    "  .subscribe(filieres => console.log(filieres));\n"
    "\n"
    "// POST avec body\n"
    "this.http.post<ChatResponse>(\n"
    "  '/api/chat',\n"
    "  { message: 'Bonjour' }\n"
    ").subscribe(resp => console.log(resp));\n"
    "\n"
    "// PUT\n"
    "this.http.put(`/api/users/${id}`, payload).subscribe();\n"
    "\n"
    "// DELETE\n"
    "this.http.delete(`/api/messages/${id}`).subscribe();"
))

story.append(Paragraph("6.3 Observables et subscribe", ST_H1))
story.append(Paragraph(
    "HttpClient retourne des <b>Observables</b> (RxJS). C'est comme une Promise, mais en "
    "plus puissant. Pour declencher la requete, il faut <code>.subscribe()</code>.",
    ST_BODY))
story.append(code(
    "this.chatService.sendMessage('Bonjour', 'sess')\n"
    "  .subscribe({\n"
    "    next: (response) => {\n"
    "      // Succes : la reponse est arrivee\n"
    "      this.messages.push({ text: response.response, ... });\n"
    "    },\n"
    "    error: (err) => {\n"
    "      // Erreur : reseau, 4xx, 5xx\n"
    "      console.error('Erreur', err);\n"
    "    },\n"
    "    complete: () => {\n"
    "      // Fini (souvent inutile pour HTTP)\n"
    "    }\n"
    "  });"
))

story.append(Paragraph("6.4 Operateurs RxJS utiles", ST_H1))
story.append(code(
    "import { catchError, map, of } from 'rxjs';\n"
    "\n"
    "this.http.get<Filiere[]>('/api/academic/filieres').pipe(\n"
    "  map(filieres => filieres.filter(f => f.is_active)),\n"
    "  catchError(err => {\n"
    "    console.error(err);\n"
    "    return of([]);  // fallback : liste vide\n"
    "  })\n"
    ").subscribe(active => console.log(active));"
))
story.append(PageBreak())

# CHAPITRE 7 - Routing
story.append(Paragraph("Chapitre 7 - Routing et lazy loading", ST_CHAPTER))

story.append(Paragraph("7.1 Configuration des routes", ST_H1))
story.append(Paragraph(
    "Notre fichier <code>app.routes.ts</code> definit toutes les pages :",
    ST_BODY))
story.append(code(
    "import { Routes } from '@angular/router';\n"
    "\n"
    "export const routes: Routes = [\n"
    "  {\n"
    "    path: '',\n"
    "    pathMatch: 'full',\n"
    "    loadComponent: () =>\n"
    "      import('./features/dashboard/dashboard.component')\n"
    "        .then(m => m.DashboardComponent),\n"
    "    title: 'Accueil - Chatbot FSBM',\n"
    "  },\n"
    "  {\n"
    "    path: 'chat',\n"
    "    loadComponent: () =>\n"
    "      import('./features/chat/chat-page.component')\n"
    "        .then(m => m.ChatPageComponent),\n"
    "  },\n"
    "  // ... 7 autres routes\n"
    "  { path: '**', redirectTo: '' },  // fallback 404\n"
    "];"
))

story.append(Paragraph("7.2 Lazy loading explique", ST_H1))
story.append(Paragraph(
    "<code>loadComponent</code> est la magie : la page n'est <b>pas chargee au depart</b>. "
    "Quand l'utilisateur clique sur le lien /chat, Angular telecharge LE chunk JS de chat "
    "(~20 KB), puis l'affiche.",
    ST_BODY))

story.append(analogy(
    "Au lieu de telecharger un dictionnaire complet (lourd), tu telecharges les pages au "
    "fur et a mesure que tu as besoin de chaque mot. Plus rapide au demarrage, et tu ne "
    "telecharge que ce que tu utilises vraiment."))

story.append(Paragraph("7.3 Navigation programmatique", ST_H1))
story.append(code(
    "import { Router } from '@angular/router';\n"
    "import { inject } from '@angular/core';\n"
    "\n"
    "export class HomeComponent {\n"
    "  private router = inject(Router);\n"
    "  \n"
    "  startChat() {\n"
    "    this.router.navigate(['/chat']);\n"
    "  }\n"
    "  \n"
    "  viewFiliere(code: string) {\n"
    "    this.router.navigate(['/filieres', code]);\n"
    "  }\n"
    "}"
))

story.append(Paragraph("7.4 Liens dans le template", ST_H1))
story.append(code(
    "<!-- routerLink declenche la navigation -->\n"
    "<a routerLink=\"/chat\">Ouvrir le chat</a>\n"
    "\n"
    "<!-- Avec parametres -->\n"
    "<a [routerLink]=\"['/filieres', filiere.code]\">\n"
    "  Voir {{ filiere.name }}\n"
    "</a>\n"
    "\n"
    "<!-- routerLinkActive ajoute une classe quand actif -->\n"
    "<a routerLink=\"/filieres\" routerLinkActive=\"active\">\n"
    "  Filieres\n"
    "</a>"
))

story.append(Paragraph("7.5 Recuperer les parametres d'URL", ST_H1))
story.append(code(
    "import { ActivatedRoute } from '@angular/router';\n"
    "\n"
    "export class FiliereDetailComponent implements OnInit {\n"
    "  private route = inject(ActivatedRoute);\n"
    "  filiere: Filiere | null = null;\n"
    "  \n"
    "  ngOnInit() {\n"
    "    this.route.params.subscribe(params => {\n"
    "      const code = params['code'];  // recupere :code de l'URL\n"
    "      this.loadFiliere(code);\n"
    "    });\n"
    "  }\n"
    "}"
))
story.append(PageBreak())

# CHAPITRE 8 - Signals
story.append(Paragraph("Chapitre 8 - Signals (Angular 17)", ST_CHAPTER))

story.append(Paragraph("8.1 C'est quoi un Signal ?", ST_H1))
story.append(Paragraph(
    "Un <b>Signal</b> est une <b>valeur reactive</b> introduite dans Angular 17. Quand sa "
    "valeur change, tous les composants qui l'utilisent sont automatiquement mis a jour.",
    ST_BODY))

story.append(Paragraph("8.2 Creer et utiliser un signal", ST_H1))
story.append(code(
    "import { signal, computed } from '@angular/core';\n"
    "\n"
    "export class ThemeService {\n"
    "  // Creation d'un signal\n"
    "  readonly theme = signal<'light' | 'dark'>('light');\n"
    "  \n"
    "  // Signal calculé\n"
    "  readonly isDark = computed(() => this.theme() === 'dark');\n"
    "  \n"
    "  // Lecture (appel comme une fonction)\n"
    "  current() {\n"
    "    return this.theme();\n"
    "  }\n"
    "  \n"
    "  // Modification\n"
    "  toggle() {\n"
    "    this.theme.set(this.theme() === 'light' ? 'dark' : 'light');\n"
    "    // ou\n"
    "    this.theme.update(v => v === 'light' ? 'dark' : 'light');\n"
    "  }\n"
    "}"
))

story.append(Paragraph("8.3 Dans un template", ST_H1))
story.append(code(
    "<!-- Lire un signal : appeler comme une fonction -->\n"
    "<p>Theme actuel : {{ theme.theme() }}</p>\n"
    "\n"
    "<!-- Conditionnel base sur signal -->\n"
    "@if (theme.isDark()) {\n"
    "  <span>🌙 Mode sombre</span>\n"
    "} @else {\n"
    "  <span>☀️ Mode clair</span>\n"
    "}\n"
    "\n"
    "<!-- Boutton qui change le signal -->\n"
    "<button (click)=\"theme.toggle()\">Changer</button>"
))

story.append(Paragraph("8.4 Signals vs Observables", ST_H1))
story.append(std_table([
    ['Critere', 'Signal', 'Observable (RxJS)'],
    ['Synchrone', 'OUI (lecture instantanee)', 'NON (besoin subscribe)'],
    ['Memoire', 'Reactive automatique', 'Manuel'],
    ['Complexite', 'Simple', 'Plus puissant'],
    ['Use case', 'Etat local', 'Streams asynchrones'],
    ['Cas FSBM', 'Theme, toggle UI', 'Appels HTTP'],
], col_widths=[3*cm, 6*cm, 7*cm]))

story.append(alert_box(
    "Notre projet utilise les Signals pour le theme service, le toggle LLM, et l'etat local "
    "des composants chat. Les Observables restent pour les appels HTTP.",
    kind="tip"))
story.append(PageBreak())

# CHAPITRE 9 - Layout shell
story.append(Paragraph("Chapitre 9 - Layout shell explique", ST_CHAPTER))

story.append(Paragraph("9.1 Structure", ST_H1))
story.append(Paragraph(
    "Le <code>AppShellComponent</code> est le <b>squelette</b> partage par toutes les pages. "
    "Il contient la sidebar de navigation, la topbar avec le logo FSBM, et un emplacement "
    "<code>&lt;router-outlet/&gt;</code> ou Angular injecte la page courante.",
    ST_BODY))

story.append(diagram(
    "  +-----------------+----------------------------+\n"
    "  | [Logo FSBM]     | [Topbar FSBM banner]       |\n"
    "  | [Collapse btn]  | [Status pill] [Chat btn]   |\n"
    "  +-----------------+----------------------------+\n"
    "  | 🏠 Accueil      |                            |\n"
    "  | 🤖 Chat IA     |                            |\n"
    "  | 🏢 Departements |                            |\n"
    "  | 📚 Filieres     |   <router-outlet />        |\n"
    "  | 📖 Modules      |   (page courante injectee  |\n"
    "  | 👨🏫 Profs        |    automatiquement par    |\n"
    "  | 📰 Actualites   |    Angular Router)         |\n"
    "  | 🌟 Vie etudiant |                            |\n"
    "  |                 |                            |\n"
    "  | [🌙 Toggle dark]|                            |\n"
    "  +-----------------+----------------------------+\n"
))

story.append(Paragraph("9.2 Code TypeScript principal", ST_H1))
story.append(code(
    "@Component({\n"
    "  selector: 'app-shell',\n"
    "  standalone: true,\n"
    "  imports: [CommonModule, RouterLink, RouterLinkActive, RouterOutlet],\n"
    "  templateUrl: './app-shell.component.html',\n"
    "  styleUrl: './app-shell.component.css',\n"
    "})\n"
    "export class AppShellComponent {\n"
    "  readonly theme = inject(ThemeService);\n"
    "  readonly collapsed = signal(false);\n"
    "  readonly isDark = computed(() => this.theme.theme() === 'dark');\n"
    "  \n"
    "  readonly navItems = [\n"
    "    { path: '/',              icon: '🏠', label: 'Accueil', exact: true },\n"
    "    { path: '/chat',          icon: '🤖', label: 'Assistant IA' },\n"
    "    { path: '/departements',  icon: '🏢', label: 'Departements' },\n"
    "    { path: '/filieres',      icon: '📚', label: 'Filieres' },\n"
    "    { path: '/modules',       icon: '📖', label: 'Modules' },\n"
    "    { path: '/professeurs',   icon: '👨🏫', label: 'Professeurs' },\n"
    "    { path: '/actualites',    icon: '📰', label: 'Actualites' },\n"
    "    { path: '/vie-etudiante', icon: '🌟', label: 'Vie etudiante' },\n"
    "  ];\n"
    "  \n"
    "  toggleCollapse() {\n"
    "    this.collapsed.update(v => !v);\n"
    "  }\n"
    "}"
))

story.append(Paragraph("9.3 Comment ca s'integre", ST_H1))
story.append(code(
    "// app.component.ts\n"
    "@Component({\n"
    "  selector: 'app-root',\n"
    "  standalone: true,\n"
    "  imports: [AppShellComponent],\n"
    "  template: `<app-shell />`,  // affiche le shell\n"
    "})\n"
    "export class AppComponent {}"
))
story.append(PageBreak())

# CHAPITRE 10 - 9 pages
story.append(Paragraph("Chapitre 10 - Les 9 pages decortiquees", ST_CHAPTER))

pages = [
    ("Dashboard (/)", "DashboardComponent",
     "Affiche : Hero anime + 8 cartes stats (live academic-service) + 4 dernieres annonces + "
     "3 prochains evenements + 4 actions rapides. Au ngOnInit, lance 3 appels HTTP en "
     "parallele (overview, announcements, events). Si backend down, affiche un warning."),
    ("Chat (/chat)", "ChatPageComponent + ChatWindowComponent",
     "Interface chat avec messages bubbles, indicator typing, input bar, quick actions. "
     "Maintient un sessionId unique. Toggle TF-IDF/LLM en haut a droite. Personnalise via "
     "memory backend (genre, nom, historique 10 tours)."),
    ("Departements (/departements)", "DepartmentsComponent",
     "5 cartes avec couleur par departement (CSS variable --dept-color). Chaque carte affiche "
     "chef, email, telephone, lien vers ses filieres."),
    ("Filieres (/filieres)", "FilieresComponent",
     "Liste de 25 filieres avec barre de recherche debouncee et chips de filtres "
     "(Licence/Master/Pro/Recherche). Utilise computed() pour filtrer en temps reel."),
    ("Detail filiere (/filieres/:code)", "FiliereDetailComponent",
     "Recupere le code depuis l'URL. Charge filiere par code + modules groupes par semestre. "
     "Affiche hero gradient (different selon licence/master), objectifs, debouches, programme S1-S6."),
    ("Modules (/modules)", "ModulesComponent",
     "100+ modules avec 3 filtres : recherche texte, filiere (dropdown), semestre (1-6). "
     "Carte par module avec code, semestre, ECTS, coefficient, heures cours/TD/TP."),
    ("Professeurs (/professeurs)", "ProfessorsComponent",
     "Annuaire de 107 profs paginé (12/page) avec : recherche, filtre departement, "
     "filtre grade (PA/PH/PES/Vacataire). Avatar = initiales. Email cliquable."),
    ("Actualites (/actualites)", "NewsComponent",
     "Layout 2 colonnes : annonces officielles (colonne large) + evenements a venir "
     "(sidebar). Badges colorés selon type (URGENT/EXAMEN/EVENT/VACANCE). Lien inscription "
     "evenement si disponible."),
    ("Vie etudiante (/vie-etudiante)", "StudentLifeComponent",
     "Grille de 8 clubs avec couleur de bordure selon categorie "
     "(SCIENTIFIQUE/TECHNIQUE/CULTUREL/SPORTIF/HUMANITAIRE). Reseaux sociaux cliquables."),
]
for url, comp, desc in pages:
    story.append(Paragraph(f"<b>{url}</b>", ST_H2))
    story.append(Paragraph(f"<b>Composant :</b> <code>{comp}</code>", ST_BODY))
    story.append(Paragraph(desc, ST_BODY))
    story.append(Spacer(1, 0.2*cm))
story.append(PageBreak())

# CHAPITRE 11 - Mode sombre
story.append(Paragraph("Chapitre 11 - Mode sombre et theme service", ST_CHAPTER))

story.append(Paragraph("11.1 Architecture", ST_H1))
story.append(Paragraph(
    "Le mode sombre repose sur 3 piliers :",
    ST_BODY))
for x in [
    "<b>ThemeService</b> : signal qui contient 'light' ou 'dark'",
    "<b>Variables CSS</b> dans styles.css : --primary, --bg, --surface, etc.",
    "<b>Attribut HTML</b> : <code>data-theme</code> sur la racine, ecoute par CSS",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("11.2 Code complet du service", ST_H1))
story.append(code(
    "import { Injectable, signal } from '@angular/core';\n"
    "\n"
    "@Injectable({ providedIn: 'root' })\n"
    "export class ThemeService {\n"
    "  private readonly STORAGE_KEY = 'fsbm-theme';\n"
    "  readonly theme = signal<'light' | 'dark'>('light');\n"
    "  \n"
    "  constructor() {\n"
    "    // 1. Recuperer la preference depuis localStorage\n"
    "    const stored = localStorage.getItem(this.STORAGE_KEY);\n"
    "    // 2. Fallback : detecter le theme systeme du navigateur\n"
    "    const initial = stored || (\n"
    "      window.matchMedia('(prefers-color-scheme: dark)').matches\n"
    "        ? 'dark' : 'light'\n"
    "    );\n"
    "    this.applyTheme(initial as 'light' | 'dark');\n"
    "  }\n"
    "  \n"
    "  toggle() {\n"
    "    this.applyTheme(this.theme() === 'light' ? 'dark' : 'light');\n"
    "  }\n"
    "  \n"
    "  private applyTheme(value: 'light' | 'dark') {\n"
    "    this.theme.set(value);\n"
    "    document.documentElement.setAttribute('data-theme', value);\n"
    "    localStorage.setItem(this.STORAGE_KEY, value);\n"
    "  }\n"
    "}"
))

story.append(Paragraph("11.3 Variables CSS", ST_H1))
story.append(code(
    ":root,\n"
    "[data-theme=\"light\"] {\n"
    "  --primary:     #1C3F6E;\n"
    "  --accent:      #16B5A6;\n"
    "  --bg:          #F4F7FA;\n"
    "  --surface:     #FFFFFF;\n"
    "  --text-dark:   #1A2638;\n"
    "  --border:      #DDE4ED;\n"
    "  /* ... */\n"
    "}\n"
    "\n"
    "[data-theme=\"dark\"] {\n"
    "  --primary:     #5B8FE3;\n"
    "  --accent:      #25D0BF;\n"
    "  --bg:          #0F1620;\n"
    "  --surface:     #1A2333;\n"
    "  --text-dark:   #F1F5F9;\n"
    "  --border:      #2A3548;\n"
    "  /* ... */\n"
    "}\n"
    "\n"
    "/* Tous les composants utilisent les variables */\n"
    ".card {\n"
    "  background: var(--surface);\n"
    "  color: var(--text-dark);\n"
    "  border: 1px solid var(--border);\n"
    "  transition: background 0.3s, color 0.3s;\n"
    "}"
))

story.append(alert_box(
    "Quand le service change <code>data-theme</code> sur &lt;html&gt;, TOUTES les "
    "variables CSS basculent automatiquement. Les composants n'ont rien a faire - ils "
    "utilisent juste <code>var(--primary)</code> etc.",
    kind="tip"))
story.append(PageBreak())

# CHAPITRE 12 - Animations + responsive
story.append(Paragraph("Chapitre 12 - Animations et responsive", ST_CHAPTER))

story.append(Paragraph("12.1 Animations CSS", ST_H1))
story.append(Paragraph(
    "Notre projet utilise des animations CSS pures (pas Angular Animations API pour rester "
    "simple). Exemple de l'apparition des cartes :",
    ST_BODY))
story.append(code(
    "@keyframes fadeInUp {\n"
    "  from { opacity: 0; transform: translateY(12px); }\n"
    "  to   { opacity: 1; transform: translateY(0); }\n"
    "}\n"
    ".fade-in-up {\n"
    "  animation: fadeInUp 0.4s ease both;\n"
    "}\n"
    "\n"
    "/* Delay pour stagger effect */\n"
    ".stat-card:nth-child(1) { animation-delay: 0ms; }\n"
    ".stat-card:nth-child(2) { animation-delay: 50ms; }\n"
    ".stat-card:nth-child(3) { animation-delay: 100ms; }"
))

story.append(Paragraph("12.2 Responsive design", ST_H1))
story.append(Paragraph(
    "Les media queries adaptent l'affichage selon la taille d'ecran :",
    ST_BODY))
story.append(code(
    "/* Desktop par defaut */\n"
    ".shell {\n"
    "  grid-template-columns: 260px 1fr;  /* sidebar 260px + contenu */\n"
    "}\n"
    "\n"
    "/* Tablette */\n"
    "@media (max-width: 1024px) {\n"
    "  .topbar { padding: 14px 20px; }\n"
    "  .content { padding: 22px; }\n"
    "}\n"
    "\n"
    "/* Mobile */\n"
    "@media (max-width: 768px) {\n"
    "  .shell { grid-template-columns: 76px 1fr; }  /* sidebar mini */\n"
    "  .nav-label, .theme-label { display: none; }\n"
    "  .status-pill { display: none; }\n"
    "}"
))

story.append(Paragraph("12.3 Quelques chiffres", ST_H1))
story.append(std_table([
    ['Metrique', 'Valeur'],
    ['Bundle initial', '~175 KB (gzipped : ~50 KB)'],
    ['Premier rendu (FCP)', '< 1 seconde'],
    ['Time to interactive', '< 1.5 seconde'],
    ['Chaque chunk lazy', '10-30 KB'],
    ['Animations FPS', '60 fps stable'],
    ['Score Lighthouse', '90+ Performance'],
], col_widths=[6*cm, 10*cm]))
story.append(PageBreak())

# CHAPITRE 13 - Build deployment
story.append(Paragraph("Chapitre 13 - Build et deploiement", ST_CHAPTER))

story.append(Paragraph("13.1 Commandes essentielles", ST_H1))
story.append(code(
    "# Installation des dependances (premiere fois)\n"
    "npm install\n"
    "\n"
    "# Dev server (avec hot reload)\n"
    "npm start\n"
    "# ou : npx ng serve\n"
    "# -> http://localhost:4200\n"
    "\n"
    "# Build production\n"
    "npm run build:prod\n"
    "# -> dist/chatbot-fsbm/  (HTML + JS + CSS minifies)\n"
    "\n"
    "# Build dev (plus rapide)\n"
    "npm run build\n"
    "\n"
    "# Generer un composant (CLI)\n"
    "npx ng generate component features/admin-dashboard\n"
    "# ou raccourci : ng g c features/admin-dashboard"
))

story.append(Paragraph("13.2 Structure du build production", ST_H1))
story.append(code(
    "dist/chatbot-fsbm/\n"
    "  index.html                 (1 KB)\n"
    "  main-XXXXXXXX.js           (175 KB - bundle initial)\n"
    "  polyfills-XXXXXXXX.js      (90 KB - support vieux navigateurs)\n"
    "  styles-XXXXXXXX.css        (13 KB)\n"
    "  chunk-XXXXXXXX.js          (chunks pages lazy)\n"
    "  assets/                    (images, logos)"
))

story.append(Paragraph("13.3 Deploiement", ST_H1))
story.append(Paragraph(
    "En production, on n'utilise PAS le dev server Angular. On sert les fichiers statiques "
    "avec :",
    ST_BODY))
for x in [
    "<b>nginx</b> (recommande, ultra-rapide)",
    "<b>Apache httpd</b> (plus traditionnel)",
    "<b>Vercel / Netlify</b> (sans serveur, automatique)",
    "<b>Cloud Storage + CDN</b> (S3 + CloudFront, GCP, Azure)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph(
    "Important : il faut configurer le serveur pour <b>fallback sur index.html</b> "
    "(SPA mode). Sinon, refresh sur /chat donnera un 404.",
    ST_BODY))
story.append(code(
    "# Exemple nginx\n"
    "location / {\n"
    "    try_files $uri $uri/ /index.html;\n"
    "}"
))

story.append(Paragraph("13.4 Conclusion", ST_H1))
story.append(Paragraph(
    "Tu maitrises maintenant le frontend Angular du projet. Pour aller plus loin :",
    ST_BODY))
for x in [
    "PDF 03 - pour comprendre le backend qui repond aux appels HTTP",
    "PDF 07 - pour la communication frontend/backend en detail",
    "PDF 09 - pour le workflow complet click -> rendu final",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

build_doc("02_Frontend_Angular_Complet.pdf", story,
          "PDF 02 - Frontend Angular",
          "FSBM Platform - Frontend Angular Complet")
