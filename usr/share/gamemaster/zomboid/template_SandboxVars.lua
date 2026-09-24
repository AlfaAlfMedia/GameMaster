SandboxVars = {
    VERSION = 6,
    -- Population multiplier, the same value as 'Population Multiplier' in the advanced
    -- population settings. Default=Normal
    -- 1 = Insane, 2 = Very high, 3 = High, 4 = Normal, 5 = Low, 6 = None
    Zombies = 4,
    -- How zombies are spread across the map. Default=Urban focused
    -- 1 = Urban focused, 2 = Uniform
    Distribution = 1,
    -- Applies some randomisation to the zombie distribution.
    ZombieVoronoiNoise = true,
    -- How often zombies return. The zone must stay unseen for the chosen period.
    -- Default=None
    -- 1 = Often, 2 = Normal, 3 = Rare, 4 = None
    ZombieRespawn = 4,
    -- Allow zombies to migrate into empty cells.
    ZombieMigrate = true,
    -- Length of one in-game day. Default=1 hour 30 minutes
    -- 1 = 15 min, 2 = 30 min, 3 = 1 h, 4 = 1 h 30, 5 = 2 h, 6 = 3 h, 7 = 4 h, 8 = 5 h,
    -- 9 = 12 h, 10 = real time, 11 = 8 h, 12 = 9 h, 13 = 10 h, 14 = 11 h, 15 = 12 h,
    -- 16 = 13 h, 17 = 14 h, 18 = 15 h, 19 = 16 h, 20 = 17 h, 21 = 18 h, 22 = 19 h,
    -- 23 = 20 h, 24 = 21 h, 25 = 22 h, 26 = 23 h, 27 = real time
    DayLength = 4,
    StartYear = 1,
    -- Month the game starts in. Default=July
    -- 1 = January, 2 = February, 3 = March, 4 = April, 5 = May, 6 = June, 7 = July,
    -- 8 = August, 9 = September, 10 = October, 11 = November, 12 = December
    StartMonth = 7,
    -- Day of the month the game starts on.
    StartDay = 9,
    -- Hour of the day the game starts at. Default=9 AM
    -- 1 = 7 AM, 2 = 9 AM, 3 = 12 PM, 4 = 1 PM, 5 = 3 PM, 6 = 9 PM, 7 = 12 AM,
    -- 8 = 2 AM, 9 = 5 AM
    StartTime = 2,
    -- Whether the time of day changes naturally or stays fixed. Default=Normal
    -- 1 = Normal, 2 = Endless day, 3 = Endless night
    DayNightCycle = 1,
    -- Whether weather changes or stays in a single state. Default=Normal
    -- 1 = Normal, 2 = No weather, 3 = Endless rain, 4 = Endless storm,
    -- 5 = Endless snow, 6 = Endless blizzard
    ClimateCycle = 1,
    -- Whether fog occurs naturally, never, or always. Default=Normal
    -- 1 = Normal, 2 = No fog, 3 = Endless fog
    FogCycle = 1,
    -- How long after the default start date (9 July 1993) taps stop being an infinite
    -- water source. Default=0-30 days
    -- 1 = Instant, 2 = 0-30 days, 3 = 0-2 months, 4 = 0-6 months, 5 = 0-1 year,
    -- 6 = 0-5 years, 7 = 2-6 months, 8 = 6-12 months, 9 = Disabled
    WaterShut = 2,
    -- How long after the default start date (9 July 1993) the power is cut for good.
    -- Default=14-30 days
    -- 1 = Instant, 2 = 14-30 days, 3 = 14 days - 2 months, 4 = 14 days - 6 months,
    -- 5 = 14 days - 1 year, 6 = 14 days - 5 years, 7 = 2-6 months, 8 = 6-12 months,
    -- 9 = Disabled
    ElecShut = 2,
    -- How long alarm batteries last after the power is cut. Default=0-30 days
    -- 1 = Instant, 2 = 0-30 days, 3 = 0-2 months, 4 = 0-6 months, 5 = 0-1 year,
    -- 6 = 0-5 years
    AlarmDecay = 2,
    -- Exact number of days until the water is shut off.
    -- Min=-1 Max=2147483647 Default=14
    WaterShutModifier = 14,
    -- Exact number of days until the power is shut off.
    -- Min=-1 Max=2147483647 Default=14
    ElecShutModifier = 14,
    -- Exact number of days alarm batteries last after the power is cut.
    -- Min=-1 Max=2147483647 Default=14
    AlarmDecayModifier = 14,
    -- Any food that can rot or spoil. Min=0.00 Max=4.00 Default=0.80
    FoodLootNew = 0.8,
    -- Everything else that can be read: books, fliers, newspapers. Min=0.00 Max=4.00 Default=0.60
    LiteratureLootNew = 0.6,
    -- Books that grant skill XP multipliers. Min=0.00 Max=4.00 Default=0.60
    SkillBookLoot = 0.6,
    -- Items that teach recipes. Min=0.00 Max=4.00 Default=0.60
    RecipeResourceLoot = 0.6,
    -- Medicine, bandages and first aid tools. Min=0.00 Max=4.00 Default=0.60
    MedicalLootNew = 0.6,
    -- Fishing gear, tents, camping equipment and similar. Min=0.00 Max=4.00 Default=0.60
    SurvivalGearsLootNew = 0.6,
    -- Canned and dried food, beverages. Min=0.00 Max=4.00 Default=0.60
    CannedFoodLootNew = 0.6,
    -- Weapons that are not tools covered by another category. Min=0.00 Max=4.00 Default=0.60
    WeaponLootNew = 0.6,
    -- Ranged weapons, including weapon attachments. Min=0.00 Max=4.00 Default=1.20
    RangedWeaponLootNew = 1.2,
    -- Loose ammo, boxes and magazines. Min=0.00 Max=4.00 Default=0.60
    AmmoLootNew = 0.6,
    -- Vehicle parts and the tools needed to install them. Min=0.00 Max=4.00 Default=0.60
    MechanicsLootNew = 0.6,
    -- Everything else. Also applies to foraging in town and road zones. Min=0.00 Max=4.00 Default=0.80
    OtherLootNew = 0.8,
    -- All wearable items that are not containers. Min=0.00 Max=4.00 Default=0.60
    ClothingLootNew = 0.6,
    -- Bags and other carryable containers, such as suitcases. Min=0.00 Max=4.00 Default=0.60
    ContainerLootNew = 0.6,
    -- Building and car keys, key rings and padlocks. Min=0.00 Max=4.00 Default=0.40
    KeyLootNew = 0.4,
    -- VHS tapes and CDs. Min=0.00 Max=4.00 Default=0.60
    MediaLootNew = 0.6,
    -- Spiffo items, plush toys and other collectables such as photos. Min=0.00 Max=4.00 Default=0.60
    MementoLootNew = 0.6,
    -- Items used for cooking, including ones usable as weapons such as knives. No food.
    -- Includes both usable and broken items. Min=0.00 Max=4.00 Default=0.60
    CookwareLootNew = 0.6,
    -- Items and weapons used as crafting or building material. General category that
    -- excludes items belonging to cooking, medical and similar groups. No tools.
    -- Min=0.00 Max=4.00 Default=0.60
    MaterialLootNew = 0.6,
    -- Items and possible weapons used in animal and plant husbandry, such as seeds,
    -- trowels or shovels. Min=0.00 Max=4.00 Default=0.60
    FarmingLootNew = 0.6,
    -- Tools that do not fit another category such as mechanics or farming. Min=0.00 Max=4.00 Default=0.60
    ToolLootNew = 0.6,
    -- [!] Changing this setting is NOT recommended. [!]
    -- Adjusts the loot chance when loot is rolled. Cannot reduce the number of rolls
    -- below 1, and high values can hurt performance.
    -- Min=0.10 Max=100.00 Default=1.00
    RollsMultiplier = 1.0,
    -- Comma-separated list of item types that never spawn as ordinary loot.
    LootItemRemovalList = "",
    -- Items on the removal list, or set to rarity 'none', do not spawn in random world
    -- stories.
    RemoveStoryLoot = false,
    -- Items on the removal list, or set to rarity 'none', do not spawn on zombies.
    RemoveZombieLoot = false,
    -- Above 0, loot spawning rises in proportion to the number of nearby zombies,
    -- multiplied by this value. Min=0 Max=20 Default=0
    ZombiePopLootEffect = 0,
    -- Min=0.00 Max=0.20 Default=0.05
    InsaneLootFactor = 0.05,
    -- Min=0.05 Max=0.60 Default=0.20
    ExtremeLootFactor = 0.2,
    -- Min=0.20 Max=1.00 Default=0.60
    RareLootFactor = 0.6,
    -- Min=0.60 Max=2.00 Default=1.00
    NormalLootFactor = 1.0,
    -- Min=1.00 Max=3.00 Default=2.00
    CommonLootFactor = 2.0,
    -- Min=2.00 Max=4.00 Default=3.00
    AbundantLootFactor = 3.0,
    -- Global temperature. Default=Normal
    -- 1 = Very cold, 2 = Cold, 3 = Normal, 4 = Hot, 5 = Very hot
    Temperature = 3,
    -- How often it rains. Default=Normal
    -- 1 = Very dry, 2 = Dry, 3 = Normal, 4 = Rainy, 5 = Very rainy
    Rain = 3,
    -- Days until erosion reaches full growth. Default=Slow (200 days)
    -- 1 = Very fast (20 days), 2 = Fast (50 days), 3 = Normal (100 days),
    -- 4 = Slow (200 days), 5 = Very slow (500 days)
    ErosionSpeed = 4,
    -- Days until full growth. -1 disables growth, 0 uses the ErosionSpeed option above.
    -- Maximum 36500, which is 100 years. Min=-1 Max=36500 Default=0
    ErosionDays = 0,
    -- Speed of plant growth. Default=Normal
    -- 1 = Very fast, 2 = Fast, 3 = Normal, 4 = Slow, 5 = Very slow
    Farming = 3,
    -- Time food needs to decay in a composter. Default=2 weeks
    -- 1 = 1 week, 2 = 2 weeks, 3 = 3 weeks, 4 = 4 weeks, 5 = 6 weeks, 6 = 8 weeks,
    -- 7 = 10 weeks, 8 = 12 weeks
    CompostTime = 2,
    -- How fast hunger, thirst and fatigue build up. Default=Normal
    -- 1 = Very fast, 2 = Fast, 3 = Normal, 4 = Slow, 5 = Very slow
    StatsDecrease = 3,
    -- Difficulty of fishing and foraging. Default=Normal
    -- 1 = Very poor, 2 = Poor, 3 = Normal, 4 = Abundant, 5 = Very abundant
    NatureAbundance = 3,
    -- Chance of setting off a house alarm on the first break-in. Default=Sometimes
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often
    Alarm = 4,
    -- How often house doors and windows are locked. Default=Very often
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often
    LockedHouses = 6,
    -- Start with a bag and a few useful tools.
    StarterKit = false,
    -- Food nutrition affects the character's condition.
    Nutrition = true,
    -- How fast food spoils outside a fridge. Default=Normal
    -- 1 = Very fast, 2 = Fast, 3 = Normal, 4 = Slow, 5 = Very slow
    FoodRotSpeed = 3,
    -- How effectively a fridge cools. Default=Normal
    -- 1 = Very low, 2 = Low, 3 = Normal, 4 = High, 5 = Very high, 6 = No decay
    FridgeFactor = 3,
    -- Above 0, loot that has been seen does not respawn before this many hours have
    -- passed. Min=0 Max=2147483647 Default=0
    SeenHoursPreventLootRespawn = 0,
    -- Above 0, loot respawns in every container in the world after this many hours. A
    -- container must have been looted at least once. Not affected by visibility or by
    -- later looting. Min=0 Max=2147483647 Default=0
    HoursForLootRespawn = 0,
    -- Containers holding this many items or more receive no new loot.
    -- Min=0 Max=2147483647 Default=5
    MaxItemsForLootRespawn = 5,
    -- Loot does not spawn in zones that players have barricaded or built on.
    ConstructionPreventsLootRespawn = true,
    -- Comma-separated list of item types removed after the number of hours set below.
    WorldItemRemovalList = "Base.Hat, Base.Glasses, Base.Maggots, Base.Slug, Base.Slug2, Base.Snail, Base.Worm, Base.Dung_Mouse, Base.Dung_Rat",
    -- Hours before an item dropped on the ground is deleted from the world. Removal
    -- happens the next time that part of the map is loaded. 0 keeps items forever.
    -- Min=0.00 Max=2147483647.00 Default=24.00
    HoursForWorldItemRemoval = 24.0,
    -- When enabled, everything *not* on the removal list is removed instead.
    ItemRemovalListBlacklistToggle = false,
    -- Months that have passed since the outbreak. Affects erosion and the state of
    -- food. Default=0
    -- 1 = 0, 2 = 1, 3 = 2, 4 = 3, 5 = 4, 6 = 5, 7 = 6, 8 = 7, 9 = 8, 10 = 9, 11 = 10,
    -- 12 = 11, 13 = 12
    TimeSinceApo = 1,
    -- Daily water use of crops and their resistance to disease. Default=Normal
    -- 1 = Very high, 2 = High, 3 = Normal, 4 = Low, 5 = Very low
    PlantResilience = 3,
    -- Crop yield. Default=Normal
    -- 1 = Very poor, 2 = Poor, 3 = Normal, 4 = Abundant, 5 = Very abundant
    PlantAbundance = 3,
    -- Recovery from the fatigue caused by performing actions. Default=Normal
    -- 1 = Very fast, 2 = Fast, 3 = Normal, 4 = Slow, 5 = Very slow
    EndRegen = 3,
    -- How often a helicopter passes over the event zone. Default=Once
    -- 1 = Never, 2 = Once, 3 = Sometimes, 4 = Often
    Helicopter = 2,
    -- How often meta events such as helicopters and distant gunshots occur and draw
    -- zombies. Default=Sometimes
    -- 1 = Never, 2 = Sometimes, 3 = Often
    MetaEvent = 2,
    -- Night-time events while the player sleeps. Default=Never
    -- 1 = Never, 2 = Sometimes, 3 = Often
    SleepingEvent = 1,
    -- How much fuel generators burn. 0.0 makes them run without fuel.
    -- Min=0.00 Max=100.00 Default=0.10
    GeneratorFuelConsumption = 0.1,
    -- How likely generators are to spawn in the world. Default=Often
    -- 1 = Extremely rare, 2 = Rare, 3 = Sometimes, 4 = Often, 5 = Very often,
    -- 6 = Common, 7 = Abundant
    GeneratorSpawning = 4,
    -- How many annotations a looted map drawn by a dead survivor carries.
    -- Default=Sometimes
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often
    AnnotatedMapChance = 4,
    -- Extra free points during character creation. Min=-100 Max=100 Default=0
    CharacterFreePoints = 0,
    -- Extra hit points for player-built constructions, making them more resistant to
    -- zombie damage. Default=Normal
    -- 1 = Very low, 2 = Low, 3 = Normal, 4 = High, 5 = Very high
    ConstructionBonusPoints = 3,
    -- Ambient light at night. Default=Normal
    -- 1 = Pitch black, 2 = Dark, 3 = Normal, 4 = Bright
    NightDarkness = 3,
    -- Time from dusk to dawn. Default=Normal
    -- 1 = Always night, 2 = Long, 3 = Normal, 4 = Short, 5 = Always day
    NightLength = 3,
    -- Enable broken limbs from impacts, zombie damage and falls.
    BoneFracture = true,
    -- Effect of injuries on the body and on healing time. Default=Normal
    -- 1 = Low, 2 = Normal, 3 = High
    InjurySeverity = 2,
    -- In-game hours before zombie corpses are removed from the world. Replaces the
    -- former HoursForCorpseRemoval server option.
    -- Min=-1.00 Max=2147483647.00 Default=216.00
    HoursForCorpseRemoval = 216.0,
    -- Effect of nearby rotting bodies on the player's health and mood. Default=Normal
    -- 1 = None, 2 = Low, 3 = Normal, 4 = High, 5 = Insane
    DecayingCorpseHealthImpact = 3,
    -- Whether nearby 'living' zombies have the same effect on health and mood.
    ZombieHealthImpact = false,
    -- How much blood is splattered on floors and walls. Default=Normal
    -- 1 = None, 2 = Low, 3 = Normal, 4 = High, 5 = Blood rain
    BloodLevel = 3,
    -- How fast clothing wears out and gets dirty and bloody. Default=Normal
    -- 1 = Disabled, 2 = Slow, 3 = Normal, 4 = Fast
    ClothingDegradation = 3,
    -- Whether fire can spread.
    FireSpread = true,
    -- In-game days before rotten food is removed from the map. -1 keeps it forever.
    -- Min=-1 Max=2147483647 Default=-1
    DaysForRottenFoodRemoval = -1,
    -- Generators work outdoors, which lets them power fuel pumps and similar.
    AllowExteriorGenerator = true,
    -- Maximum fog intensity. Default=Normal
    -- 1 = Normal, 2 = Moderate, 3 = Low, 4 = None
    MaxFogIntensity = 1,
    -- Maximum rain intensity. Default=Normal
    -- 1 = Normal, 2 = Moderate, 3 = Low
    MaxRainFxIntensity = 1,
    -- Snow settles on the ground. When off it is only visible on vegetation and roofs.
    EnableSnowOnGround = true,
    -- Disable to move freely during a melee attack.
    AttackBlockMovements = true,
    -- Likelihood of randomly generated survivor houses: burnt out, with hidden loot or
    -- corpses. Default=Rare
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often, 7 = Always try
    SurvivorHouseChance = 3,
    -- Likelihood of road stories such as roadblocks. Default=Rare
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often, 7 = Always try
    VehicleStoryChance = 3,
    -- Likelihood of stories tied to map zones, such as a campfire in the woods.
    -- Default=Rare
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often, 7 = Always try
    ZoneStoryChance = 3,
    -- Choose from every clothing item in the game during character customisation.
    AllClothesUnlocked = false,
    -- When off, tainted water is not marked with a warning.
    EnableTaintedWaterText = true,
    -- Allow vehicles to spawn.
    EnableVehicles = true,
    -- How often cars are found on the map. Default=Low
    -- 1 = None, 2 = Very low, 3 = Low, 4 = Normal, 5 = High
    CarSpawnRate = 3,
    -- Overall loudness of engines. Min=0.00 Max=100.00 Default=1.00
    ZombieAttractionMultiplier = 1.0,
    -- Cars are unlocked and need no key to start.
    VehicleEasyUse = false,
    -- Fuel level of discovered cars. Default=Low
    -- 1 = Very low, 2 = Low, 3 = Normal, 4 = High, 5 = Very high, 6 = Full
    InitialGas = 2,
    -- Fuel pumps never run dry.
    FuelStationGasInfinite = false,
    -- Minimum amount of fuel a pump can spawn with. Min=0.00 Max=1.00 Default=0.00
    FuelStationGasMin = 0.0,
    -- Maximum amount of fuel a pump can spawn with. Min=0.00 Max=1.00 Default=0.80
    FuelStationGasMax = 0.8,
    -- Percentage chance that an individual pump starts out empty.
    -- Min=0 Max=100 Default=20
    FuelStationGasEmptyChance = 20,
    -- How likely cars are to be locked. Default=Sometimes
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often
    LockedCar = 4,
    -- How thirsty vehicles on the map are. Min=0.00 Max=100.00 Default=1.00
    CarGasConsumption = 1.0,
    -- Condition newly found cars are in. Default=Normal
    -- 1 = Very low, 2 = Low, 3 = Normal, 4 = High, 5 = Very high
    CarGeneralCondition = 3,
    -- Damage vehicles take in a crash. Default=Normal
    -- 1 = Very low, 2 = Low, 3 = Normal, 4 = High, 5 = Very high
    CarDamageOnImpact = 3,
    -- Damage the player takes when hit by a car. Default=None
    -- 1 = None, 2 = Low, 3 = Normal, 4 = High, 5 = Very high
    DamageToPlayerFromHitByACar = 1,
    -- Vehicle wrecks appear on the map's main roads.
    TrafficJam = true,
    -- How often cars are found with an alarm. Default=Rare
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often
    CarAlarm = 3,
    -- Players take damage in a car crash.
    PlayerDamageFromCrash = true,
    -- Hours before a siren stops sounding. 0.0 plays until the battery is empty.
    -- Min=0.00 Max=168.00 Default=0.00
    SirenShutoffHours = 0.0,
    -- Chance of finding vehicles with fuel in the tank. Default=Normal
    -- 1 = Low, 2 = Normal, 3 = High
    ChanceHasGas = 2,
    -- Chance of finding a car that was looked after since the outbreak. Default=Low
    -- 1 = None, 2 = Low, 3 = Normal, 4 = High
    RecentlySurvivorVehicles = 2,
    -- Some melee weapons can hit several zombies with one swing.
    MultiHitZombies = false,
    -- Chance of being bitten when a zombie attacks from behind. Default=High
    -- 1 = Low, 2 = Medium, 3 = High
    RearVulnerability = 3,
    -- Zombies move towards the sound of vehicle sirens.
    SirenEffectsZombies = true,
    -- Rate at which animal stats such as hunger and thirst decrease. Default=Normal
    -- 1 = Ultra fast, 2 = Very fast, 3 = Fast, 4 = Normal, 5 = Slow, 6 = Very slow
    AnimalStatsModifier = 4,
    -- The same, for animals handled in meta mode. Default=Normal
    -- 1 = Ultra fast, 2 = Very fast, 3 = Fast, 4 = Normal, 5 = Slow, 6 = Very slow
    AnimalMetaStatsModifier = 4,
    -- How long animals stay pregnant before giving birth. Default=Normal
    -- 1 = Ultra fast, 2 = Very fast, 3 = Fast, 4 = Normal, 5 = Slow, 6 = Very slow
    AnimalPregnancyTime = 4,
    -- Rate at which animals age. Default=Normal
    -- 1 = Ultra fast, 2 = Very fast, 3 = Fast, 4 = Normal, 5 = Slow, 6 = Very slow
    AnimalAgeModifier = 4,
    -- Rate at which animals produce milk. Default=Normal
    -- 1 = Ultra fast, 2 = Very fast, 3 = Fast, 4 = Normal, 5 = Slow, 6 = Very slow
    AnimalMilkIncModifier = 4,
    -- Rate at which animals grow wool. Default=Normal
    -- 1 = Ultra fast, 2 = Very fast, 3 = Fast, 4 = Normal, 5 = Slow, 6 = Very slow
    AnimalWoolIncModifier = 4,
    -- Chance of finding animals on farms. Default=Often
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often, 7 = Always
    AnimalRanchChance = 5,
    -- Hours before grass eaten by animals or mown by the player grows back.
    -- Min=1 Max=9999 Default=240
    AnimalGrassRegrowTime = 240,
    -- A meta fox, one not visible in the game, can attack chickens when the coop door
    -- is left open at night.
    AnimalMetaPredator = false,
    -- Affected species follow their breeding season. When off they breed and lay eggs
    -- all year round.
    AnimalMatingSeason = true,
    -- How long eggs take to hatch. Default=Normal
    -- 1 = Ultra fast, 2 = Very fast, 3 = Fast, 4 = Normal, 5 = Slow, 6 = Very slow
    AnimalEggHatch = 4,
    -- Animal noises attract nearby zombies.
    AnimalSoundAttractZombies = true,
    -- Chance of animals leaving tracks. Default=Sometimes
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often
    AnimalTrackChance = 4,
    -- Chance of creating a path along which animals can be hunted. Default=Sometimes
    -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often
    AnimalPathChance = 4,
    -- Frequency and intensity of rat and vermin infestations in affected buildings.
    -- Min=0 Max=50 Default=25
    MaximumRatIndex = 25,
    -- Days until the maximum vermin density is reached. Min=0 Max=365 Default=90
    DaysUntilMaximumRatIndex = 90,
    -- How media that has not been fully watched or read is displayed.
    -- Default=Hidden completely
    -- 1 = Shown in full, 2 = Shown as ???, 3 = Hidden completely
    MetaKnowledge = 3,
    -- See every recipe a station can produce, including ones not yet known.
    SeeNotLearntRecipe = true,
    -- Buildings with more rooms than this are never pre-looted.
    -- Min=0 Max=200 Default=50
    MaximumLootedBuildingRooms = 50,
    -- Whether food poisoning is enabled. Default=True
    -- 1 = True, 2 = False, 3 = Only bleach poisoning disabled
    EnablePoisoning = 1,
    -- Whether and where maggots spawn on corpses. Default=In and around bodies
    -- 1 = In and around bodies, 2 = In bodies only, 3 = Never
    MaggotSpawn = 1,
    -- Higher values make bulbs last longer before they break. 0 means they never break.
    -- Does not affect vehicle headlights. Min=0.00 Max=1000.00 Default=2.00
    LightBulbLifespan = 2.0,
    -- Fish population in rivers and lakes. Default=Poor
    -- 1 = Very poor, 2 = Poor, 3 = Normal, 4 = Abundant, 5 = Very abundant
    FishAbundance = 2,
    -- At or above this skill level, TV, VHS and other media grant no XP.
    -- Min=0 Max=10 Default=3
    LevelForMediaXPCutoff = 3,
    -- At or above this skill level, dismantling furniture grants no XP. Does not apply
    -- to electrical. Min=0 Max=10 Default=0
    LevelForDismantleXPCutoff = 0,
    -- Days before old blood splatter is removed. Removal happens when map chunks are
    -- loaded. 0 means never. Min=0 Max=365 Default=0
    BloodSplatLifespanDays = 0,
    -- Days before already-read literature gives a benefit again.
    -- Min=1 Max=365 Default=45
    LiteratureCooldown = 45,
    -- Whether the trait point bonus shrinks when several negative traits are picked.
    -- Default=None
    -- 1 = None, 2 = 1 point penalty per 3 negative traits,
    -- 3 = 1 point penalty per 2 negative traits,
    -- 4 = 1 point penalty for every negative trait after the first
    NegativeTraitsPenalty = 1,
    -- In-game minutes needed to read one page. Min=0.00 Max=60.00 Default=2.00
    MinutesPerPage = 2.0,
    -- Crops and herbs grown inside buildings die. Does not apply to house plants.
    KillInsideCrops = true,
    -- Plant growth is affected by the seasons.
    PlantGrowingSeasons = true,
    -- [!] Changing this setting is NOT recommended and can cause performance problems. [!]
    -- Allows dirt to be placed and farmed on levels other than the ground floor.
    PlaceDirtAboveground = false,
    -- Speed of plant growth. Min=0.10 Max=100.00 Default=1.00
    FarmingSpeedNew = 1.0,
    -- Harvest yield. Min=0.10 Max=10.00 Default=1.00
    FarmingAmountNew = 1.0,
    -- Chance that a building has already been looted when it is found.
    -- Min=0 Max=200 Default=25
    MaximumLooted = 25,
    -- Days until that maximum chance is reached. Min=0 Max=3650 Default=90
    DaysUntilMaximumLooted = 90,
    -- Chance that a rural building has already been looted when it is found.
    -- Min=0.00 Max=2.00 Default=0.50
    RuralLooted = 0.5,
    -- Maximum share of loot that stops spawning once the day below is reached.
    -- Min=0 Max=100 Default=20
    MaximumDiminishedLoot = 20,
    -- Days until the maximum diminished loot is reached. Min=0 Max=3650 Default=3650
    DaysUntilMaximumDiminishedLoot = 3650,
    -- Multiplier for muscle strain from swinging weapons or carrying heavy loads.
    -- Min=0.00 Max=10.00 Default=0.70
    MuscleStrainFactor = 0.7,
    -- Multiplier for the discomfort caused by worn items.
    -- Min=0.00 Max=10.00 Default=0.80
    DiscomfortFactor = 0.8,
    -- Above 0, severe wound infections can cause damage.
    -- Min=0.00 Max=10.00 Default=1.00
    WoundInfectionFactor = 1.0,
    -- Randomly tinted clothing will not come out so dark that it is effectively black.
    NoBlackClothes = true,
    -- Removes the chance of failing when climbing ropes or over fences.
    EasyClimbing = false,
    -- Maximum burn time of material that can be put into a campfire, wood stove and
    -- similar. Min=1 Max=168 Default=8
    MaximumFireFuelHours = 8,
    -- Replaces the hit-chance mechanic with a damage-chance calculation, which favours
    -- the player's own aim. Default=Zombies only
    -- 1 = Disabled, 2 = Zombies only, 3 = All types of target
    FirearmUseDamageChance = 2,
    -- Multiplier for the distance from which zombies hear gunshots.
    -- Min=0.20 Max=2.00 Default=1.00
    FirearmNoiseMultiplier = 1.0,
    -- Multiplier for the chance of a firearm jamming. 0 disables jamming.
    -- Min=0.00 Max=10.00 Default=1.00
    FirearmJamMultiplier = 1.0,
    -- Multiplier for moodle effects on hit chance. 0 disables the penalty.
    -- Min=0.00 Max=10.00 Default=1.00
    FirearmMoodleMultiplier = 1.0,
    -- Multiplier for weather effects such as wind, rain and fog on hit chance.
    -- 0 disables them. Min=0.00 Max=10.00 Default=1.00
    FirearmWeatherMultiplier = 1.0,
    -- Head gear such as a welding mask affects hit chance.
    FirearmHeadGearEffect = true,
    -- Chance of turning a dirt floor into a clay floor. Applies to lakes.
    -- Min=0.00 Max=1.00 Default=0.05
    ClayLakeChance = 0.05,
    -- The same, applied to rivers. Min=0.00 Max=1.00 Default=0.05
    ClayRiverChance = 0.05,
    -- Min=1 Max=100 Default=20
    GeneratorTileRange = 20,
    -- How many levels above and below itself a generator can supply with electricity.
    -- Min=1 Max=15 Default=3
    GeneratorVerticalPowerRange = 3,
    -- Basement generation.
    Basement = {
        -- How often basements spawn in random locations. Default=Sometimes
        -- 1 = Never, 2 = Extremely rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often, 7 = Always
        SpawnFrequency = 4,
    },
    -- Map and map item settings.
    -- Map and map item settings.
    Map = {
        -- Show the minimap window.
        AllowMiniMap = false,
        -- Allow access to the world map.
        AllowWorldMap = true,
        -- The whole world map is known from the start.
        MapAllKnown = false,
        -- Maps can only be read when a light source is present.
        MapNeedsLight = true,
    },
    -- Zombie behaviour.
    -- Zombie behaviour.
    ZombieLore = {
        -- Zombie movement speed. Default=Random
        -- 1 = Sprinters, 2 = Fast shamblers, 3 = Shamblers, 4 = Random
        Speed = 4,
        -- With random speed, the percentage of zombies that are sprinters.
        -- Min=0 Max=100 Default=0
        SprinterPercentage = 0,
        -- Damage a zombie deals per attack. Default=Normal
        -- 1 = Superhuman, 2 = Normal, 3 = Weak, 4 = Random
        Strength = 2,
        -- How hard zombies are to kill. Default=Random
        -- 1 = Tough, 2 = Normal, 3 = Fragile, 4 = Random
        Toughness = 4,
        -- How the virus spreads. Default=Blood and saliva
        -- 1 = Blood and saliva, 2 = Saliva only, 3 = Everyone is infected, 4 = None
        Transmission = 1,
        -- How quickly the infection takes effect. Default=2-3 days
        -- 1 = Instant, 2 = 0-30 seconds, 3 = 0-1 minute, 4 = 0-12 hours, 5 = 2-3 days,
        -- 6 = 1-2 weeks, 7 = Never
        Mortality = 5,
        -- How quickly corpses rise as zombies. Default=0-1 minute
        -- 1 = Instant, 2 = 0-30 seconds, 3 = 0-1 minute, 4 = 0-12 hours, 5 = 2-3 days,
        -- 6 = 1-2 weeks
        Reanimate = 3,
        -- Zombie intelligence. Default=Basic navigation
        -- 1 = Navigate and use doors, 2 = Navigate, 3 = Basic navigation, 4 = Random
        Cognition = 3,
        -- Min=0 Max=100 Default=0
        DoorOpeningPercentage = 0,
        -- Which zombies can crawl under vehicles. Default=Often
        -- 1 = Never, 2 = Very rare, 3 = Rare, 4 = Sometimes, 5 = Often, 6 = Very often,
        -- 7 = Always
        CrawlUnderVehicle = 5,
        -- How long zombies remember a player after seeing or hearing them. Default=Normal
        -- 1 = Long, 2 = Normal, 3 = Short, 4 = None, 5 = Random,
        -- 6 = Random between normal and none
        Memory = 2,
        -- Zombie sight radius. Default=Random between normal and poor
        -- 1 = Eagle eyed, 2 = Normal, 3 = Poor, 4 = Random,
        -- 5 = Random between normal and poor
        Sight = 5,
        -- Zombie hearing radius. Default=Random between normal and poor
        -- 1 = Pinpoint, 2 = Normal, 3 = Poor, 4 = Random,
        -- 5 = Random between normal and poor
        Hearing = 5,
        -- Enables the advanced concealment mechanic: hiding behind cars, traits and weather
        -- being taken into account, and more.
        SpottedLogic = true,
        -- Wandering zombies attack doors and constructions when no player is seen or heard.
        ThumpNoChasing = false,
        -- Zombies can destroy player-built constructions and defences.
        ThumpOnConstruction = true,
        -- When zombies are more active. Inactive zombies move slower and are less likely to
        -- hunt. Default=Both
        -- 1 = Both, 2 = Night, 3 = Day
        ActiveOnly = 1,
        -- Zombies can set off house alarms when breaking through windows and doors.
        TriggerHouseAlarm = true,
        -- Several zombies can drag the player down while attacking, depending on their
        -- strength.
        ZombiesDragDown = true,
        -- Crawlers near a player also help drag them down.
        ZombiesCrawlersDragDown = false,
        -- Zombies can lunge at the player after climbing a fence if the player stands too
        -- close.
        ZombiesFenceLunge = true,
        -- Multiplier for the effectiveness of armour worn by zombies.
        -- Min=0.00 Max=100.00 Default=2.00
        ZombiesArmorFactor = 2.0,
        -- Maximum defence percentage that worn protective clothing can give a zombie.
        -- Min=0 Max=100 Default=85
        ZombiesMaxDefense = 85,
        -- Percentage chance of a zombie carrying a randomly attached weapon.
        -- Min=0 Max=100 Default=6
        ChanceOfAttachedWeapon = 6,
        -- Damage zombies take when falling from a height.
        -- Min=0.00 Max=100.00 Default=1.00
        ZombiesFallDamage = 1.0,
        -- Whether some seemingly dead zombies revive and attack.
        -- Default=Some zombies in the world play dead
        -- 1 = Some zombies in the world play dead,
        -- 2 = Some in the world, and some you 'kill', can play dead,
        -- 3 = Zombies never play dead
        DisableFakeDead = 1,
        -- Where zombies are kept from spawning around player spawn points.
        -- Default=In and around the building
        -- 1 = In and around the building, 2 = In the building, 3 = In the room,
        -- 4 = Zombies can spawn anywhere
        PlayerSpawnZombieRemoval = 1,
        -- How many zombies it takes to damage a tall fence. Min=-1 Max=100 Default=25
        FenceThumpersRequired = 25,
        -- How quickly zombies damage tall fences. Min=0.01 Max=100.00 Default=1.00
        FenceDamageMultiplier = 1.0,
    },
    -- Zombie population management.
    -- Zombie population management.
    ZombieConfig = {
        -- The same as the sandbox zombie count setting, where 4.0 equals insane.
        -- Min=0.00 Max=4.00 Default=0.65
        PopulationMultiplier = 0.65,
        -- Desired population at the start of the game. Min=0.00 Max=4.00 Default=1.00
        PopulationStartMultiplier = 1.0,
        -- Desired population density on the peak day. Min=0.00 Max=4.00 Default=1.50
        PopulationPeakMultiplier = 1.5,
        -- The day on which the population reaches its peak. Min=1 Max=365 Default=28
        PopulationPeakDay = 28,
        -- Hours that must pass before zombies respawn in a cell. 0 disables respawning.
        -- Min=0.00 Max=8760.00 Default=0.00
        RespawnHours = 0.0,
        -- Hours a cell must stay unseen before zombies respawn in it.
        -- Min=0.00 Max=8760.00 Default=0.00
        RespawnUnseenHours = 0.0,
        -- Fraction of a cell's desired population that may be placed at every respawn
        -- interval. Min=0.00 Max=1.00 Default=0.00
        RespawnMultiplier = 0.0,
        -- Hours that must pass before zombies wander to fill emptied parts of a cell.
        -- Min=0.00 Max=8760.00 Default=12.00
        RedistributeHours = 12.0,
        -- Distance virtual zombies travel towards the last sound they heard.
        -- Min=10 Max=1000 Default=100
        FollowSoundDistance = 100,
        -- Size of the groups idle real zombies form. 0 means no groups. Groups do not form
        -- inside buildings or forest zones. Min=0 Max=1000 Default=20
        RallyGroupSize = 20,
        -- Percentage by which group size may deviate from the standard size, in both
        -- directions. At 50 percent variance and a standard size of 20, groups range from
        -- 10 to 30. Min=0 Max=100 Default=50
        RallyGroupSizeVariance = 50,
        -- Distance idle real zombies travel in order to form groups. Min=5 Max=50 Default=20
        RallyTravelDistance = 20,
        -- Distance kept between zombie groups. Min=5 Max=25 Default=15
        RallyGroupSeparation = 15,
        -- Distance between group members and their leader. Min=1 Max=10 Default=3
        RallyGroupRadius = 3,
        -- Maximum number of tracked zombies before cleanup happens. 0 disables cleanup.
        -- The default of 300 is strongly recommended; higher values, or 0, can cause severe
        -- performance problems. Min=0 Max=5000 Default=300
        ZombiesCountBeforeDelete = 300,
    },
    -- XP rate per skill.
    -- XP rate per skill.
    MultiplierConfig = {
        -- Rate at which all skills level up. Min=0.00 Max=1000.00 Default=1.00
        Global = 1.0,
        -- When enabled, every skill uses the global multiplier.
        GlobalToggle = true,
        -- Rate at which the Fitness skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Fitness = 1.0,
        -- Rate at which the Strength skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Strength = 1.0,
        -- Rate at which the Sprinting skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Sprinting = 1.0,
        -- Rate at which the Lightfooted skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Lightfoot = 1.0,
        -- Rate at which the Nimble skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Nimble = 1.0,
        -- Rate at which the Sneaking skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Sneak = 1.0,
        -- Rate at which the Axe skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Axe = 1.0,
        -- Rate at which the Long blunt skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Blunt = 1.0,
        -- Rate at which the Short blunt skill levels up. Min=0.00 Max=1000.00 Default=1.00
        SmallBlunt = 1.0,
        -- Rate at which the Long blade skill levels up. Min=0.00 Max=1000.00 Default=1.00
        LongBlade = 1.0,
        -- Rate at which the Short blade skill levels up. Min=0.00 Max=1000.00 Default=1.00
        SmallBlade = 1.0,
        -- Rate at which the Spear skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Spear = 1.0,
        -- Rate at which the Maintenance skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Maintenance = 1.0,
        -- Rate at which the Carpentry skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Woodwork = 1.0,
        -- Rate at which the Cooking skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Cooking = 1.0,
        -- Rate at which the Farming skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Farming = 1.0,
        -- Rate at which the First aid skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Doctor = 1.0,
        -- Rate at which the Electrical skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Electricity = 1.0,
        -- Rate at which the Welding skill levels up. Min=0.00 Max=1000.00 Default=1.00
        MetalWelding = 1.0,
        -- Rate at which the Mechanics skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Mechanics = 1.0,
        -- Rate at which the Tailoring skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Tailoring = 1.0,
        -- Rate at which the Aiming skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Aiming = 1.0,
        -- Rate at which the Reloading skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Reloading = 1.0,
        -- Rate at which the Fishing skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Fishing = 1.0,
        -- Rate at which the Trapping skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Trapping = 1.0,
        -- Rate at which the Foraging skill levels up. Min=0.00 Max=1000.00 Default=1.00
        PlantScavenging = 1.0,
        -- Rate at which the Flint knapping skill levels up. Min=0.00 Max=1000.00 Default=1.00
        FlintKnapping = 1.0,
        -- Rate at which the Masonry skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Masonry = 1.0,
        -- Rate at which the Pottery skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Pottery = 1.0,
        -- Rate at which the Carving skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Carving = 1.0,
        -- Rate at which the Animal care skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Husbandry = 1.0,
        -- Rate at which the Tracking skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Tracking = 1.0,
        -- Rate at which the Metalworking skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Blacksmith = 1.0,
        -- Rate at which the Butchering skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Butchering = 1.0,
        -- Rate at which the Glassmaking skill levels up. Min=0.00 Max=1000.00 Default=1.00
        Glassmaking = 1.0,
    },
}
