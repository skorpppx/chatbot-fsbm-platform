// =============================================================================
//  FSBM Platform — MongoDB Initialisation
//  Création de la base fsbm_reviews et des collections + indexes
//
//  Exécution :
//      mongosh < init.js
//  ou via mongosh interactif :
//      load("init.js")
// =============================================================================

print("[FSBM-MongoDB] Initialisation de la base fsbm_reviews...");

use("fsbm_reviews");

// =============================================================================
//  Collection: reviews
//  Avis détaillés des étudiants sur le chatbot / l'application
// =============================================================================
db.createCollection("reviews", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["user_id", "rating", "created_at"],
            properties: {
                user_id:      { bsonType: ["int", "long", "string"] },
                username:     { bsonType: "string" },
                rating:       { bsonType: "int", minimum: 1, maximum: 5 },
                title:        { bsonType: "string", maxLength: 200 },
                content:      { bsonType: "string", maxLength: 2000 },
                category:     { enum: ["CHATBOT", "INTERFACE", "PERFORMANCE", "CONTENT", "AUTRE"] },
                sentiment:    { enum: ["POSITIVE", "NEUTRAL", "NEGATIVE"] },
                sentiment_score: { bsonType: "double" },
                tags:         { bsonType: "array", items: { bsonType: "string" } },
                is_verified:  { bsonType: "bool" },
                helpful_count:{ bsonType: "int" },
                created_at:   { bsonType: "date" },
                updated_at:   { bsonType: "date" }
            }
        }
    }
});
db.reviews.createIndex({ user_id: 1 });
db.reviews.createIndex({ rating: 1, created_at: -1 });
db.reviews.createIndex({ category: 1 });
db.reviews.createIndex({ sentiment: 1 });
db.reviews.createIndex({ content: "text", title: "text" });

// =============================================================================
//  Collection: chatbot_feedback
//  Feedback rapide (pouce haut/bas) sur une réponse précise
// =============================================================================
db.createCollection("chatbot_feedback", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["conversation_id", "is_helpful", "created_at"],
            properties: {
                conversation_id: { bsonType: ["int", "long"] },
                session_id:      { bsonType: "string" },
                user_id:         { bsonType: ["int", "long", "null"] },
                message_text:    { bsonType: "string" },
                bot_response:    { bsonType: "string" },
                intent_detected: { bsonType: "string" },
                confidence:      { bsonType: "double" },
                is_helpful:      { bsonType: "bool" },
                comment:         { bsonType: "string", maxLength: 500 },
                created_at:      { bsonType: "date" }
            }
        }
    }
});
db.chatbot_feedback.createIndex({ conversation_id: 1 });
db.chatbot_feedback.createIndex({ session_id: 1 });
db.chatbot_feedback.createIndex({ is_helpful: 1, created_at: -1 });
db.chatbot_feedback.createIndex({ intent_detected: 1 });

// =============================================================================
//  Collection: conversations
//  Log complet d'une session de conversation (échanges multiples)
// =============================================================================
db.createCollection("conversations", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["session_id", "started_at"],
            properties: {
                session_id:    { bsonType: "string" },
                user_id:       { bsonType: ["int", "long", "null"] },
                started_at:    { bsonType: "date" },
                ended_at:      { bsonType: ["date", "null"] },
                duration_sec:  { bsonType: "int" },
                messages: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        properties: {
                            sender:     { enum: ["user", "bot"] },
                            text:       { bsonType: "string" },
                            timestamp:  { bsonType: "date" },
                            intent:     { bsonType: "string" },
                            confidence: { bsonType: "double" }
                        }
                    }
                },
                topic_summary: { bsonType: "string" },
                resolved:      { bsonType: "bool" },
                handed_off:    { bsonType: "bool" },
                metadata: {
                    bsonType: "object",
                    properties: {
                        user_agent:  { bsonType: "string" },
                        ip_country:  { bsonType: "string" },
                        device_type: { enum: ["DESKTOP", "MOBILE", "TABLET"] }
                    }
                }
            }
        }
    }
});
db.conversations.createIndex({ session_id: 1 }, { unique: true });
db.conversations.createIndex({ user_id: 1, started_at: -1 });
db.conversations.createIndex({ started_at: -1 });
db.conversations.createIndex({ resolved: 1 });

// =============================================================================
//  Collection: sentiment_analysis
//  Résultats d'analyse de sentiment (snapshot)
// =============================================================================
db.createCollection("sentiment_analysis", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["text", "sentiment", "score", "analyzed_at"],
            properties: {
                source_type:  { enum: ["REVIEW", "FEEDBACK", "MESSAGE", "COMMENT"] },
                source_id:    { bsonType: ["int", "long", "string", "objectId"] },
                text:         { bsonType: "string" },
                sentiment:    { enum: ["POSITIVE", "NEUTRAL", "NEGATIVE"] },
                score:        { bsonType: "double", minimum: -1, maximum: 1 },
                emotions: {
                    bsonType: "object",
                    properties: {
                        joy:      { bsonType: "double" },
                        anger:    { bsonType: "double" },
                        sadness:  { bsonType: "double" },
                        surprise: { bsonType: "double" },
                        fear:     { bsonType: "double" }
                    }
                },
                language:     { bsonType: "string" },
                analyzed_at:  { bsonType: "date" }
            }
        }
    }
});
db.sentiment_analysis.createIndex({ source_type: 1, source_id: 1 });
db.sentiment_analysis.createIndex({ sentiment: 1, analyzed_at: -1 });

// =============================================================================
//  Collection: usage_logs
//  Tracking d'utilisation anonyme (pour analytics-service)
// =============================================================================
db.createCollection("usage_logs", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["event_type", "timestamp"],
            properties: {
                event_type: { enum: ["PAGE_VIEW", "CHAT_START", "MESSAGE_SENT", "FAQ_VIEW",
                                     "SEARCH", "LOGIN", "LOGOUT", "FEEDBACK", "DOWNLOAD"] },
                session_id: { bsonType: "string" },
                user_id:    { bsonType: ["int", "long", "null"] },
                page:       { bsonType: "string" },
                params:     { bsonType: "object" },
                duration_ms:{ bsonType: "int" },
                timestamp:  { bsonType: "date" }
            }
        }
    }
});
db.usage_logs.createIndex({ event_type: 1, timestamp: -1 });
db.usage_logs.createIndex({ session_id: 1 });
db.usage_logs.createIndex({ user_id: 1, timestamp: -1 });
db.usage_logs.createIndex({ timestamp: -1 });

// =============================================================================
//  Collection: suggestions
//  Suggestions d'amélioration soumises par les étudiants
// =============================================================================
db.createCollection("suggestions");
db.suggestions.createIndex({ status: 1, votes: -1 });
db.suggestions.createIndex({ created_at: -1 });

// =============================================================================
//  DONNÉES INITIALES — Reviews réalistes (exemples)
// =============================================================================
db.reviews.insertMany([
    {
        user_id: 12345,
        username: "Yassine B.",
        rating: 5,
        title: "Très utile pour les questions de scolarité !",
        content: "Le chatbot m'a beaucoup aidé à comprendre la procédure de réinscription. Réponses claires et rapides.",
        category: "CHATBOT",
        sentiment: "POSITIVE",
        sentiment_score: 0.92,
        tags: ["scolarité", "rapide", "clair"],
        is_verified: true,
        helpful_count: 23,
        created_at: new Date("2026-04-15T10:30:00Z"),
        updated_at: new Date("2026-04-15T10:30:00Z")
    },
    {
        user_id: 54321,
        username: "Salma A.",
        rating: 4,
        title: "Bonne aide mais à améliorer",
        content: "Très bon pour les FAQ standards. Parfois ne comprend pas les questions complexes sur les masters.",
        category: "CHATBOT",
        sentiment: "POSITIVE",
        sentiment_score: 0.65,
        tags: ["masters", "amélioration"],
        is_verified: true,
        helpful_count: 15,
        created_at: new Date("2026-04-20T14:15:00Z"),
        updated_at: new Date("2026-04-20T14:15:00Z")
    },
    {
        user_id: 11111,
        username: "Mehdi L.",
        rating: 5,
        title: "Interface moderne et agréable",
        content: "Le design est très propre, les animations fluides. On dirait une vraie application professionnelle.",
        category: "INTERFACE",
        sentiment: "POSITIVE",
        sentiment_score: 0.95,
        tags: ["design", "UX", "moderne"],
        is_verified: true,
        helpful_count: 42,
        created_at: new Date("2026-05-01T09:00:00Z"),
        updated_at: new Date("2026-05-01T09:00:00Z")
    },
    {
        user_id: 22222,
        username: "Imane Z.",
        rating: 3,
        title: "Manque de données sur les bourses",
        content: "Quand je demande des infos sur les bourses internationales, le chatbot ne sait pas vraiment répondre.",
        category: "CONTENT",
        sentiment: "NEUTRAL",
        sentiment_score: 0.1,
        tags: ["bourses", "international", "manque"],
        is_verified: true,
        helpful_count: 8,
        created_at: new Date("2026-05-10T11:45:00Z"),
        updated_at: new Date("2026-05-10T11:45:00Z")
    },
    {
        user_id: 33333,
        username: "Othmane F.",
        rating: 5,
        title: "Indispensable pour les nouveaux étudiants",
        content: "En tant que primo-entrant, le chatbot m'a évité de faire la queue à la scolarité. Top !",
        category: "CHATBOT",
        sentiment: "POSITIVE",
        sentiment_score: 0.98,
        tags: ["primo-entrant", "gain de temps"],
        is_verified: true,
        helpful_count: 67,
        created_at: new Date("2026-05-12T16:20:00Z"),
        updated_at: new Date("2026-05-12T16:20:00Z")
    }
]);

// =============================================================================
//  DONNÉES INITIALES — Suggestions
// =============================================================================
db.suggestions.insertMany([
    {
        title: "Ajouter un mode sombre",
        description: "Le mode sombre serait très utile pour étudier le soir.",
        category: "INTERFACE",
        status: "EN_COURS",
        votes: 128,
        author: "Yassine B.",
        created_at: new Date("2026-04-01T10:00:00Z")
    },
    {
        title: "Intégrer l'emploi du temps en temps réel",
        description: "Pouvoir consulter mon emploi du temps directement dans le chatbot.",
        category: "FONCTIONNALITE",
        status: "OUVERT",
        votes: 95,
        author: "Salma A.",
        created_at: new Date("2026-04-10T14:30:00Z")
    },
    {
        title: "Support multilingue (arabe / anglais)",
        description: "Pouvoir interagir avec le chatbot en arabe ou en anglais.",
        category: "LANGUE",
        status: "OUVERT",
        votes: 78,
        author: "Mehdi L.",
        created_at: new Date("2026-04-15T09:15:00Z")
    },
    {
        title: "Application mobile native",
        description: "Une app Android/iOS officielle de la FSBM.",
        category: "PLATEFORME",
        status: "ETUDE",
        votes: 156,
        author: "Imane Z.",
        created_at: new Date("2026-04-20T11:00:00Z")
    }
]);

print("[FSBM-MongoDB] ✅ Initialisation terminée !");
print("[FSBM-MongoDB] Collections créées :");
print("  - reviews          (" + db.reviews.countDocuments() + " documents)");
print("  - chatbot_feedback (" + db.chatbot_feedback.countDocuments() + " documents)");
print("  - conversations    (" + db.conversations.countDocuments() + " documents)");
print("  - sentiment_analysis (" + db.sentiment_analysis.countDocuments() + " documents)");
print("  - usage_logs       (" + db.usage_logs.countDocuments() + " documents)");
print("  - suggestions      (" + db.suggestions.countDocuments() + " documents)");
