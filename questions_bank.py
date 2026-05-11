def get_question_bank():
    """
    Mood-first, open-ended questions that let the user describe what they want.
    Expanded to include highly specific genre intersections for the neural architecture.
    Scale: 0 = not at all, 10 = absolutely yes.
    """
    bank = []

    # ── PURE GENRE DEEP-DIVES ──────────────────────────────────────────────────
    deep_dives = [
        # Action
        ("Do you want non-stop adrenaline and explosive action scenes?", {"Action": 1.0}),
        ("Are you looking for a movie with incredible hand-to-hand martial arts combat?", {"Action": 0.8, "Thriller": 0.2}),
        ("Do you love massive, epic battle sequences?", {"Action": 0.7, "Fantasy": 0.3}),
        
        # Sci-Fi
        ("Are you fascinated by futuristic worlds and advanced technology?", {"Sci-Fi": 1.0}),
        ("Do you want a mind-bending story about time travel or alternate realities?", {"Sci-Fi": 0.8, "Thriller": 0.2}),
        ("Are you in the mood for an epic space opera exploring the galaxy?", {"Sci-Fi": 0.8, "Action": 0.2}),
        
        # Drama
        ("Are you looking for a deeply moving story that might make you cry?", {"Drama": 1.0}),
        ("Do you want a grounded, realistic story about everyday human struggles?", {"Drama": 0.9, "Romance": 0.1}),
        ("Are you in the mood for an inspiring biographical story based on real events?", {"Drama": 0.8, "History": 0.2}),
        
        # Comedy
        ("Do you want something completely absurd and laugh-out-loud funny?", {"Comedy": 1.0}),
        ("Are you looking for witty dialogue and clever, fast-paced humor?", {"Comedy": 0.8, "Drama": 0.2}),
        ("Do you want a feel-good, lighthearted movie to boost your mood?", {"Comedy": 0.7, "Romance": 0.3}),
        
        # Horror
        ("Do you want a movie that relies on pure psychological dread and tension?", {"Horror": 0.7, "Thriller": 0.3}),
        ("Are you looking for jump scares and terrifying monsters?", {"Horror": 1.0}),
        ("Do you enjoy dark, supernatural stories involving ghosts or demons?", {"Horror": 0.8, "Fantasy": 0.2}),
        
        # Thriller
        ("Do you want a movie with a massive plot twist that you won't see coming?", {"Thriller": 1.0}),
        ("Are you in the mood for a slow-burn mystery where you have to piece the clues together?", {"Thriller": 0.8, "Drama": 0.2}),
        ("Do you want a tense, edge-of-your-seat cat-and-mouse chase?", {"Thriller": 0.7, "Action": 0.3}),
        
        # Romance
        ("Are you looking for a sweeping, epic love story?", {"Romance": 1.0, "Drama": 0.2}),
        ("Do you want a cute, awkward, and funny romantic comedy?", {"Romance": 0.6, "Comedy": 0.4}),
        ("Are you in the mood for a tragic, star-crossed romance?", {"Romance": 0.7, "Drama": 0.5}),
        
        # Fantasy
        ("Do you want to escape into a magical world with its own rules and mythology?", {"Fantasy": 1.0}),
        ("Are you looking for a grand quest involving mythical creatures and heroes?", {"Fantasy": 0.8, "Action": 0.2}),
        ("Do you enjoy dark, gritty fantasy stories?", {"Fantasy": 0.6, "Horror": 0.2, "Drama": 0.2}),
    ]

    # ── HYBRID GENRE SCENARIOS (For adaptive fine-tuning) ─────────────────────
    hybrid_scenarios = [
        # Sci-Fi + Horror
        ("Are you in the mood for something terrifying set in outer space or the future?", {"Sci-Fi": 0.6, "Horror": 0.6}),
        ("Do you like movies where artificial intelligence goes dangerously wrong?", {"Sci-Fi": 0.7, "Thriller": 0.4, "Horror": 0.2}),
        
        # Action + Comedy
        ("Do you want a buddy-cop style movie with lots of action and banter?", {"Action": 0.6, "Comedy": 0.6}),
        ("Are you looking for an action movie that doesn't take itself too seriously?", {"Action": 0.5, "Comedy": 0.7}),
        
        # Rom-Com
        ("Do you want to watch two people fall in love while constantly bickering and making you laugh?", {"Romance": 0.6, "Comedy": 0.6}),
        
        # Thriller + Horror
        ("Do you want a gritty crime story about hunting a terrifying serial killer?", {"Thriller": 0.7, "Horror": 0.4}),
        ("Are you looking for a survival story where the characters are trapped?", {"Thriller": 0.6, "Horror": 0.5, "Action": 0.2}),
        
        # Drama + Thriller
        ("Do you enjoy tense courtroom dramas or intense political thrillers?", {"Drama": 0.6, "Thriller": 0.6}),
        ("Are you in the mood for a dark family drama with a hidden secret?", {"Drama": 0.7, "Thriller": 0.5}),
        
        # Fantasy + Romance
        ("Do you like love stories involving vampires, werewolves, or magic?", {"Fantasy": 0.6, "Romance": 0.6}),
        ("Are you looking for a fairy tale romance?", {"Fantasy": 0.5, "Romance": 0.7, "Comedy": 0.2}),
        
        # Sci-Fi + Action
        ("Do you want massive futuristic battles with lasers and spaceships?", {"Sci-Fi": 0.6, "Action": 0.7}),
        ("Are you looking for a superhero origin story?", {"Action": 0.6, "Sci-Fi": 0.4, "Fantasy": 0.2}),
    ]

    # ── VIBES & NIGHT TYPE ────────────────────────────────────────────────────
    vibe_questions = [
        ("Is this a chill, lazy evening where you just want to relax and turn off your brain?", {"Comedy": 0.5, "Romance": 0.3, "Action": 0.2}),
        ("Are you in a hyped-up mood and want something high energy to keep you awake?", {"Action": 0.7, "Thriller": 0.4, "Sci-Fi": 0.2}),
        ("Do you want to watch something alone, quiet, and reflective?", {"Drama": 0.8, "Sci-Fi": 0.3, "Romance": 0.2}),
        ("Are you watching this with someone special — a date night?", {"Romance": 0.7, "Comedy": 0.4, "Horror": 0.2}),
        ("Is this a late-night watch where you want something intense and atmospheric?", {"Thriller": 0.6, "Horror": 0.5, "Sci-Fi": 0.2}),
        ("Are you looking for something to binge all night long?", {"Thriller": 0.5, "Sci-Fi": 0.5, "Fantasy": 0.3}),
        ("Do you want a movie that leaves you feeling good and optimistic about life?", {"Comedy": 0.6, "Drama": 0.3, "Romance": 0.2}),
        ("Are you in the mood for something completely weird and unconventional?", {"Sci-Fi": 0.5, "Fantasy": 0.4, "Comedy": 0.3}),
    ]

    # ── SPECIFIC TROPES ───────────────────────────────────────────────────────
    tropes = [
        ("Do you love 'heist' movies where a crew plans a massive robbery?", {"Thriller": 0.6, "Action": 0.4, "Comedy": 0.2}),
        ("Are you a fan of 'whodunit' murder mysteries?", {"Thriller": 0.8, "Drama": 0.3, "Comedy": 0.2}),
        ("Do you enjoy post-apocalyptic movies set after the end of the world?", {"Sci-Fi": 0.6, "Action": 0.4, "Horror": 0.2}),
        ("Do you like 'coming-of-age' stories about teenagers figuring out life?", {"Drama": 0.6, "Comedy": 0.5, "Romance": 0.3}),
        ("Are you looking for a sports underdog story?", {"Drama": 0.7, "Action": 0.3}),
        ("Do you love movies featuring time loops (like living the same day over and over)?", {"Sci-Fi": 0.5, "Comedy": 0.4, "Thriller": 0.3}),
    ]

    all_questions = deep_dives + hybrid_scenarios + vibe_questions + tropes
    
    for text, mapping in all_questions:
        bank.append({"text": text, "mapping": mapping})

    return bank
