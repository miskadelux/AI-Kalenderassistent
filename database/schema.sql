CREATE TABLE IF NOT EXISTS events (
    -- id: Primärnyckel som räknas upp automatiskt för varje händelse
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- title: Obligatorisk titel med rimlig längd
    title VARCHAR(255) NOT NULL,
    -- description: Valfri lång text för detaljer kring händelsen
    description TEXT,
    -- Datum och tider för händelsen
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    -- status: ENUM används här eftersom fältet bara tillåter ett fast antal fördefinierade värden ('aktiv' eller 'avbokad'). 
    -- Standardvärdet sätts till 'aktiv'.
    status ENUM('aktiv', 'avbokad') DEFAULT 'aktiv',
    -- created_at: Uppfyller FR-2.2 genom att automatiskt sätta tidsstämpeln när raden skapas
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Validering: Säkerställer att sluttiden inte kan vara tidigare än starttiden
    CONSTRAINT chk_end_time_after_start CHECK (end_time > start_time)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
-- Obs om tidslängd (FR-1.4): Tidslängden lagras inte i databasen utan räknas ut dynamiskt 
-- i applikationen (Python/Flask) utifrån start_time och end_time för att undvika redundans.