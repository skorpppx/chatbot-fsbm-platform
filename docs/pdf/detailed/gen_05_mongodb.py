"""PDF 5 - MongoDB + NoSQL Complet"""
from pdf_utils import *
from reportlab.platypus import Spacer, PageBreak

story = []
cover_page(story, "PDF 05/10", "MongoDB + NoSQL",
           "Base documentaire flexible + 6 collections + Motor async",
           accent_color=HexColor('#4DB33D'))

# TOC
story.append(Paragraph("Sommaire", ST_CHAPTER))
for label, page in [
    ("Chapitre 1 - C'est quoi NoSQL ?", "3"),
    ("Chapitre 2 - SQL vs NoSQL", "6"),
    ("Chapitre 3 - C'est quoi MongoDB ?", "9"),
    ("Chapitre 4 - Documents BSON", "12"),
    ("Chapitre 5 - Les 6 collections de fsbm_reviews", "15"),
    ("Chapitre 6 - JSON Schema validation", "20"),
    ("Chapitre 7 - Index dans MongoDB", "23"),
    ("Chapitre 8 - Requetes MongoDB", "25"),
    ("Chapitre 9 - Motor (driver async Python)", "29"),
    ("Chapitre 10 - Quand utiliser MongoDB vs MySQL", "32"),
    ("Chapitre 11 - Conclusion", "35"),
]:
    story.append(toc_entry(label, page))
story.append(PageBreak())

# CH 1
story.append(Paragraph("Chapitre 1 - C'est quoi NoSQL ?", ST_CHAPTER))

story.append(Paragraph("1.1 Definition", ST_H1))
story.append(Paragraph(
    "<b>NoSQL</b> signifie <b>'Not Only SQL'</b> (pas seulement SQL). C'est une famille de "
    "bases de donnees qui ne suivent <b>pas le modele relationnel</b> tabulaire.",
    ST_BODY))

story.append(analogy(
    "SQL = un <b>classeur Excel</b> avec lignes/colonnes rigides. NoSQL = un <b>tiroir</b> "
    "ou tu mets des dossiers de toutes les formes. Chaque dossier (document) peut avoir une "
    "structure differente."))

story.append(Paragraph("1.2 Les 4 categories de NoSQL", ST_H1))
story.append(std_table([
    ['Type', 'Exemples', 'Use case'],
    ['Documentaire', 'MongoDB, CouchDB', 'Reviews, logs, content'],
    ['Cle-valeur', 'Redis, DynamoDB', 'Cache, sessions'],
    ['Colonnes', 'Cassandra, HBase', 'Analytics big data'],
    ['Graphes', 'Neo4j, ArangoDB', 'Reseaux sociaux'],
], col_widths=[3*cm, 4*cm, 9*cm]))

story.append(Paragraph(
    "Notre projet utilise <b>MongoDB</b> (documentaire). C'est le NoSQL le plus populaire.",
    ST_BODY))

story.append(Paragraph("1.3 Histoire", ST_H1))
story.append(Paragraph(
    "Le terme 'NoSQL' a explose en 2009 quand Google, Amazon, Facebook avaient besoin de "
    "gerer des volumes massifs de donnees flexibles que les SGBD relationnels classiques "
    "geraient mal. MongoDB est sorti en 2009 par 10gen (devenu MongoDB Inc.).",
    ST_BODY))

story.append(Paragraph("1.4 Pourquoi NoSQL ?", ST_H1))
for x in [
    "<b>Schema flexible</b> : pas besoin de migrer pour ajouter un champ",
    "<b>Scaling horizontal</b> : facile de repartir sur plusieurs serveurs (sharding)",
    "<b>Performance</b> sur de gros volumes (millions de docs)",
    "<b>JSON natif</b> : pas besoin de mapper objet <-> table",
    "<b>Developpement rapide</b> : ideal pour MVP et prototypes",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))
story.append(PageBreak())

# CH 2 - SQL vs NoSQL
story.append(Paragraph("Chapitre 2 - SQL vs NoSQL", ST_CHAPTER))

story.append(Paragraph("2.1 Comparaison detaillee", ST_H1))
story.append(std_table([
    ['Critere', 'SQL (MySQL)', 'NoSQL (MongoDB)'],
    ['Modele', 'Tables avec lignes', 'Collections de documents'],
    ['Schema', 'Fixe et strict', 'Flexible (peut etre valide)'],
    ['Relations', 'JOINs natifs', 'Embedding ou references'],
    ['Transactions', 'ACID complet', 'ACID depuis v4'],
    ['Langage', 'SQL standardise', 'API JavaScript-like'],
    ['Scaling', 'Vertical (gros serveur)', 'Horizontal (cluster)'],
    ['Apprentissage', 'Plus connu', 'Plus recent'],
    ['Cas ideal', 'Donnees structurees liees', 'Donnees variables, gros volume'],
    ['Exemples', 'Banque, ERP, comptabilite', 'CMS, logs, reviews, IoT'],
    ['Dans FSBM', 'Etudiants, profs, notes', 'Reviews, logs, sentiments'],
], col_widths=[3.5*cm, 6*cm, 6.5*cm]))

story.append(Paragraph("2.2 Quand choisir l'un ou l'autre ?", ST_H1))
story.append(Paragraph("Choisis SQL si :", ST_H2))
for x in [
    "Tes donnees sont fortement liees (relations N:N complexes)",
    "Tu as besoin de transactions ACID strictes (banque, comptabilite)",
    "Ton schema est stable et bien defini",
    "Tu utilises beaucoup de JOINs et d'aggregations",
    "Ton volume est petit a moyen (< 100M lignes)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(Paragraph("Choisis NoSQL si :", ST_H2))
for x in [
    "Tes donnees sont variables / evolutives",
    "Tu as enormement de donnees (terabytes)",
    "Tu fais surtout des lookups simples (par cle)",
    "Tu prefiers une structure hierarchique JSON",
    "Tu veux scaler horizontalement facilement",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

story.append(alert_box(
    "Dans notre PFE, on utilise <b>les DEUX</b>. C'est ce qu'on appelle <b>'polyglot "
    "persistence'</b>. Chaque type de donnees va dans la base qui lui convient. "
    "MySQL pour les donnees academiques structurees, MongoDB pour les feedbacks flexibles.",
    kind="tip"))
story.append(PageBreak())

# CH 3 - MongoDB
story.append(Paragraph("Chapitre 3 - C'est quoi MongoDB ?", ST_CHAPTER))

story.append(Paragraph("3.1 MongoDB en bref", ST_H1))
story.append(Paragraph(
    "<b>MongoDB</b> est le SGBD documentaire le plus populaire au monde. Il stocke des "
    "<b>documents JSON-like</b> dans des <b>collections</b>.",
    ST_BODY))

story.append(Paragraph("3.2 Vocabulaire", ST_H1))
story.append(std_table([
    ['SQL', 'MongoDB'],
    ['Database', 'Database'],
    ['Table', 'Collection'],
    ['Row', 'Document'],
    ['Column', 'Field'],
    ['Primary Key', '_id (ObjectId auto)'],
    ['JOIN', '$lookup (rarement utilise)'],
    ['SQL query', 'Query API (JSON)'],
], col_widths=[6*cm, 10*cm]))

story.append(Paragraph("3.3 Exemple de document", ST_H1))
story.append(code(
    "// Une review dans la collection 'reviews'\n"
    "{\n"
    "    \"_id\": ObjectId(\"6553...\"),\n"
    "    \"user_id\": 12345,\n"
    "    \"username\": \"Yassine B.\",\n"
    "    \"rating\": 5,\n"
    "    \"title\": \"Tres utile pour les questions de scolarite !\",\n"
    "    \"content\": \"Le chatbot m'a beaucoup aide...\",\n"
    "    \"category\": \"CHATBOT\",\n"
    "    \"sentiment\": \"POSITIVE\",\n"
    "    \"sentiment_score\": 0.92,\n"
    "    \"tags\": [\"scolarite\", \"rapide\", \"clair\"],\n"
    "    \"is_verified\": true,\n"
    "    \"helpful_count\": 23,\n"
    "    \"created_at\": ISODate(\"2026-04-15T10:30:00Z\")\n"
    "}"
))

story.append(Paragraph(
    "Note les types varies : nombres, strings, booleens, tableaux, dates, sous-documents. "
    "Tout en un seul document.",
    ST_BODY))

story.append(Paragraph("3.4 Outils MongoDB", ST_H1))
for x in [
    "<b>mongosh</b> - shell ligne de commande (comme mysql CLI)",
    "<b>MongoDB Compass</b> - GUI desktop officielle",
    "<b>Studio 3T</b> - GUI avancee (payante)",
    "<b>MongoDB Atlas</b> - service cloud manage (free tier 512MB)",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))
story.append(PageBreak())

# CH 4 - BSON
story.append(Paragraph("Chapitre 4 - Documents BSON", ST_CHAPTER))

story.append(Paragraph("4.1 JSON vs BSON", ST_H1))
story.append(Paragraph(
    "MongoDB ne stocke pas du JSON pur, mais du <b>BSON = Binary JSON</b>. C'est un format "
    "binaire compact qui supporte plus de types que JSON :",
    ST_BODY))
story.append(std_table([
    ['Type BSON', 'JSON equivalent', 'Note'],
    ['String', 'String', 'UTF-8'],
    ['Int32 / Int64', 'Number', 'Distinction int/float'],
    ['Double', 'Number', 'Floats'],
    ['Boolean', 'Boolean', 'true/false'],
    ['Date', 'String ISO', 'Stocke en ms epoch'],
    ['ObjectId', '-', 'ID unique 12 bytes'],
    ['Array', 'Array', 'Liste hetero'],
    ['Object', 'Object', 'Sous-document'],
    ['Binary', '-', 'Donnees binaires'],
    ['Null', 'null', 'Absence'],
], col_widths=[3*cm, 3*cm, 10*cm]))

story.append(Paragraph("4.2 _id et ObjectId", ST_H1))
story.append(Paragraph(
    "Chaque document a un champ <code>_id</code> unique (genere automatiquement). C'est un "
    "<b>ObjectId</b> de 12 bytes contenant : timestamp + machine + counter.",
    ST_BODY))
story.append(code(
    "// Exemple : ObjectId(\"655398754d6e2f3c1a0b8c92\")\n"
    "// |--------||----||----||----------|\n"
    "// timestamp machine pid  counter\n"
    "\n"
    "// Tu peux le forcer :\n"
    "db.users.insertOne({ _id: \"karim_alaoui\", name: \"Karim\" });\n"
    "\n"
    "// Sinon MongoDB en genere un :\n"
    "db.users.insertOne({ name: \"Fatima\" });\n"
    "// -> _id: ObjectId(\"...\") auto"
))

story.append(Paragraph("4.3 Embedding vs References", ST_H1))
story.append(Paragraph(
    "Pour modeliser des relations, MongoDB offre 2 strategies :",
    ST_BODY))

story.append(Paragraph("Embedding (imbriquer)", ST_H2))
story.append(code(
    "{\n"
    "  \"_id\": ...,\n"
    "  \"title\": \"Avis sur le chatbot\",\n"
    "  \"author\": {\n"
    "    \"name\": \"Karim\",\n"
    "    \"email\": \"karim@etu.fsbm.ma\"\n"
    "  },\n"
    "  \"comments\": [\n"
    "    { \"user\": \"Salma\", \"text\": \"D'accord !\" },\n"
    "    { \"user\": \"Hamza\", \"text\": \"Aussi mon avis.\" }\n"
    "  ]\n"
    "}"
))
story.append(Paragraph("References (separation)", ST_H2))
story.append(code(
    "// Collection 'reviews'\n"
    "{ \"_id\": ObjectId(\"a1\"), \"title\": \"...\", \"author_id\": ObjectId(\"u1\") }\n"
    "\n"
    "// Collection 'users' separee\n"
    "{ \"_id\": ObjectId(\"u1\"), \"name\": \"Karim\", \"email\": \"...\" }"
))

story.append(alert_box(
    "<b>Regle :</b> embed si on lit toujours ensemble, refer si volumes gros ou modifs "
    "frequentes. Pour notre FSBM : commentaires <b>embed</b> dans reviews (toujours lus "
    "ensemble), user_id <b>refer</b> (utilisateur evolue independamment).",
    kind="tip"))
story.append(PageBreak())

# CH 5 - 6 collections
story.append(Paragraph("Chapitre 5 - Les 6 collections de fsbm_reviews", ST_CHAPTER))

collections_detail = [
    ("1. reviews",
     "Avis textuels detaillés des utilisateurs sur le chatbot ou la plateforme. "
     "Champs : user_id, rating (1-5), title, content, category, sentiment, tags, "
     "helpful_count, created_at."),
    ("2. chatbot_feedback",
     "Feedback rapide (pouce haut/bas) lié a une conversation chatbot specifique. "
     "Champs : conversation_id, session_id, message_text, bot_response, "
     "intent_detected, confidence, is_helpful, comment."),
    ("3. conversations",
     "Log complet d'une session de conversation chatbot. Embeddes : array de messages "
     "(role, text, timestamp, intent, confidence). Plus metadata : duration, device_type."),
    ("4. sentiment_analysis",
     "Resultats d'analyse de sentiment (NLP). source_type (REVIEW/FEEDBACK/MESSAGE), "
     "score (-1 a 1), emotions (joy, anger, sadness, surprise, fear), language."),
    ("5. usage_logs",
     "Tracking anonyme : page_view, chat_start, message_sent, search, login, "
     "feedback. event_type + session_id + duration_ms + timestamp."),
    ("6. suggestions",
     "Suggestions d'amelioration soumises par les utilisateurs. title, description, "
     "category, status (OUVERT/EN_COURS/ETUDE/FAIT), votes, author."),
]
for n, d in collections_detail:
    story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

story.append(Paragraph("5.1 Structure complete : reviews", ST_H1))
story.append(code(
    "{\n"
    "  _id: ObjectId(\"...\"),\n"
    "  user_id: 12345,\n"
    "  username: \"Yassine B.\",\n"
    "  rating: 5,                   // int 1-5\n"
    "  title: \"Tres utile !\",\n"
    "  content: \"Le chatbot...\",   // max 2000 chars\n"
    "  category: \"CHATBOT\",        // enum : CHATBOT|INTERFACE|PERFORMANCE|CONTENT|AUTRE\n"
    "  sentiment: \"POSITIVE\",      // enum : POSITIVE|NEUTRAL|NEGATIVE\n"
    "  sentiment_score: 0.92,       // float\n"
    "  tags: [\"scolarite\", \"rapide\"],\n"
    "  is_verified: true,\n"
    "  helpful_count: 23,\n"
    "  created_at: ISODate(\"2026-04-15T10:30:00Z\"),\n"
    "  updated_at: ISODate(\"2026-04-15T10:30:00Z\")\n"
    "}"
))
story.append(PageBreak())

# CH 6 - Validation
story.append(Paragraph("Chapitre 6 - JSON Schema validation", ST_CHAPTER))

story.append(Paragraph("6.1 Le risque de la flexibilite", ST_H1))
story.append(Paragraph(
    "MongoDB est <b>trop flexible</b> par defaut. Sans validation, on peut inserer n'importe "
    "quoi (un rating string au lieu de int, un email mal formate, etc.).",
    ST_BODY))

story.append(Paragraph("6.2 Solution : JSON Schema validator", ST_H1))
story.append(code(
    "db.createCollection(\"reviews\", {\n"
    "    validator: {\n"
    "        $jsonSchema: {\n"
    "            bsonType: \"object\",\n"
    "            required: [\"user_id\", \"rating\", \"created_at\"],\n"
    "            properties: {\n"
    "                user_id: { bsonType: [\"int\", \"long\", \"string\"] },\n"
    "                username: { bsonType: \"string\" },\n"
    "                rating: { bsonType: \"int\", minimum: 1, maximum: 5 },\n"
    "                title: { bsonType: \"string\", maxLength: 200 },\n"
    "                content: { bsonType: \"string\", maxLength: 2000 },\n"
    "                category: {\n"
    "                    enum: [\"CHATBOT\", \"INTERFACE\", \"PERFORMANCE\", \"CONTENT\", \"AUTRE\"]\n"
    "                },\n"
    "                sentiment: {\n"
    "                    enum: [\"POSITIVE\", \"NEUTRAL\", \"NEGATIVE\"]\n"
    "                },\n"
    "                sentiment_score: { bsonType: \"double\" },\n"
    "                tags: { bsonType: \"array\", items: { bsonType: \"string\" } },\n"
    "                is_verified: { bsonType: \"bool\" },\n"
    "                helpful_count: { bsonType: \"int\" },\n"
    "                created_at: { bsonType: \"date\" }\n"
    "            }\n"
    "        }\n"
    "    }\n"
    "});"
))

story.append(Paragraph(
    "Si on tente d'inserer un document qui ne respecte pas le schema, MongoDB rejette :",
    ST_BODY))
story.append(code(
    "db.reviews.insertOne({\n"
    "  user_id: 1,\n"
    "  rating: \"5\",     // ERREUR : devrait etre int\n"
    "  created_at: new Date()\n"
    "});\n"
    "// Document failed validation"
))
story.append(PageBreak())

# CH 7 - Index
story.append(Paragraph("Chapitre 7 - Index dans MongoDB", ST_CHAPTER))

story.append(Paragraph("7.1 Creation d'index", ST_H1))
story.append(code(
    "// Index simple\n"
    "db.reviews.createIndex({ user_id: 1 });   // 1 = ascendant, -1 = descendant\n"
    "\n"
    "// Index compose\n"
    "db.reviews.createIndex({ rating: 1, created_at: -1 });\n"
    "\n"
    "// Index unique\n"
    "db.users.createIndex({ email: 1 }, { unique: true });\n"
    "\n"
    "// Index TEXT (recherche full-text)\n"
    "db.reviews.createIndex({ content: \"text\", title: \"text\" });\n"
    "\n"
    "// Liste des index\n"
    "db.reviews.getIndexes();"
))

story.append(Paragraph("7.2 Index dans notre projet", ST_H1))
story.append(code(
    "// Collection reviews\n"
    "db.reviews.createIndex({ user_id: 1 });\n"
    "db.reviews.createIndex({ rating: 1, created_at: -1 });\n"
    "db.reviews.createIndex({ category: 1 });\n"
    "db.reviews.createIndex({ sentiment: 1 });\n"
    "db.reviews.createIndex({ content: \"text\", title: \"text\" });\n"
    "\n"
    "// Collection chatbot_feedback\n"
    "db.chatbot_feedback.createIndex({ conversation_id: 1 });\n"
    "db.chatbot_feedback.createIndex({ session_id: 1 });\n"
    "db.chatbot_feedback.createIndex({ is_helpful: 1, created_at: -1 });"
))
story.append(PageBreak())

# CH 8 - Requetes
story.append(Paragraph("Chapitre 8 - Requetes MongoDB", ST_CHAPTER))

story.append(Paragraph("8.1 find()", ST_H1))
story.append(code(
    "// Tout\n"
    "db.reviews.find();\n"
    "\n"
    "// Avec filtre\n"
    "db.reviews.find({ rating: 5 });\n"
    "\n"
    "// Operateurs : $gt, $lt, $gte, $lte\n"
    "db.reviews.find({ rating: { $gte: 4 } });\n"
    "\n"
    "// AND implicite\n"
    "db.reviews.find({ rating: 5, sentiment: \"POSITIVE\" });\n"
    "\n"
    "// OR\n"
    "db.reviews.find({\n"
    "  $or: [\n"
    "    { rating: 5 },\n"
    "    { sentiment: \"POSITIVE\" }\n"
    "  ]\n"
    "});\n"
    "\n"
    "// IN\n"
    "db.reviews.find({ category: { $in: [\"CHATBOT\", \"INTERFACE\"] } });\n"
    "\n"
    "// Regex (recherche partielle)\n"
    "db.reviews.find({ title: { $regex: /utile/i } });\n"
    "\n"
    "// Tri + limite\n"
    "db.reviews.find()\n"
    "  .sort({ created_at: -1 })\n"
    "  .limit(10);\n"
    "\n"
    "// Projection (selection de champs)\n"
    "db.reviews.find({}, { title: 1, rating: 1, _id: 0 });"
))

story.append(Paragraph("8.2 insertOne / insertMany", ST_H1))
story.append(code(
    "db.reviews.insertOne({\n"
    "  user_id: 1,\n"
    "  rating: 5,\n"
    "  title: \"Super !\",\n"
    "  created_at: new Date()\n"
    "});\n"
    "\n"
    "db.reviews.insertMany([\n"
    "  { user_id: 2, rating: 4, ... },\n"
    "  { user_id: 3, rating: 5, ... }\n"
    "]);"
))

story.append(Paragraph("8.3 updateOne / updateMany", ST_H1))
story.append(code(
    "// Modifier un document\n"
    "db.reviews.updateOne(\n"
    "  { _id: ObjectId(\"...\") },\n"
    "  { $set: { rating: 4, sentiment: \"NEUTRAL\" } }\n"
    ");\n"
    "\n"
    "// Incrementer\n"
    "db.reviews.updateOne(\n"
    "  { _id: ObjectId(\"...\") },\n"
    "  { $inc: { helpful_count: 1 } }\n"
    ");\n"
    "\n"
    "// Ajouter a un array\n"
    "db.reviews.updateOne(\n"
    "  { _id: ObjectId(\"...\") },\n"
    "  { $push: { tags: \"recommande\" } }\n"
    ");"
))

story.append(Paragraph("8.4 Aggregation Pipeline", ST_H1))
story.append(Paragraph(
    "Pour des requetes complexes (group by, joins, calculs) :",
    ST_BODY))
story.append(code(
    "// Compter les reviews par categorie\n"
    "db.reviews.aggregate([\n"
    "  { $group: {\n"
    "      _id: \"$category\",\n"
    "      count: { $sum: 1 },\n"
    "      avg_rating: { $avg: \"$rating\" }\n"
    "  }},\n"
    "  { $sort: { count: -1 } }\n"
    "]);\n"
    "\n"
    "// Resultat :\n"
    "// [\n"
    "//   { _id: \"CHATBOT\", count: 42, avg_rating: 4.5 },\n"
    "//   { _id: \"INTERFACE\", count: 18, avg_rating: 4.8 },\n"
    "// ]"
))
story.append(PageBreak())

# CH 9 - Motor
story.append(Paragraph("Chapitre 9 - Motor (driver async Python)", ST_CHAPTER))

story.append(Paragraph("9.1 Pourquoi Motor ?", ST_H1))
story.append(Paragraph(
    "Le driver officiel <b>pymongo</b> est synchrone. Pour FastAPI async, on utilise "
    "<b>Motor</b> (driver async officiel MongoDB).",
    ST_BODY))

story.append(Paragraph("9.2 Installation et setup", ST_H1))
story.append(code(
    "pip install motor\n"
    "\n"
    "# review_service/app/db.py\n"
    "from motor.motor_asyncio import AsyncIOMotorClient\n"
    "\n"
    "MONGO_URL = \"mongodb://localhost:27017\"\n"
    "client = AsyncIOMotorClient(MONGO_URL)\n"
    "db = client.fsbm_reviews\n"
    "\n"
    "# Acces aux collections\n"
    "reviews_col = db.reviews\n"
    "feedback_col = db.chatbot_feedback"
))

story.append(Paragraph("9.3 CRUD asynchrone avec Motor", ST_H1))
story.append(code(
    "# INSERT\n"
    "result = await reviews_col.insert_one({\n"
    "    \"user_id\": 1,\n"
    "    \"rating\": 5,\n"
    "    \"title\": \"Super !\",\n"
    "    \"created_at\": datetime.utcnow()\n"
    "})\n"
    "print(result.inserted_id)\n"
    "\n"
    "# FIND ONE\n"
    "review = await reviews_col.find_one({\"_id\": ObjectId(\"...\")})\n"
    "\n"
    "# FIND MANY (cursor async)\n"
    "cursor = reviews_col.find({\"rating\": {\"$gte\": 4}}).sort(\"created_at\", -1).limit(10)\n"
    "reviews = await cursor.to_list(length=10)\n"
    "\n"
    "# UPDATE\n"
    "await reviews_col.update_one(\n"
    "    {\"_id\": ObjectId(\"...\")},\n"
    "    {\"$inc\": {\"helpful_count\": 1}}\n"
    ")\n"
    "\n"
    "# DELETE\n"
    "await reviews_col.delete_one({\"_id\": ObjectId(\"...\")})"
))

story.append(Paragraph("9.4 Integration FastAPI", ST_H1))
story.append(code(
    "@router.post(\"/api/reviews\")\n"
    "async def create_review(review: ReviewCreate):\n"
    "    doc = review.model_dump()\n"
    "    doc[\"created_at\"] = datetime.utcnow()\n"
    "    result = await reviews_col.insert_one(doc)\n"
    "    return {\"id\": str(result.inserted_id)}\n"
    "\n"
    "@router.get(\"/api/reviews\")\n"
    "async def list_reviews(limit: int = 20):\n"
    "    cursor = reviews_col.find().sort(\"created_at\", -1).limit(limit)\n"
    "    reviews = await cursor.to_list(length=limit)\n"
    "    # Conversion ObjectId -> str pour JSON\n"
    "    for r in reviews:\n"
    "        r[\"_id\"] = str(r[\"_id\"])\n"
    "    return reviews"
))
story.append(PageBreak())

# CH 10
story.append(Paragraph("Chapitre 10 - Quand utiliser MongoDB vs MySQL", ST_CHAPTER))

story.append(Paragraph("10.1 Repartition dans notre projet", ST_H1))
story.append(std_table([
    ['Type de donnees', 'BDD choisie', 'Justification'],
    ['Etudiants (CNE, nom, filiere)', 'MySQL', 'Schema fixe, relations strictes'],
    ['Filieres + departements', 'MySQL', 'Relations N:N, integrite'],
    ['Notes etudiants', 'MySQL', 'Calculs, transactions'],
    ['Modules + emploi du temps', 'MySQL', 'Relations complexes'],
    ['Reviews textuelles', 'MongoDB', 'Schema variable, full-text search'],
    ['Sentiment analyses', 'MongoDB', 'Structure JSON imbriquee'],
    ['Logs d\'usage', 'MongoDB', 'Volume massif, ecritures'],
    ['Suggestions ameliorations', 'MongoDB', 'Champs evoluent souvent'],
    ['Conversations chatbot', 'MySQL+Mongo', 'MySQL pour historique strict, Mongo pour logs riches'],
], col_widths=[5*cm, 3*cm, 8*cm]))

story.append(Paragraph("10.2 Erreurs classiques", ST_H1))
story.append(Paragraph("Erreur 1 : tout en MongoDB pour 'simplifier'", ST_H2))
story.append(Paragraph(
    "Tu perds l'integrite referentielle, les transactions ACID, les JOINs efficaces. Pour "
    "gerer un cursus academique avec notes/modules/profs lies, MySQL est BIEN MEILLEUR.",
    ST_BODY))

story.append(Paragraph("Erreur 2 : tout en SQL et stocker du JSON dans BLOBs", ST_H2))
story.append(Paragraph(
    "Pour des reviews flexibles, c'est faisable en MySQL (champ JSON) mais bien moins "
    "performant pour les recherches. MongoDB est natif pour ce cas.",
    ST_BODY))

story.append(Paragraph("10.3 Bilan pour le jury", ST_H1))
story.append(alert_box(
    "<b>Polyglot persistence</b> = utiliser plusieurs BDD selon le type de donnees. "
    "C'est une pratique <b>industrielle</b> (Amazon, Netflix, Spotify). Demontrer qu'on la "
    "maitrise est un grand plus en soutenance.",
    kind="key"))
story.append(PageBreak())

# CH 11 - Conclusion
story.append(Paragraph("Chapitre 11 - Conclusion", ST_CHAPTER))

story.append(Paragraph("11.1 Recap des concepts", ST_H1))
for x in [
    "NoSQL = 'Not Only SQL' = familles non-relationnelles",
    "4 categories : Documentaire (MongoDB), Cle-valeur (Redis), Colonnes (Cassandra), Graphes (Neo4j)",
    "MongoDB = documentaire, JSON-like, schema flexible",
    "BSON = JSON binaire avec plus de types",
    "Collections = tables, Documents = rows",
    "_id ObjectId = cle primaire auto",
    "Embedding vs References pour modeliser",
    "JSON Schema validator pour contraintes",
    "Motor = driver async Python pour FastAPI",
    "Polyglot persistence = MySQL + MongoDB ensemble",
]:
    story.append(Paragraph(f"+ {x}", ST_LIST))

story.append(Paragraph("11.2 Pour aller plus loin", ST_H1))
for x in [
    "PDF 04 - pour bien comprendre MySQL et SQLAlchemy",
    "PDF 06 - pour le NLP et l'IA (utilise MongoDB pour logs en Phase 2)",
    "PDF 08 - pour la securite MongoDB",
]:
    story.append(Paragraph(f"• {x}", ST_LIST))

build_doc("05_MongoDB_NoSQL_Complet.pdf", story,
          "PDF 05 - MongoDB + NoSQL",
          "FSBM Platform - MongoDB et NoSQL Complet")
