# maps heathkit data types to timescaledb tables
# list all available data types and map them to a personicle data type
# this mapping will keep evolving with new and custom data types

DATA_DICTIONARY = {
    # Based on https://developer.apple.com/documentation/healthkit/data_types

    # Characteristic Identifiers
    "HKCharacteristicType.activityMoveMode": "metadata",
    "HKCharacteristicType.biologicalSex": "metadata",
    "HKCharacteristicType.bloodType": "metadata",
    "HKCharacteristicType.dateOfBirth": "metadata",
    "HKCharacteristicType.fitzpatrickSkinType": "metadata",
    "HKCharacteristicType.wheelchairUse": "metadata",

    # Activity
    "HKQuantityType.stepCount": "step_count",
    "HKQuantityType.distanceWalkingRunning": "distance",
    "HKQuantityType.distanceCycling": "distance",
    "HKQuantityType.pushCount": "push_count",
    "HKQuantityType.distanceWheelchair": "distance",
    "HKQuantityType.swimmingStrokeCount": "swimming_stroke_count",
    "HKQuantityType.distanceSwimming": "distance",
    "HKQuantityType.distanceDownhillSnowSports": "distance",
    "HKQuantityType.basalEnergyBurned": "energy_burned",
    "HKQuantityType.activeEnergyBurned": "energy_burned",
    "HKQuantityType.flightsClimbed": "step_count",
    "HKQuantityType.nikeFuel": "nike_fuel",
    "HKQuantityType.appleExerciseTime": "exercise_time",
    "HKCategoryType.appleStandHour": "stand_time",
    "HKQuantityType.appleStandTime": "stand_time",
    "HKQuantityType.vo2Max": "vo2_max",
    "HKCategoryType.lowCardioFitnessEvent": "event",

    # Body measurement
    "HKQuantityType.height": "metadata",
    "HKQuantityType.bodyMass": "metadata",
    "HKQuantityType.bodyMassIndex": "metadata",
    "HKQuantityType.leanBodyMass": "metadata",
    "HKQuantityType.bodyFatPercentage": "metadata",
    "HKQuantityType.waistCircumference": "metadata",

    # Reproductive Health
    "HKQuantityType.basalBodyTemperature": "body_temperature",
    "HKCategoryType.cervicalMucusQuality": "mucus_quality",
    "HKCategoryType.contraceptive": "contraceptive",
    "HKCategoryType.intermenstrualBleeding": "menstrual_bleeding",
    "HKCategoryType.lactation": "lactation",
    "HKCategoryType.menstrualFlow": "menstrual_flow",
    "HKCategoryType.ovulationTestResult": "ovulation_result",
    "HKCategoryType.pregnancy": "pregnancy",
    "HKCategoryType.sexualActivity": "sexual_activity",
    "HKCategoryType.pregnancyTestResult": "prengnancy_result",
    "HKCategoryType.progesteroneTestResult": "progresterone_resu;t",

    # Hearing
    "HKQuantityTypeIdentifier.environmentalAudioExposure": "audio_exposure",
    "HKQuantityTypeIdentifier.headphoneAudioExposure": "audio_exposure",
    "HKCategoryTypeIdentifier.environmentalAudioExposureEvent": "audio_exposure_event",
    "HKCategoryTypeIdentifier.headphoneAudioExposureEvent": "audio_exposure_event",

    # Vital Signs
    "HKQuantityTypeIdentifier.heartRate": "heart_rate",
    "HKCategoryTypeIdentifier.lowHeartRateEvent": "heart_rate_event",
    "HKCategoryTypeIdentifier.highHeartRateEvent": "heart_rate_event",
    "HKCategoryTypeIdentifier.irregularHeartRhythmEvent": "heart_rate_event",
    "HKQuantityTypeIdentifier.restingHeartRate": "heart_rate",
    "HKQuantityTypeIdentifier.heartRateVariabilitySDNN": "heart_rate_variability",
    "HKQuantityTypeIdentifier.walkingHeartRateAverage": "heart_rate",
    "HKDataTypeIdentifierHeartbeatSeries": "",
    "HKElectrocardiogramType": "",
    "HKQuantityTypeIdentifier.oxygenSaturation": "",
    "HKQuantityTypeIdentifier.bodyTemperature": "",
    "HKCorrelationTypeIdentifier.bloodPressure": "",
    "HKQuantityTypeIdentifier.bloodPressureSystolic": "",
    "HKQuantityTypeIdentifier.bloodPressureDiastolic": "",
    "HKQuantityTypeIdentifier.respiratoryRate": "",

    # Nutrition
    "dietaryEnergyConsume": "",
    "dietaryFatTota": "",
    "dietaryFatSaturate": "",
    "dietaryCholestero": "",
    "dietaryCarbohydrate": "",
    "dietaryFibe": "",
    "dietarySuga": "",
    "dietaryProtei": "",
    "dietaryCalciu": "",
    "dietaryIro": "",
    "dietaryPotassiu": "",
    "dietarySodiu": "",
    "dietaryVitamin": "",
    "dietaryVitamin": "",
    "dietaryVitamin": "",

    # Alcohol Consumption
    "HKQuantityTypeIdentifier.bloodAlcoholContent": "",
    "HKQuantityTypeIdentifier.numberOfAlcoholicBeverages": "",

    # Mobility
    "HKQuantityTypeIdentifier.appleWalkingSteadiness": "",
    "HKCategoryTypeIdentifier.appleWalkingSteadinessEvent": "",
    "HKQuantityTypeIdentifier.sixMinuteWalkTestDistance": "",
    "HKQuantityTypeIdentifier.walkingSpeed": "",
    "HKQuantityTypeIdentifier.walkingStepLength": "",
    "HKQuantityTypeIdentifier.walkingAsymmetryPercentage": "",
    "HKQuantityTypeIdentifier.walkingDoubleSupportPercentage": "",
    "HKQuantityTypeIdentifier.stairAscentSpeed": "",
    "HKQuantityTypeIdentifier.stairDescentSpeed": "",

    # Symptoms


    # Lab and Test Results
    "HKQuantityTypeIdentifier.bloodAlcoholContent": "",
    "HKQuantityTypeIdentifier.bloodGlucose": "",
    "HKQuantityTypeIdentifier.electrodermalActivity": "",
    "HKQuantityTypeIdentifier.forcedExpiratoryVolume1": "",
    "HKQuantityTypeIdentifier.forcedVitalCapacity": "",
    "HKQuantityTypeIdentifier.inhalerUsage": "",
    "HKQuantityTypeIdentifier.insulinDelivery": "",
    "HKQuantityTypeIdentifier.numberOfTimesFallen": "",
    "HKQuantityTypeIdentifier.peakExpiratoryFlowRate": "",
    "HKQuantityTypeIdentifier.peripheralPerfusionIndex": "",


    # Mindfulness and Sleep
    "HKCategoryTypeIdentifier.sleepAnalysis": "",
    "HKCategoryTypeIdentifier.mindfulSession": "",

    # Self Care
    "HKCategoryTypeIdentifier.toothbrushingEvent": "",
    "HKCategoryTypeIdentifier.handwashingEvent": "",

    # Workouts
    "HKWorkoutTypeIdentifier": "",
    "HKWorkoutRouteTypeIdentifier": "",

    # Clinical Records

    # UV Exposure

    "HKCategoryType": "",
    "HKCorrelationType": "",
    "HKActivitySummaryType": "",
    "HKAudiogramSampleType": "",
    "HKElectrocardiogramType": "",
    "HKSeriesType": "",
    "HKClinicalType": "",
    "HKWorkoutType": "",
    "HKObjectType": "",
    "HKSampleType": ""
}