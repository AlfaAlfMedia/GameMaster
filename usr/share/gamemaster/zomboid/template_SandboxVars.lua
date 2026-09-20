SandboxVars = {
    VERSION = 6,
    -- Dies ändert den \Bevölkerungsdichte Multiplikator\ unter Bevölkerung (erweitert). Standard=Normal
    -- 1 = Verrückt
    -- 2 = Sehr Viele
    -- 3 = Viele
    -- 4 = Normal
    -- 5 = Wenige
    -- 6 = Keine
    Zombies = 4,
    -- Steuert, wie Zombies auf der Karte verteilt werden. Standard=Mehr in Städten
    -- 1 = Mehr in Städten
    -- 2 = Gleichmäßig
    Distribution = 1,
    -- Controls whether some randomization is applied to zombie distribution.
    ZombieVoronoiNoise = true,
    -- Damit die Zombies wiederkehren, muss die Zone für den ausgewählten Zeitpunkt ungesehen sein. Standard=Keine
    -- 1 = Oft
    -- 2 = Normal
    -- 3 = Selten
    -- 4 = Keine
    ZombieRespawn = 4,
    -- Zombies wird erlaubt, in leere Zellen einzuwandern.
    ZombieMigrate = true,
    -- Standard=1 Stunde, 30 Minuten
    -- 1 = 15 Minuten
    -- 2 = 30 Minuten
    -- 3 = 1 Stunde
    -- 4 = 1 Stunde, 30 Minuten
    -- 5 = 2 Stunden
    -- 6 = 3 Stunden
    -- 7 = 4 Stunden
    -- 8 = 5 Stunden
    -- 9 = 12 Stunden
    -- 10 = Echtzeit
    -- 11 = 8 stunden
    -- 12 = 9 stunden
    -- 13 = 10 stunden
    -- 14 = 11 stunden
    -- 15 = 12 stunden
    -- 16 = 13 stunden
    -- 17 = 14 stunden
    -- 18 = 15 stunden
    -- 19 = 16 stunden
    -- 20 = 17 stunden
    -- 21 = 18 stunden
    -- 22 = 19 stunden
    -- 23 = 20 stunden
    -- 24 = 21 stunden
    -- 25 = 22 stunden
    -- 26 = 23 stunden
    -- 27 = Echtzeit
    DayLength = 4,
    StartYear = 1,
    -- Monat, in dem das Spiel beginnt. Standard=Juli
    -- 1 = Januar
    -- 2 = Februar
    -- 3 = März
    -- 4 = April
    -- 5 = Mai
    -- 6 = Juni
    -- 7 = Juli
    -- 8 = August
    -- 9 = September
    -- 10 = Oktober
    -- 11 = November
    -- 12 = Dezember
    StartMonth = 7,
    -- Tag des Monats, an dem das Spiel beginnt.
    StartDay = 9,
    -- Stunde des Tages, an dem Spiel beginnt. Standard=9 Uhr
    -- 1 = 7 Uhr
    -- 2 = 9 Uhr
    -- 3 = 12 Uhr
    -- 4 = 13 Uhr
    -- 5 = 15 Uhr
    -- 6 = 21 Uhr
    -- 7 = 0 Uhr
    -- 8 = 2 Uhr
    -- 9 = 5 Uhr
    StartTime = 2,
    -- Whether the time of day changes naturally, or it's always day/night. Standard=Normal
    -- 1 = Normal
    -- 2 = Endless Day
    -- 3 = Endless Night
    DayNightCycle = 1,
    -- Whether weather changes or remains at a single state. Standard=Normal
    -- 1 = Normal
    -- 2 = No Weather
    -- 3 = Endless Rain
    -- 4 = Endless Storm
    -- 5 = Endless Snow
    -- 6 = Endless Blizzard
    ClimateCycle = 1,
    -- Whether fog occurs naturally, never occurs, or is always present. Standard=Normal
    -- 1 = Normal
    -- 2 = No Fog
    -- 3 = Endless Fog
    FogCycle = 1,
    -- Lege fest, wie lange nach dem Standard-Startdatum (9. Juli 1993) Sanitäranlagen (z.B. Waschbecken) aufhören sollen, unendlichen Wasserquellen zu sein. Standard=0-30 Tage
    -- 1 = Sofort
    -- 2 = 0-30 Tage
    -- 3 = 0-2 Monate
    -- 4 = 0-6 Monate
    -- 5 = 0-1 Jahr
    -- 6 = 0-5 Jahre
    -- 7 = 2-6 Monate
    -- 8 = 6-12 Monate
    -- 9 = Deaktiviert
    WaterShut = 2,
    -- Lege fest, wie lange nach dem Standard-Startdatum (9. Juli 1993) der Strom endgültig abgeschaltet wird. Standard=14 - 30 Days
    -- 1 = Instant
    -- 2 = 14 - 30 Days
    -- 3 = 14 Days - 2 Months
    -- 4 = 14 Days - 6 Months
    -- 5 = 14 Days - 1 Year
    -- 6 = 14 Days - 5 Years
    -- 7 = 2 - 6 Months
    -- 8 = 6 - 12 Months
    -- 9 = Disabled
    ElecShut = 2,
    -- Steuert, wie lange Alarmbatterien halten, nachdem der Strom abgeschaltet wird. Standard=0-30 Tage
    -- 1 = Sofort
    -- 2 = 0-30 Tage
    -- 3 = 0-2 Monate
    -- 4 = 0-6 Monate
    -- 5 = 0-1 Jahr
    -- 6 = 0-5 Jahre
    AlarmDecay = 2,
    -- Lege fest, wie lange nach dem Standard-Startdatum (9. Juli 1993) Sanitäranlagen (z.B. Waschbecken) aufhören sollen, unendlichen Wasserquellen zu sein. Minimum=-1 Maximum=2147483647 Standard=14
    WaterShutModifier = 14,
    -- Lege fest, wie lange nach dem Standard-Startdatum (9. Juli 1993) der Strom endgültig abgeschaltet wird. Minimum=-1 Maximum=2147483647 Standard=14
    ElecShutModifier = 14,
    -- Steuert, wie lange Alarmbatterien halten, nachdem der Strom abgeschaltet wird. Minimum=-1 Maximum=2147483647 Standard=14
    AlarmDecayModifier = 14,
    -- Any food that can rot or spoil. Minimum=0,00 Maximum=4,00 Standard=0,80
    FoodLootNew = 0.8,
    -- All other items that can be read, including books, fliers, and newspapers. Minimum=0,00 Maximum=4,00 Standard=0,60
    LiteratureLootNew = 0.6,
    -- Books that provide skill XP multipliers. Minimum=0,00 Maximum=4,00 Standard=0,60
    SkillBookLoot = 0.6,
    -- Items that teach recipes. Minimum=0,00 Maximum=4,00 Standard=0,60
    RecipeResourceLoot = 0.6,
    -- Medicine, bandages and first aid tools. Minimum=0,00 Maximum=4,00 Standard=0,60
    MedicalLootNew = 0.6,
    -- Angeln, Zelte, Campingausrüstung usw. Minimum=0,00 Maximum=4,00 Standard=0,60
    SurvivalGearsLootNew = 0.6,
    -- Canned and dried food, beverages. Minimum=0,00 Maximum=4,00 Standard=0,60
    CannedFoodLootNew = 0.6,
    -- Weapons that are not tools in other categories. Minimum=0,00 Maximum=4,00 Standard=0,60
    WeaponLootNew = 0.6,
    -- Beinhaltet auch Waffenaufsätze. Minimum=0,00 Maximum=4,00 Standard=1,20
    RangedWeaponLootNew = 1.2,
    -- Loose ammo, boxes and magazines. Minimum=0,00 Maximum=4,00 Standard=0,60
    AmmoLootNew = 0.6,
    -- Vehicle parts and the tools needed to install them. Minimum=0,00 Maximum=4,00 Standard=0,60
    MechanicsLootNew = 0.6,
    -- Alles andere. Bezieht sich auch auf die Nahrungssuche in Stadt- und Straßenzonen. Minimum=0,00 Maximum=4,00 Standard=0,80
    OtherLootNew = 0.8,
    -- All wearable items that are not containers. Minimum=0,00 Maximum=4,00 Standard=0,60
    ClothingLootNew = 0.6,
    -- Rucksäcke und andere tragbare/ausrüstbare Behälter, z. B. Koffer. Minimum=0,00 Maximum=4,00 Standard=0,60
    ContainerLootNew = 0.6,
    -- Schlüssel für Gebäude/Autos, Schlüsselanhänger und Schlösser. Minimum=0,00 Maximum=4,00 Standard=0,40
    KeyLootNew = 0.4,
    -- VHS-Kasetten und CDs. Minimum=0,00 Maximum=4,00 Standard=0,60
    MediaLootNew = 0.6,
    -- Spiffo-Artikel, Plüschtiere und andere Andenken zum Sammeln, z. B. Fotos. Minimum=0,00 Maximum=4,00 Standard=0,60
    MementoLootNew = 0.6,
    -- Gegenstände, die beim Kochen zum Einsatz kommen, einschließlich solcher, die als Waffen verwendet werden können (z. B. Messer). Keine Lebensmittel. Einschließlich brauchbarer und unbrauchbarer Gegenstände. Minimum=0,00 Maximum=4,00 Standard=0,60
    CookwareLootNew = 0.6,
    -- Gegenstände und Waffen, die als Zutaten zum Basteln oder Bauen verwendet werden. Allgemeine Kategorie, die keine zu anderen Kategorien wie Kochen und Medizin gehörenden Gegenstände umfasst. Keine Werkzeuge. Minimum=0,00 Maximum=4,00 Standard=0,60
    MaterialLootNew = 0.6,
    -- Gegenstände und potenzielle Waffen, die sowohl in der Tier- als auch in der Pflanzenzucht verwendet werden, wie z. B. Saatgut, Kellen oder Schaufeln. Minimum=0,00 Maximum=4,00 Standard=0,60
    FarmingLootNew = 0.6,
    -- Gegenstände und Waffen, die zu Werkzeugen gehören, aber nicht in andere Kategorien wie Kfz-Mechanik oder Landwirtschaft passen. Minimum=0,00 Maximum=4,00 Standard=0,60
    ToolLootNew = 0.6,
    -- <BHC> [!] Es wird empfohlen, diese Einstellung NICHT zu ändern. [!] <RGB:1,1,1>   Kann verwendet werden, um die Chance auf Beute anzupassen, wenn die Beute gespawnt wird. Kann Anzahl der Würfe nicht unter 1 reduzieren. Kann sich bei hohen Werten negativ auf die Leistung auswirken. Es wird dringend empfohlen, diese Einstellung nicht zu ändern. Minimum=0,10 Maximum=100,00 Standard=1,00
    RollsMultiplier = 1.0,
    -- Eine durch Kommas getrennte Liste von Gegenstandstypen, die nicht als gewöhnliche Beute spawnen werden.
    LootItemRemovalList = "",
    -- Wenn diese Option aktiviert ist, spawnen Gegenstände, die auf der Entfernungsliste von Beutegegenständen stehen oder deren Seltenheit auf 'Keine' eingestellt ist, nicht in zufälligen Weltgeschichten.
    RemoveStoryLoot = false,
    -- Wenn diese Option aktiviert ist, spawnen Gegenstände, die auf der Entfernungsliste von Beutegegenständen stehen oder deren Seltenheit auf 'Keine' eingestellt ist, nicht an oder auf Zombies.
    RemoveZombieLoot = false,
    -- Ist der Wert größer als 0, wird das Spawnen von Beute im Verhältnis zur Anzahl der Zombies in der Nähe erhöht,  wobei der Effekt mit dieser Zahl multipliziert wird. Minimum=0 Maximum=20 Standard=0
    ZombiePopLootEffect = 0,
    -- Minimum=0,00 Maximum=0,20 Standard=0,05
    InsaneLootFactor = 0.05,
    -- Minimum=0,05 Maximum=0,60 Standard=0,20
    ExtremeLootFactor = 0.2,
    -- Minimum=0,20 Maximum=1,00 Standard=0,60
    RareLootFactor = 0.6,
    -- Minimum=0,60 Maximum=2,00 Standard=1,00
    NormalLootFactor = 1.0,
    -- Minimum=1,00 Maximum=3,00 Standard=2,00
    CommonLootFactor = 2.0,
    -- Minimum=2,00 Maximum=4,00 Standard=3,00
    AbundantLootFactor = 3.0,
    -- Steuert die globale Temperatur. Standard=Normal
    -- 1 = Sehr kalt
    -- 2 = Kalt
    -- 3 = Normal
    -- 4 = Heiß
    -- 5 = Sehr heiß
    Temperature = 3,
    -- Steuert wie oft es regnet. Standard=Normal
    -- 1 = Sehr trocken
    -- 2 = Trocken
    -- 3 = Normal
    -- 4 = Regnerisch
    -- 5 = Sehr regnerisch
    Rain = 3,
    -- Anzahl der Tage bis 100% Wachstum. Standard=Langsam (200 Tage)
    -- 1 = Sehr schnell (20 Tage)
    -- 2 = Schnell (50 Tage)
    -- 3 = Normal (100 Tage)
    -- 4 = Langsam (200 Tage)
    -- 5 = Sehr langsam (500 Tage)
    ErosionSpeed = 4,
    -- Anzahl der Tage bis 100% Wachstum.  -1 bedeutet kein Wachstum.  Null bedeutet, die Erosionsgeschwindigkeitsoption zu nutzen.  Maximum 36,500 (100 Jahre). Minimum=-1 Maximum=36500 Standard=0
    ErosionDays = 0,
    -- Steuert die Geschwindigkeit des Pflanzenwachstums. Standard=Normal
    -- 1 = Sehr schnell
    -- 2 = Schnell
    -- 3 = Normal
    -- 4 = Langsam
    -- 5 = Sehr langsam
    Farming = 3,
    -- Steuert die Zeit, die es braucht, bis Lebensmittel in einem Komposter zerfallen. Standard=2 Wochen
    -- 1 = 1 Woche
    -- 2 = 2 Wochen
    -- 3 = 3 Wochen
    -- 4 = 4 Wochen
    -- 5 = 6 Wochen
    -- 6 = 8 Wochen
    -- 7 = 10 Wochen
    -- 8 = 12 Wochen
    CompostTime = 2,
    -- Wie schnell der Hunger, Durst und die Müdigkeit des Charakters abnimmt. Standard=Normal
    -- 1 = Sehr schnell
    -- 2 = Schnell
    -- 3 = Normal
    -- 4 = Langsam
    -- 5 = Sehr langsam
    StatsDecrease = 3,
    -- Wirkt sich auf die Schwierigkeit von Fischen/Futtersuche aus. Standard=Normal
    -- 1 = Sehr schlecht
    -- 2 = Schlecht
    -- 3 = Normal
    -- 4 = Reichlich
    -- 5 = Sehr reichlich
    NatureAbundance = 3,
    -- Die Chance beim ersten Einbruch, den Hausalarm auszulösen. Standard=Manchmal
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    Alarm = 4,
    -- Definiere hier, wie oft die Türen/Fenster der Häuser gesperrt sein sollen. Standard=Sehr oft
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    LockedHouses = 6,
    -- Beginne mit einer Tasche und ein paar nützlichen Werkzeugen.
    StarterKit = false,
    -- Nährwert von Lebensmitteln wirkt sich auf den Zustand des Spielers aus.
    Nutrition = true,
    -- Definiere hier, wie schnell das Essen außerhalb eines Kühlschranks verderben soll. Standard=Normal
    -- 1 = Sehr schnell
    -- 2 = Schnell
    -- 3 = Normal
    -- 4 = Langsam
    -- 5 = Sehr langsam
    FoodRotSpeed = 3,
    -- Definiere hier, wie wirksam ein Kühlschrank kühlen kann. Standard=Normal
    -- 1 = Sehr wenig
    -- 2 = Wenig
    -- 3 = Normal
    -- 4 = Hoch
    -- 5 = Sehr hoch
    -- 6 = Kein Verfall
    FridgeFactor = 3,
    -- Wenn der Wert größer als 0 ist, wird die Beute die gesehen wurde, nicht vor ablauf dieser Zeit (in Stunden) respawnen. Minimum=0 Maximum=2147483647 Standard=0
    SeenHoursPreventLootRespawn = 0,
    -- Wenn der Wert größer als 0 ist, wird nach X Stunden in allen Behältern der Welt Beute respawnen. Um Beute spawnen zu können, muss ein Behälter mindestens einmal geplündert worden sein. Beute-Respawn wird nicht durch die Sichtbarkeit oder nachfolgendes Plündern beeinflusst. Minimum=0 Maximum=2147483647 Standard=0
    HoursForLootRespawn = 0,
    -- Behälter mit dieser oder höheren Gegenstandsanzahl, werden keine neue Beute bekommen. Minimum=0 Maximum=2147483647 Standard=5
    MaxItemsForLootRespawn = 5,
    -- Gegenstände erscheinen nicht in Zonen, die Spieler verbarrikadiert oder bebaut haben.
    ConstructionPreventsLootRespawn = true,
    -- Eine durch Kommata getrennte Liste von Gegenstandstypen, die nach der bestimmten Anzahl an Stunden entfernt werden.
    WorldItemRemovalList = "Base.Hat, Base.Glasses, Base.Maggots, Base.Slug, Base.Slug2, Base.Snail, Base.Worm, Base.Dung_Mouse, Base.Dung_Rat",
    -- Anzahl der Stunden, die vergangen sein müssen, bis ein Gegenstand, der auf den Boden gefallen ist, aus der Spielwelt gelöscht wird.  Gegenstände werden entfernt, wenn der betreffende Teil der Karte das nächste Mal geladen wird.  Null bedeutet, dass die Gegenstände nicht entfernt werden. Minimum=0,00 Maximum=2147483647,00 Standard=24,00
    HoursForWorldItemRemoval = 24.0,
    -- Wenn aktiv, werden alle Elemente, die *nicht* in der Lösch-Liste enthalten sind, entfernt.
    ItemRemovalListBlacklistToggle = false,
    -- Dies wird Auswirkungen auf die Erosion und den Zustand der Lebensmittel haben. Standard=0
    -- 1 = 0
    -- 2 = 1
    -- 3 = 2
    -- 4 = 3
    -- 5 = 4
    -- 6 = 5
    -- 7 = 6
    -- 8 = 7
    -- 9 = 8
    -- 10 = 9
    -- 11 = 10
    -- 12 = 11
    -- 13 = 12
    TimeSinceApo = 1,
    -- Hat einfluss auf den täglichen Wasserverbrauch der Pflanzenanlagen, sowie die Resistenz gegenüber Krankheiten. Standard=Normal
    -- 1 = Sehr hoch
    -- 2 = Hoch
    -- 3 = Normal
    -- 4 = Niedrig
    -- 5 = Sehr niedrig
    PlantResilience = 3,
    -- Beeinflusst den Ertrag der Pflanzenanlagen. Standard=Normal
    -- 1 = Sehr schlecht
    -- 2 = Schlecht
    -- 3 = Normal
    -- 4 = Reichlich
    -- 5 = Sehr reichlich
    PlantAbundance = 3,
    -- Erholung von der Ermüdung durch das Ausführen von Handlungen. Standard=Normal
    -- 1 = Sehr schnell
    -- 2 = Schnell
    -- 3 = Normal
    -- 4 = Langsam
    -- 5 = Sehr langsam
    EndRegen = 3,
    -- Regelt wie oft Hubschrauber über die Event-Zone fliegen. Standard=Einmal
    -- 1 = Nie
    -- 2 = Einmal
    -- 3 = Manchmal
    -- 4 = Oft
    Helicopter = 2,
    -- Regelt wie oft Zombies angezogen werden. Wenn Meta-Ereignisse wie Hubschrauber und ferne Schüsse auftreten. Standard=Manchmal
    -- 1 = Nie
    -- 2 = Manchmal
    -- 3 = Oft
    MetaEvent = 2,
    -- Regelt die Ereignisse in der Nachtzeit, während der Spieler schläft. Standard=Nie
    -- 1 = Nie
    -- 2 = Manchmal
    -- 3 = Oft
    SleepingEvent = 1,
    -- Beeinflusst wie viel Kraftstoff von Generatoren verbraucht wird. Ein Generator der keinen Kraftstoff benötigt, sollte auf 0,0 eingestellt werden. Minimum=0,00 Maximum=100,00 Standard=0,10
    GeneratorFuelConsumption = 0.1,
    -- Erhöht/Verringert die Wahrscheinlichkeit zum Erscheinen von Stromgeneratoren in der Welt. Standard=Oft
    -- 1 = Extrem selten
    -- 2 = Selten
    -- 3 = Manchmal
    -- 4 = Oft
    -- 5 = Sehr oft
    -- 6 = Häufig
    -- 7 = Reichlich
    GeneratorSpawning = 4,
    -- Hat Auswirkungen darauf, wieviel Anmerkungen eine geplünderte Karte haben wird, die von einem verstorbenen Überlebenden gezeichnet wurden. Standard=Manchmal
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    AnnotatedMapChance = 4,
    -- Fügt bei der Charakter-Erstellung freie Punkte hinzu. Minimum=-100 Maximum=100 Standard=0
    CharacterFreePoints = 0,
    -- Gibt den von Spielern gebauten Konstruktionen zusätzliche Trefferpunkte, so dass sie widerstandsfähiger gegen Zombie-Schäden sind. Standard=Normal
    -- 1 = Sehr niedrig
    -- 2 = Niedrig
    -- 3 = Normal
    -- 4 = Hoch
    -- 5 = Sehr hoch
    ConstructionBonusPoints = 3,
    -- Regelt die Umgebungsbeleuchtung bei Nacht. Standard=Normal
    -- 1 = Pechschwarz
    -- 2 = Dunkel
    -- 3 = Normal
    -- 4 = Hell
    NightDarkness = 3,
    -- Regelt die Zeit von der Abenddämmerung bis zum Morgengrauen. Standard=Normal
    -- 1 = Immer Nacht
    -- 2 = Lang
    -- 3 = Normal
    -- 4 = Kurz
    -- 5 = Immer Tag
    NightLength = 3,
    -- Aktiviert/Deaktiviert gebrochene Gliedmaßen, wenn Überlebende Verletzungen von Stößen, Zombie-Schäden und Stürzen erhalten.
    BoneFracture = true,
    -- Erhöht/Verringert die Auswirkungen von Verletzungen auf den Körper und die Heilungszeit. Standard=Normal
    -- 1 = Niedrig
    -- 2 = Normal
    -- 3 = Hoch
    InjurySeverity = 2,
    -- Anzahl der Spielstunden bis Zombie-Leichen automatisch aus der Welt entfernt werden. (Ersetzt die ehemalige HoursForCorpseRemoval Server Option). Minimum=-1,00 Maximum=2147483647,00 Standard=216,00
    HoursForCorpseRemoval = 216.0,
    -- Beeinflusst die Wirkung der Gesundheit und Emotionen des Spielers in der Nähe verfaulender Körper. Standard=Normal
    -- 1 = Keine
    -- 2 = Niedrig
    -- 3 = Normal
    -- 4 = Hoch
    -- 5 = Verrückt
    DecayingCorpseHealthImpact = 3,
    -- Bestimmt, ob in der Nähe befindliche „lebende“ Zombies die gleichen Auswirkungen auf die Gesundheit und die Emotionen des Spielers haben.
    ZombieHealthImpact = false,
    -- Wie viel Blut wird auf Boden und Wände gespritzt. Standard=Normal
    -- 1 = Keine
    -- 2 = Niedrig
    -- 3 = Normal
    -- 4 = Hoch
    -- 5 = Blutregen
    BloodLevel = 3,
    -- Beeinflusst wie schnell Kleidung verschlechtert wird, schmutzig und blutig. (Kann deaktiviert werden.) Standard=Normal
    -- 1 = Deaktiviert
    -- 2 = Langsam
    -- 3 = Normal
    -- 4 = Schnell
    ClothingDegradation = 3,
    -- Bestimmt, ob Feuer sich ausbreiten kann.
    FireSpread = true,
    -- Anzahl der Tage im Spiel, bevor verdorbenes Essen von der Karte entfernt wird. Der Wert -1 bedeutet, dass faules Essen niemals entfernt wird. Minimum=-1 Maximum=2147483647 Standard=-1
    DaysForRottenFoodRemoval = -1,
    -- Wenn aktiviert, arbeiten die Generatoren im Aussenbereich und ermöglichen so bspw., die Versorgung der Zapfsäule.
    AllowExteriorGenerator = true,
    -- Steuert die maximale Intensität des Nebels. Standard=Normal
    -- 1 = Normal
    -- 2 = Mäßig
    -- 3 = Niedrig
    -- 4 = Keine
    MaxFogIntensity = 1,
    -- Steuert die maximale Intensität des Regens. Standard=Normal
    -- 1 = Normal
    -- 2 = Mäßig
    -- 3 = Niedrig
    MaxRainFxIntensity = 1,
    -- Wenn aktiviert sammelt sich Schnee nicht auf dem Boden an, sondern ist nur auf der Vegetation und den Dächern sichtbar.
    EnableSnowOnGround = true,
    -- Dekativiere um während eines Nahkampfangriffs ungehindert laufen zu können.
    AttackBlockMovements = true,
    -- Erhöht/Verringert die Wahrscheinlichkeit von zufällig Generierten Häusern/Verstecken: Ausgebrannt, mit versteckter Beute oder Leichen etc. Standard=Selten
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    -- 7 = Immer versuchen
    SurvivorHouseChance = 3,
    -- Wahrscheinlichkeit, mit der Straßengeschichten auftauchen (z.B. Straßensperren). Standard=Selten
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    -- 7 = Immer versuchen
    VehicleStoryChance = 3,
    -- Wahrscheinlichkeit, mit der Geschichten auftauchen, die für Kartenzonen spezifisch sind (z.B. Lagerfeuer im Wald). Standard=Selten
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    -- 7 = Immer versuchen
    ZoneStoryChance = 3,
    -- Ermöglicht es dir, bei der Anpassung deines Charakters aus allen Kleidungsstücken im Spiel zu wählen
    AllClothesUnlocked = false,
    -- Wenn deaktiviert, wird verunreinigtes Wasser nicht als solches durch eine Warnung gekennzeichnet
    EnableTaintedWaterText = true,
    -- Ermöglicht das Spawnen von Fahrzeugen.
    EnableVehicles = true,
    -- Regelt wie oft Autos auf der Karte gefunden werden können. Standard=Wenig
    -- 1 = Keine
    -- 2 = Sehr wenig
    -- 3 = Wenig
    -- 4 = Normal
    -- 5 = Hoch
    CarSpawnRate = 3,
    -- Verwende dies, um die allgemeine Lautstärke des Motors zu reduzieren oder zu erhöhen. Minimum=0,00 Maximum=100,00 Standard=1,00
    ZombieAttractionMultiplier = 1.0,
    -- Regelt, ob Autos verschlossen sind, Schlüssel zum Starten benötigen usw.
    VehicleEasyUse = false,
    -- Regelt den Kraftstofffüllstand von entdeckten Autos. Standard=Niedrig
    -- 1 = Sehr niedrig
    -- 2 = Niedrig
    -- 3 = Normal
    -- 4 = Hoch
    -- 5 = Sehr hoch
    -- 6 = Voll
    InitialGas = 2,
    -- Wenn aktiv, geht den Zapfsäulen nie der Kraftstoff aus
    FuelStationGasInfinite = false,
    -- Gibt die Mindestmenge an Benzin an, die in den Zapfsäulen auftauchen kann. Aktiviere die Fortgeschritten-Option unten, um eine benutzerdefinierte Menge zu verwenden. Minimum=0,00 Maximum=1,00 Standard=0,00
    FuelStationGasMin = 0.0,
    -- Gibt die Höchstmenge an Benzin an, die in den Zapfsäulen auftauchen kann. Aktiviere die Fortgeschritten-Option unten, um eine benutzerdefinierte Menge zu verwenden. Minimum=0,00 Maximum=1,00 Standard=0,80
    FuelStationGasMax = 0.8,
    -- Gibt die Wahrscheinlichkeit in Prozent an, dass einzelne Zapfsäulen beim Start leer sind. Minimum=0 Maximum=100 Standard=20
    FuelStationGasEmptyChance = 20,
    -- Regelt die Wahrscheinlich, dass Autos verschlossen sind Standard=Manchmal
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    LockedCar = 4,
    -- Steuert wie sprithungrig die Fahrzeuge auf der Karte sind. Minimum=0,00 Maximum=100,00 Standard=1,00
    CarGasConsumption = 1.0,
    -- In welchem Zustand wird das neue Auto erscheinen. Standard=Normal
    -- 1 = Sehr niedrig
    -- 2 = Niedrig
    -- 3 = Normal
    -- 4 = Hoch
    -- 5 = Sehr hoch
    CarGeneralCondition = 3,
    -- Steuert den Schaden, der den verunfallenden Fahrzeugen zugefügt wird. Standard=Normal
    -- 1 = Sehr niedrig
    -- 2 = Niedrig
    -- 3 = Normal
    -- 4 = Hoch
    -- 5 = Sehr hoch
    CarDamageOnImpact = 3,
    -- Schaden den der Spieler bei einer Kollision vom Auto erhält. Standard=Keine
    -- 1 = Keine
    -- 2 = Niedrig
    -- 3 = Normal
    -- 4 = Hoch
    -- 5 = Sehr hoch
    DamageToPlayerFromHitByACar = 1,
    -- Aktiviere oder deaktiviere Fahrzeugwracks, die auf den Hauptstraßen der Karte erscheinen.
    TrafficJam = true,
    -- Wie oft werden Autos mit einem Alarm gefunden. Standard=Selten
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    CarAlarm = 3,
    -- Aktiviere/Deaktiviere, Spielerschäden durch einen Autounfall.
    PlayerDamageFromCrash = true,
    -- Anzahl der Stunden bevor der Sirenenton aufhört zu spielen.  0.0 - bedeutet spielen bis der Akku leer ist. Minimum=0,00 Maximum=168,00 Standard=0,00
    SirenShutoffHours = 0.0,
    -- Regelt die Chancen für Fahrzeuge mit Kraftstoff im Tank zu finden. Standard=Normal
    -- 1 = Niedrig
    -- 2 = Normal
    -- 3 = Hoch
    ChanceHasGas = 2,
    -- Legt fest, ob der Spieler ein Auto entdecken kann, das nach der Infektion gewartet und gepflegt wurde. Standard=Niedrig
    -- 1 = Keine
    -- 2 = Niedrig
    -- 3 = Normal
    -- 4 = Hoch
    RecentlySurvivorVehicles = 2,
    -- Wenn aktiviert, gewisse Nahkampfwaffen können mehrere Zombies mit einem Schlag treffen.
    MultiHitZombies = false,
    -- Chance gebissen zu werden, wenn ein Zombie von hinten angreift. Standard=Hoch
    -- 1 = Niedrig
    -- 2 = Mittel
    -- 3 = Hoch
    RearVulnerability = 3,
    -- Bestimmt, ob Zombies sich auf den Klang von Fahrzeugsirenen zubewegen.
    SirenEffectsZombies = true,
    -- Geschwindigkeit, mit der Tierstatistiken (Hunger, Durst, usw.) abnehmen. Standard=Normal
    -- 1 = Ultra schnell
    -- 2 = Sehr schnell
    -- 3 = Schnell
    -- 4 = Normal
    -- 5 = Langsam
    -- 6 = Sehr langsam
    AnimalStatsModifier = 4,
    -- Geschwindigkeit, mit der Tierstatistiken (Hunger, Durst, usw.) im Meta-Modus abnehmen. Standard=Normal
    -- 1 = Ultra schnell
    -- 2 = Sehr schnell
    -- 3 = Schnell
    -- 4 = Normal
    -- 5 = Langsam
    -- 6 = Sehr langsam
    AnimalMetaStatsModifier = 4,
    -- Wie lange Tiere trächtig sind, bevor sie Junge gebären. Standard=Normal
    -- 1 = Ultra schnell
    -- 2 = Sehr schnell
    -- 3 = Schnell
    -- 4 = Normal
    -- 5 = Langsam
    -- 6 = Sehr langsam
    AnimalPregnancyTime = 4,
    -- Geschwindigkeit, mit der Tiere altern. Standard=Normal
    -- 1 = Ultra schnell
    -- 2 = Sehr schnell
    -- 3 = Schnell
    -- 4 = Normal
    -- 5 = Langsam
    -- 6 = Sehr langsam
    AnimalAgeModifier = 4,
    -- Standard=Normal
    -- 1 = Ultra schnell
    -- 2 = Sehr schnell
    -- 3 = Schnell
    -- 4 = Normal
    -- 5 = Langsam
    -- 6 = Sehr langsam
    AnimalMilkIncModifier = 4,
    -- Standard=Normal
    -- 1 = Ultra schnell
    -- 2 = Sehr schnell
    -- 3 = Schnell
    -- 4 = Normal
    -- 5 = Langsam
    -- 6 = Sehr langsam
    AnimalWoolIncModifier = 4,
    -- Bestimmt die Chance, Tiere auf Farmen zu finden. Standard=Oft
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    -- 7 = Immer
    AnimalRanchChance = 5,
    -- Anzahl der Stunden, nach deren Ablauf Gras nachwächst,  das von Tieren gefressen oder vom Spieler gemäht wurde. Minimum=1 Maximum=9999 Standard=240
    AnimalGrassRegrowTime = 240,
    -- Bestimmt, ob ein Meta-Fuchs (d.h. ein im Spiel nicht sichtbarer) deine  Hühner angreifen kann, wenn die Stalltür nachts aufgelassen wird.
    AnimalMetaPredator = false,
    -- Bei aktivierter Option beachten betroffene Tierarten ihren Fortpflanzungszirkus.  Ansonsten können sie sich das ganze Jahr über fortpflanzen bzw. Eier legen.
    AnimalMatingSeason = true,
    -- Wie lange es dauert, bevor Küken aus Eiern hüpfen. Standard=Normal
    -- 1 = Ultra schnell
    -- 2 = Sehr schnell
    -- 3 = Schnell
    -- 4 = Normal
    -- 5 = Langsam
    -- 6 = Sehr langsam
    AnimalEggHatch = 4,
    -- Wenn aktiviert, ziehen Tierlaute in der Nähe befindliche Zombies an.
    AnimalSoundAttractZombies = true,
    -- The chance of animals leaving tracks. Standard=Manchmal
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    AnimalTrackChance = 4,
    -- The chance of creating a path for animals to be hunted. Standard=Manchmal
    -- 1 = Nie
    -- 2 = Extrem selten
    -- 3 = Selten
    -- 4 = Manchmal
    -- 5 = Oft
    -- 6 = Sehr oft
    AnimalPathChance = 4,
    -- Häufigkeit und Intensität von Befall durch Ratten und Ungeziefer in betroffenen Gebäuden. Minimum=0 Maximum=50 Standard=25
    MaximumRatIndex = 25,
    -- Wie lange es dauert, bis die maximale Ungezieferdichte erreicht ist. Minimum=0 Maximum=365 Standard=90
    DaysUntilMaximumRatIndex = 90,
    -- Wenn ein Medium nicht vollständig gesehen oder gelesen wurde, bestimmt diese Einstellung, ob es vollständig angezeigt, als "???" angezeigt oder komplett ausgeblendet wird. Standard=Komplett ausgeblendet
    -- 1 = Vollständig angezeigt
    -- 2 = Als ??? angezeigt
    -- 3 = Komplett ausgeblendet
    MetaKnowledge = 3,
    -- Wenn aktiv kannst du alle Rezepte sehen, die an einer Station hergestellt werden können, auch wenn sie noch nicht bekannt sind.
    SeeNotLearntRecipe = true,
    -- Wenn ein Gebäude mehr Räumen hat, als hier festgelegt, wird es nicht geplündert. Minimum=0 Maximum=200 Standard=50
    MaximumLootedBuildingRooms = 50,
    -- Regelt, ob das Vergiften von Lebensmitteln aktiviert ist. Standard=Richtig
    -- 1 = Richtig
    -- 2 = Falsch
    -- 3 = Nur die Bleichmittelvergiftung ist deaktiviert
    EnablePoisoning = 1,
    -- Bestimmt, ob und wann Maden in Leichen spawnen können. Standard=In und um Körper
    -- 1 = In und um Körper
    -- 2 = Nur in Körpern
    -- 3 = Niemals
    MaggotSpawn = 1,
    -- Je höher der Wert, desto länger halten Glühbirnen, bevor sie kaputt gehen. Bei 0 gehen Glühbirnen niemals kaputt. Beeinflusst nicht die Fahrzeugscheinwerfer. Minimum=0,00 Maximum=1000,00 Standard=2,00
    LightBulbLifespan = 2.0,
    -- Fischreichtum in Flüssen und Seen. Standard=Schlecht
    -- 1 = Sehr schlecht
    -- 2 = Schlecht
    -- 3 = Normal
    -- 4 = Reichlich
    -- 5 = Sehr reichlich
    FishAbundance = 2,
    -- Steht eine Fähigkeit auf dieser Stufe oder höher, bringen Fernsehen/VHS/andere Medien  keine EP ein. Minimum=0 Maximum=10 Standard=3
    LevelForMediaXPCutoff = 3,
    -- Steht eine Fähigkeit auf dieser Stufe oder höher, bringt das Zerlegen von Möbeln keine EP für ein. Gilt nicht für Elektrotechnik. Minimum=0 Maximum=10 Standard=0
    LevelForDismantleXPCutoff = 0,
    -- Anzahl der Tage, bevor alte Blutspritzer entfernt werden. Entfernung erfolgt, wenn Kartenteile geladen werden. Bei 0 werden sie nie entfernt. Minimum=0 Maximum=365 Standard=0
    BloodSplatLifespanDays = 0,
    -- Anzahl der Tage, bis wieder von bereits gelesener Literatur profitiert werden kann. Minimum=1 Maximum=365 Standard=45
    LiteratureCooldown = 45,
    -- Bestimmt, ob sich der Bonus auf Eigenschaftspunkte bei der Auswahl mehrerer negativer Eigenschaften verringert. Standard=Keine
    -- 1 = Keine
    -- 2 = 1 Punkt Strafe pro 3 gewählte negative Eigenschaften
    -- 3 = 1 Punkt Strafe pro 2 gewählte negative Eigenschaften
    -- 4 = 1 Punkt Strafe für jede gewählte negative Eigenschaft nach der ersten
    NegativeTraitsPenalty = 1,
    -- Dauer in Spielwelt-Minuten, die zum Lesen einer Seite benötigt wird. Minimum=0,00 Maximum=60,00 Standard=2,00
    MinutesPerPage = 2.0,
    -- Wenn aktiv, sterben Nutzpflanzen und Kräuter, die in Gebäuden wachsen. Gilt nicht für Hauspflanzen.
    KillInsideCrops = true,
    -- Wenn aktiv, wird der Pflanzenwachstum von Jahreszeiten beeinflusst.
    PlantGrowingSeasons = true,
    -- <BHC> [!] Es wird empfohlen, diese Einstellung NICHT zu ändern. Eine Änderung dieser Einstellung kann zu Performance-Problemen führen. [!] <RGB:1,1,1>   Wenn aktiviert, kann Erde auch auf anderen Ebenen als der Bodenebene platziert und bewirtschaftet werden.
    PlaceDirtAboveground = false,
    -- Die Geschwindigkeit des Pflanzenwachstums. Minimum=0,10 Maximum=100,00 Standard=1,00
    FarmingSpeedNew = 1.0,
    -- Bestimmt den Ernteertrag. Minimum=0,10 Maximum=10,00 Standard=1,00
    FarmingAmountNew = 1.0,
    -- Die Wahrscheinlichkeit, dass ein Gebäude bereits geplündert ist, wenn es gefunden wird. Aktiviere die Fortgeschritten-Option unten, um eine benutzerdefinierten Wert zu verwenden. Minimum=0 Maximum=200 Standard=25
    MaximumLooted = 25,
    -- Wie lange es dauert, bis die maximale Wahrscheinlichkeit auf das Vorfinden geplünderter Häuser erreicht ist. Minimum=0 Maximum=3650 Standard=90
    DaysUntilMaximumLooted = 90,
    -- Die Chance, dass ein Gebäude auf dem Land bereits geplündert ist, wenn es gefunden wird. Aktiviere die Fortgeschritten-Option unten, um eine benutzerdefinierten Wert zu verwenden. Minimum=0,00 Maximum=2,00 Standard=0,50
    RuralLooted = 0.5,
    -- Die maximale Beute, die nicht spawnen wird, wenn der Tag der maximal verringerten Beute erreicht ist. Aktiviere die Fortgeschritten-Option unten, um eine exakte Prozentzahl zu verwenden. Minimum=0 Maximum=100 Standard=20
    MaximumDiminishedLoot = 20,
    -- Tage, bis die maximal verringerten Beute erreicht wird. Minimum=0 Maximum=3650 Standard=3650
    DaysUntilMaximumDiminishedLoot = 3650,
    -- Wirkt als Multiplikator bei der Belastung der Muskeln durch das Schwingen von Waffen oder das Tragen schwerer Lasten. Minimum=0,00 Maximum=10,00 Standard=0,70
    MuscleStrainFactor = 0.7,
    -- Wirkt als Multiplikator für Unwohlsein durch getragener Gegenstände. Minimum=0,00 Maximum=10,00 Standard=0,80
    DiscomfortFactor = 0.8,
    -- Wenn größer als Null, kann Schaden durch schwere Wundinfektionen verursacht werden. Minimum=0,00 Maximum=10,00 Standard=1,00
    WoundInfectionFactor = 1.0,
    -- Wenn aktiviert, wird Kleidung mit zufälligen Farbtönen nicht so dunkel sein, dass sie praktisch schwarz ist.
    NoBlackClothes = true,
    -- Deaktiviert die Wahrscheinlichkeit, beim Klettern an Seilen oder über Mauern hinweg zu scheitern.
    EasyClimbing = false,
    -- Die maximale Brenndauer an Material, die in ein Lagerfeuer, einen Holzofen usw. eingelegt werden kann. Minimum=1 Maximum=168 Standard=8
    MaximumFireFuelHours = 8,
    -- Ersetzt die Trefferchance-Mechanik durch die Berechnung der Schadenschance. In diesem Modus wird das Zielen durch den Spieler bevorzugt. Standard=Zombies only
    -- 1 = Disabled
    -- 2 = Zombies only
    -- 3 = All types of target
    FirearmUseDamageChance = 2,
    -- Ein Multiplikator für die Entfernung, aus der Zombies Schüsse hören können. Minimum=0,20 Maximum=2,00 Standard=1,00
    FirearmNoiseMultiplier = 1.0,
    -- Multiplikator für die Wahrscheinlichkeit, mit der Schusswaffen klemmen. 0 deaktiviert Klemmen. Minimum=0,00 Maximum=10,00 Standard=1,00
    FirearmJamMultiplier = 1.0,
    -- Multiplikator für Zustandseffekte auf Trefferchance. 0 deaktiviert Zustandsstrafe. Minimum=0,00 Maximum=10,00 Standard=1,00
    FirearmMoodleMultiplier = 1.0,
    -- Multiplikator für Wettereffekte (Wind, Regen und Nebel) bei Trefferchance. 0 deaktiviert Wettereffekte. Minimum=0,00 Maximum=10,00 Standard=1,00
    FirearmWeatherMultiplier = 1.0,
    -- Aktivieren, damit Kopfbedeckungen wie Schweißmasken die Trefferchance beeinflussen
    FirearmHeadGearEffect = true,
    -- Chance to turn a dirt floor into a clay floor. Applies to lakes. Minimum=0,00 Maximum=1,00 Standard=0,05
    ClayLakeChance = 0.05,
    -- Chance to turn a dirt floor into a clay floor. Applies to rivers. Minimum=0,00 Maximum=1,00 Standard=0,05
    ClayRiverChance = 0.05,
    -- Minimum=1 Maximum=100 Standard=20
    GeneratorTileRange = 20,
    -- How many levels both above and below a generator it can provide with electricity. Minimum=1 Maximum=15 Standard=3
    GeneratorVerticalPowerRange = 3,
    Basement = {
        -- Bestimmt, wie häufig Keller an zufälligen Orten spawnen. Standard=Manchmal
        -- 1 = Nie
        -- 2 = Extrem selten
        -- 3 = Selten
        -- 4 = Manchmal
        -- 5 = Oft
        -- 6 = Sehr oft
        -- 7 = Immer
        SpawnFrequency = 4,
    },
    Map = {
        -- Wenn diese Option aktiviert ist, wird ein Minikartenfenster angezeigt.
        AllowMiniMap = false,
        -- Wenn diese Option aktiviert ist, kann auf die Weltkarte zugegriffen werden.
        AllowWorldMap = true,
        -- Wenn diese Option aktiviert ist, wird die Weltkarte beim Spielstart komplett bekannt sein.
        MapAllKnown = false,
        -- Bei aktivierter Funktion können die Karten nur gelesen werden, wenn eine Lichtquelle vorhanden ist.
        MapNeedsLight = true,
    },
    ZombieLore = {
        -- Steuert die Zombie-Bewegungsrate. Standard=zufällig
        -- 1 = Sprinter
        -- 2 = Schnelle Schlurfer
        -- 3 = Schlurfer
        -- 4 = zufällig
        Speed = 4,
        -- Wenn zufällige Geschwindigkeit aktiviert ist, wird hier festgesetzt, wie viel Prozent der Zombies Sprinter sind. Aktiviere die Fortgeschritten-Option unten, um einen benutzerdefinierten Prozentsatz zu verwenden. Minimum=0 Maximum=100 Standard=0
        SprinterPercentage = 0,
        -- Steuert den Schaden den Zombies pro Angriff verursachen. Standard=Normal
        -- 1 = Übermenschlich
        -- 2 = Normal
        -- 3 = Schwach
        -- 4 = zufällig
        Strength = 2,
        -- Steuert die Schwierigkeit, Zombies zu töten. Standard=zufällig
        -- 1 = Zäh
        -- 2 = Normal
        -- 3 = Zerbrechlich
        -- 4 = zufällig
        Toughness = 4,
        -- Steuert wie sich der Zombievirus ausbreitet. Standard=Blut + Speichel
        -- 1 = Blut + Speichel
        -- 2 = Nur Speichel
        -- 3 = Jeder ist Infiziert
        -- 4 = Keine
        Transmission = 1,
        -- Steuert wie schnell die Infektion wirksam wird. Standard=2-3 Tage
        -- 1 = Sofort
        -- 2 = 0-30 Sekunden
        -- 3 = 0-1 Minute
        -- 4 = 0-12 Stunden
        -- 5 = 2-3 Tage
        -- 6 = 1-2 Wochen
        -- 7 = Nie
        Mortality = 5,
        -- Steuert wie schnell sich Leichen als Zombies erheben. Standard=0-1 Minute
        -- 1 = Sofort
        -- 2 = 0-30 Sekunden
        -- 3 = 0-1 Minute
        -- 4 = 0-12 Stunden
        -- 5 = 2-3 Tage
        -- 6 = 1-2 Wochen
        Reanimate = 3,
        -- Steuert die Zombie-Intelligenz. Standard=Einfache Navigation
        -- 1 = Navigieren + Verwendung von Türen
        -- 2 = Navigieren
        -- 3 = Einfache Navigation
        -- 4 = zufällig
        Cognition = 3,
        -- Minimum=0 Maximum=100 Standard=0
        DoorOpeningPercentage = 0,
        -- Steuert welche Zombies unter Fahrzeuge kriechen können. Standard=Oft
        -- 1 = Nie
        -- 2 = Sehr selten
        -- 3 = Selten
        -- 4 = Manchmal
        -- 5 = Oft
        -- 6 = Sehr oft
        -- 7 = Immer
        CrawlUnderVehicle = 5,
        -- Steuert wie lange sich Zombies an Spieler erinnern, nachdem sie sie gesehen oder gehört haben. Standard=Normal
        -- 1 = Lang
        -- 2 = Normal
        -- 3 = Kurz
        -- 4 = Keine
        -- 5 = Zufällig
        -- 6 = Zufällig zwischen Normal und Keine
        Memory = 2,
        -- Steuert den Sichtradius von Zombies. Standard=Zufällig zwischen Normal und Schlecht
        -- 1 = Adleraugen
        -- 2 = Normal
        -- 3 = Schlecht
        -- 4 = Zufällig
        -- 5 = Zufällig zwischen Normal und Schlecht
        Sight = 5,
        -- Steuert den Hörradius von Zombies. Standard=Zufällig zwischen Normal und Schlecht
        -- 1 = Sehr gut
        -- 2 = Normal
        -- 3 = Schlecht
        -- 4 = Zufällig
        -- 5 = Zufällig zwischen Normal und Schlecht
        Hearing = 5,
        -- Aktiviert die neue fortschrittliche Tarnungsmechanik, die es dir ermöglicht, dich vor Zombies hinter Autos zu verstecken, Eigenschaften und Wetter zu berücksichtigen uvm.
        SpottedLogic = true,
        -- Zombies greifen Türen und Konstruktionen an während sie umherwandern, wenn keine Spieler zu Sehen/Hören sind.
        ThumpNoChasing = false,
        -- Bestimmt ob Zombies, Spieler-Konstruktionen und Verteidigungen zerstören können oder nicht.
        ThumpOnConstruction = true,
        -- Gibt an, ob Zombies während des Tages oder bei Nacht vermehrt aktiv sind. Inaktive Zombies werden langsamer und neigen nicht dazu auf Jagd zu gehen. Standard=Beides
        -- 1 = Beides
        -- 2 = Nacht
        -- 3 = Tag
        ActiveOnly = 1,
        -- Ermöglicht Zombies, Hausalarme auszulösen, wenn sie durch Fenster und Türen brechen.
        TriggerHouseAlarm = true,
        -- Wenn aktiviert können mehrere Zombies dich bei ihrem Angriff herunterziehen zum fressen. Abhängig von Stärke der Zombies.
        ZombiesDragDown = true,
        -- Bestimmt, ob Kriecher-Zombies in der Nähe eines Spielers dazu beitragen, von einer Zombiegruppe heruntergezogen und getötet zu werden.
        ZombiesCrawlersDragDown = false,
        -- Wenn diese Funktion aktiviert ist, haben Zombies die Möglichkeit, nach dem Spieler zu greifen, nachdem sie über einen Zaun geklettert sind, wenn Sie zu nahe sind.
        ZombiesFenceLunge = true,
        -- Dient als Multiplikator bei der Bestimmung der Wirksamkeit der von Zombies getragenen Rüstung. Minimum=0,00 Maximum=100,00 Standard=2,00
        ZombiesArmorFactor = 2.0,
        -- Der maximale Verteidigungsprozentsatz, den eine getragene Schutzbekleidung einem Zombie bieten kann. Minimum=0 Maximum=100 Standard=85
        ZombiesMaxDefense = 85,
        -- Prozentuale Chance, eine zufällig angebrachte Waffe zu haben. Minimum=0 Maximum=100 Standard=6
        ChanceOfAttachedWeapon = 6,
        -- Wie viel Schaden Zombies nehmen, wenn sie aus der Höhe fallen. Minimum=0,00 Maximum=100,00 Standard=1,00
        ZombiesFallDamage = 1.0,
        -- Bestimmt, ob einige tot aussehende Zombies wiederbelebt werden und den Spieler angreifen. Standard=Einige Zombies auf der Welt werden vorgeben, tot zu sein
        -- 1 = Einige Zombies auf der Welt werden vorgeben, tot zu sein
        -- 2 = Einige Zombies auf der Welt, sowie einige, die Sie „töten“, können vorgeben, tot zu sein
        -- 3 = Zombies werden niemals vorgeben, tot zu sein
        DisableFakeDead = 1,
        -- Zombies werden nicht dort spawnen, wo Spieler spawnen. Standard=Im Gebäude und drumherum
        -- 1 = Im Gebäude und drumherum
        -- 2 = Im Gebäude
        -- 3 = Im Raum
        -- 4 = Zombies können überall spawnen
        PlayerSpawnZombieRemoval = 1,
        -- How many zombies it takes to damage a tall fence. Minimum=-1 Maximum=100 Standard=25
        FenceThumpersRequired = 25,
        -- How quickly zombies damage tall fences. Minimum=0,01 Maximum=100,00 Standard=1,00
        FenceDamageMultiplier = 1.0,
    },
    ZombieConfig = {
        -- Identisch mit der Einstellung unter Sandbox \Zombie Anzahl\. 4.0 Verrückt Minimum=0,00 Maximum=4,00 Standard=0,65
        PopulationMultiplier = 0.65,
        -- Zum Einstellen der gewünschten Bevölkerung zu Beginn des Spiels. Minimum=0,00 Maximum=4,00 Standard=1,00
        PopulationStartMultiplier = 1.0,
        -- Zum Einstellen der gewünschten Bevölkerungsdichte an einem 'Höhepunkt-Tag'. Minimum=0,00 Maximum=4,00 Standard=1,50
        PopulationPeakMultiplier = 1.5,
        -- Der Tag, an dem die Bevölkerungsdichte ihren Höhepunkt erreicht. Minimum=1 Maximum=365 Standard=28
        PopulationPeakDay = 28,
        -- Anzahl der Stunden die verstreichen müssen, bevor Zombies in einer Zelle wiedererscheinen. Null bedeutet, deaktiviert Minimum=0,00 Maximum=8760,00 Standard=0,00
        RespawnHours = 0.0,
        -- Anzahl der Stunden in der eine Zelle ungesehen bleiben muss, bevor Zombies wiedererscheinen. Minimum=0,00 Maximum=8760,00 Standard=0,00
        RespawnUnseenHours = 0.0,
        -- Der Bruchteil einer Zelle mit der gewünschten Bevölkerungsdichte, die alle 'Wiedererschein-Stunden' aufgestellt werden können. Minimum=0,00 Maximum=1,00 Standard=0,00
        RespawnMultiplier = 0.0,
        -- Anzahl der Stunden die verstreichen müssen bevor Zombies wandern um Teile der Zelle zu leeren. Minimum=0,00 Maximum=8760,00 Standard=12,00
        RedistributeHours = 12.0,
        -- Der Abstand zum letzten gehörten Geräusch zu dem virtuelle Zombies wandern. Minimum=10 Maximum=1000 Standard=100
        FollowSoundDistance = 100,
        -- Die Gruppenstärke von echten Zombies die sich im Leerlauf bilden. Null bedeutet, Zombies bilden keine Gruppen. Gruppen bilden sich nicht innerhalb von Gebäuden oder Waldzonen. Minimum=0 Maximum=1000 Standard=20
        RallyGroupSize = 20,
        -- Prozentsatz, um den die Größe von Zombie-Gruppen von der Standardgröße abweichen kann (sowohl größer als auch kleiner).   Bei einer Varianz von 50 % und einer Standardgruppengröße von 20 variiert die Gruppengröße beispielsweise zwischen 10 und 30. Minimum=0 Maximum=100 Standard=50
        RallyGroupSizeVariance = 50,
        -- Entfernungen die echte Zombies im Leerlauf reisen um Gruppen zu bilden. Minimum=5 Maximum=50 Standard=20
        RallyTravelDistance = 20,
        -- Der Abstand zwischen den Zombiegruppen. Minimum=5 Maximum=25 Standard=15
        RallyGroupSeparation = 15,
        -- Die Distanz zwischen Mitglieder und dem Anführer der Gruppe. Minimum=1 Maximum=10 Standard=3
        RallyGroupRadius = 3,
        -- Controls the maximum number of zombies tracked before cleanup occurs. 0 means zombies will not be cleaned up. The default value (300) is strongly recommended. Increasing this value or setting to 0 may cause severe performance problems. For troubleshooting and bug-report purposes, please reproduce any issue with the default setting before submitting a report. Minimum=0 Maximum=5000 Standard=300
        ZombiesCountBeforeDelete = 300,
    },
    MultiplierConfig = {
        -- Bestimmt die Rate, mit der sich alle Fähigkeiten entwickeln. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Global = 1.0,
        -- Wenn diese Option aktiviert wird, werden alle Fähigkeiten den globalen Multiplikator verwenden.
        GlobalToggle = true,
        -- Bestimmt die Rate, mit der sich die Fitness-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Fitness = 1.0,
        -- Bestimmt die Rate, mit der sich die Stärke-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Strength = 1.0,
        -- Bestimmt die Rate, mit der sich die Sprint-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Sprinting = 1.0,
        -- Bestimmt die Rate, mit der sich die Leichtfüßig-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Lightfoot = 1.0,
        -- Bestimmt die Rate, mit der sich die Flink-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Nimble = 1.0,
        -- Bestimmt die Rate, mit der sich die Schleichen-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Sneak = 1.0,
        -- Bestimmt die Rate, mit der sich die Axt-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Axe = 1.0,
        -- Bestimmt die Rate, mit der sich die Stumpfwaffen-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Blunt = 1.0,
        -- Bestimmt die Rate, mit der sich die Kurze-Stumpfwaffe-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        SmallBlunt = 1.0,
        -- Bestimmt die Rate, mit der sich die Lange-Klingenwaffe-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        LongBlade = 1.0,
        -- Bestimmt die Rate, mit der sich die Kurze-Klingenwaffe-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        SmallBlade = 1.0,
        -- Bestimmt die Rate, mit der sich die Speer-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Spear = 1.0,
        -- Bestimmt die Rate, mit der sich die Instandhaltungs-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Maintenance = 1.0,
        -- Bestimmt die Rate, mit der sich die Tischlerei-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Woodwork = 1.0,
        -- Bestimmt die Rate, mit der sich die Kochen-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Cooking = 1.0,
        -- Bestimmt die Rate, mit der sich die Landwirtschaft-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Farming = 1.0,
        -- Bestimmt die Rate, mit der sich die Erste-Hilfe-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Doctor = 1.0,
        -- Bestimmt die Rate, mit der sich die Elektrotechnik-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Electricity = 1.0,
        -- Bestimmt die Rate, mit der sich die Schweißen-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        MetalWelding = 1.0,
        -- Bestimmt die Rate, mit der sich die Kfz-Mechanik-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Mechanics = 1.0,
        -- Bestimmt die Rate, mit der sich die Schneidern-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Tailoring = 1.0,
        -- Bestimmt die Rate, mit der sich die Zielen-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Aiming = 1.0,
        -- Bestimmt die Rate, mit der sich die Nachladen-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Reloading = 1.0,
        -- Bestimmt die Rate, mit der sich die Angeln-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Fishing = 1.0,
        -- Bestimmt die Rate, mit der sich die Fallenstellen-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Trapping = 1.0,
        -- Bestimmt die Rate, mit der sich die Nahrungssuche-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        PlantScavenging = 1.0,
        -- Bestimmt die Rate, mit der sich die Feuersteinbearbeitung-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        FlintKnapping = 1.0,
        -- Bestimmt die Rate, mit der sich die Maurerei-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Masonry = 1.0,
        -- Bestimmt die Rate, mit der sich die Töpferei-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Pottery = 1.0,
        -- Bestimmt die Rate, mit der sich die Schnitzen-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Carving = 1.0,
        -- Bestimmt die Rate, mit der sich die Tierpflege-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Husbandry = 1.0,
        -- Bestimmt die Rate, mit der sich die Spurensuche-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Tracking = 1.0,
        -- Bestimmt die Rate, mit der sich die Metallbearbeitung-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Blacksmith = 1.0,
        -- Bestimmt die Rate, mit der sich die Schlachtung-Fähigkeit entwickelt. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Butchering = 1.0,
        -- Rate at which Glassmaking skill levels up. Minimum=0,00 Maximum=1000,00 Standard=1,00
        Glassmaking = 1.0,
    },
}
